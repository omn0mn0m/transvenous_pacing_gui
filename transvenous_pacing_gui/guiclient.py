"""
.. module:: guiclient
    :platform: Windows
    :synopsis: Instructor GUI tkinter frame
 
.. moduleauthor:: Nam Tran, Richie Beck, Cooper Pearson
"""

# Standard Library imports
import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import Radiobutton
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Scale
from tkinter import BooleanVar

# Pip Dependency imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Project imports
from transvenous_pacing_gui.signals import Signals
from transvenous_pacing_gui.client import Client

class InstructorGUI(tk.Frame):
    """Instructor GUI frame to be used in the main GUI
 
    This class contains multiple input widgets for the GUI,
    as well as the Client class used to connect with the
    socket server.
    """

    # Settings
    header_1_style = "TkDefaultFont 18 bold"
    header_2_style = "TkDefaultFont 16 bold"
    default_style  = "TkDefaultFont 14"

    def __init__(self, parent, *args, **kwargs):
        """Constructor
 
        Args:
            parent (tk.widget): parent widget to make the frame a child of
            *args: Variable length argument list
            **kwargs: Arbitrary keyword argument list
        """
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Socket client
        self.client = Client(port=25565)

        # ============ GUI Variables ============ 
        self.host = StringVar(self, value=self.client.get_hostname())

        # Instructor realtime setting variables
        self.hr = IntVar(self, value=80)
        self.threshold = StringVar(self, value=20)
        self.hr_paced = IntVar(self, value=80)
        
        self.pathway_1 = IntVar(self, value=0)
        self.pathway_2 = IntVar(self, value=0)

        # Manual Override variables
        self.position = IntVar(self, value=0)
        self.is_pacing = BooleanVar(self, value=False)
        self.is_pos_overriding = BooleanVar(self, value=False)

        # ============ Main Frame Sides ===========
        # Left side frame
        frame_left = Frame(self, bd=1, relief=tk.SUNKEN)
        frame_left.pack(side=tk.LEFT, padx=10, pady=10)
        Label(frame_left, text="Override Settings", font=self.header_1_style).pack()

        # Middle frame
        frame_mid = Frame(self, bd=1, relief=tk.SUNKEN)
        frame_mid.pack(side=tk.LEFT, padx=10, pady=10)
        Label(frame_mid, text="Real-Time Settings", font=self.header_1_style).pack()

        # Right side frame
        frame_right = Frame(self, bd=1, relief=tk.SUNKEN)
        frame_right.pack(side=tk.RIGHT, padx=10, pady=10)
        Label(frame_right, text="Display Preview", font=self.header_1_style).pack()

        # ============ Position Selection ===============
        frame_position = Frame(frame_left)
        frame_position.pack(pady=5)

        # Sets the position variable to invoke a callback
        self.position.trace('w', self.callback_manual_pos)

        # Radiobutton options for the override
        POSITIONS = [
            ("Superior Vena Cava", 1),
            ("High Right Atrium", 2),
            ("Mid Right Atrium", 3),
            ("Low Right Atrium", 4),
            ("Right Ventricle", 5),
            ("Right Ventricular Wall", 6),
            ("Asystole", 0),
        ]

        Label(frame_position, text="Show Manual Position", font=self.default_style).pack()

        # Creates each radiobutton item
        for button_text, position_value in POSITIONS:
            Radiobutton(frame_position, text=button_text, value=position_value, variable=self.position, font=self.default_style).pack()

        # Creates a toggle button to start/stop the manual override
        self.btn_pos_override = Button(frame_position, text="Start Override", command=self.toggle_pos_override, fg="green", font=self.default_style)
        self.btn_pos_override.pack()

        # ============ Command Sends =============
        frame_command = Frame(frame_left)
        frame_command.pack(pady=5)

        Label(frame_command, text="Commands", font=self.default_style).pack()

        # Button to make the microcontroller recalibrate its sensor values
        btn_recalibrate = Button(frame_command, text="Calibrate Sensors", command=lambda: self.send_command('cal'), fg="green", font=self.default_style)
        btn_recalibrate.pack(side=tk.LEFT)

        # Button to make the student GUI restart the signal at asystole in case it gets stuck
        btn_reset_signal = Button(frame_command, text="Reset Signal (Asystole)", command=lambda: self.send_command('ressig'), fg="green", font=self.default_style)
        btn_reset_signal.pack(side=tk.LEFT)

        # ============ Connection Space ===============
        frame_connection = Frame(frame_mid)
        frame_connection.pack(pady=5)

        # Displays the host machine's IP address for use with the other GUI
        ip_label = "Device IP: {}".format(self.client.get_ip())
        Label(frame_connection, text=ip_label, font=self.default_style).pack()

        Label(frame_connection, text="Hostname", font=self.default_style).pack(side=tk.LEFT)

        # Area to enter the hostname to connect to
        entry_hostname = Entry(frame_connection, textvariable=self.host, font=self.default_style)
        entry_hostname.pack(side=tk.LEFT)

        # Button to start the TCP/IP connection
        btn_connect = Button(frame_connection, text="Connect", command=self.connect, fg="green", font=self.default_style)
        btn_connect.pack(side=tk.LEFT)

        # ============ Customisation Space ===============
        frame_signal = Frame(frame_mid)
        frame_signal.pack(pady=5)

        # Intrinsic heart rate entry area
        Label(frame_signal, text="Heart Rate", font=self.default_style).grid(row=0, column=0)
        
        scale_hr = Scale(frame_signal, from_=0, to=100, length=150, variable=self.hr, orient=tk.HORIZONTAL)
        scale_hr.grid(row=0, column=1)

        entry_hr = Entry(frame_signal, textvariable=self.hr, font=self.default_style, width=4)
        entry_hr.grid(row=0, column=2)

        # Pacing threshold entry area
        Label(frame_signal, text="Pacing Threshold", font=self.default_style).grid(row=1, column=0)

        scale_threshold = Scale(frame_signal, from_=0, to=50, length=150, variable=self.threshold, orient=tk.HORIZONTAL)
        scale_threshold.grid(row=1, column=1)

        entry_threshold = Entry(frame_signal, textvariable=self.threshold, font=self.default_style, width=4)
        entry_threshold.grid(row=1, column=2)

        # Paced heart rate entry area
        Label(frame_signal, text="Paced Heart Rate", font=self.default_style).grid(row=2, column=0)

        scale_hr_paced = Scale(frame_signal, from_=0, to=100, length=150, variable=self.hr_paced, orient=tk.HORIZONTAL)
        scale_hr_paced.grid(row=2, column=1)

        entry_hr_paced = Entry(frame_signal, textvariable=self.hr_paced, font=self.default_style, width=4)
        entry_hr_paced.grid(row=2, column=2)

        # Buttons for this area
        frame_signal_buttons = Frame(frame_signal)
        frame_signal_buttons.grid(row=3, columnspan=3)

        # Sends the updated settings (heart rate, pacing threshold, paced heart rate) to the student GUI
        btn_send_customisations = Button(frame_signal_buttons, text="Update ECG", command=self.send_customisations, fg="green", font=self.default_style, pady=5)
        btn_send_customisations.pack(side=tk.LEFT, fill=tk.X)

        # Starts a simulated pacer signal
        self.btn_pacing = Button(frame_signal_buttons, text="Start Pacing", command=self.toggle_pacing, fg="green", font=self.default_style, pady=5)
        self.btn_pacing.pack(side=tk.RIGHT, fill=tk.X)

        # ========== Pathway Selection ==============
        frame_pathway = Frame(frame_mid)
        frame_pathway.pack(pady=5)

        # Sets both pathway variables to invoke a callback
        self.pathway_1.trace('w', self.callback_pathway_1)
        self.pathway_2.trace('w', self.callback_pathway_2)

        # Alternate pathway options
        PATHWAYS_1 = [
            ("Low Right Atrium", 0),
            ("Inferior Vena Cava", 10)
        ]

        PATHWAYS_2 = [
            ("Right Ventricular Wall", 0),
            ("Pulmonary Artery", 10)
        ]

        Label(frame_pathway, text="Pathway Selection 1", font=self.header_2_style).pack(pady=5)

        # Create each radiobutton for the first pathway option
        for button_text, pathway_value in PATHWAYS_1:
            Radiobutton(frame_pathway, text=button_text, value=pathway_value, variable=self.pathway_1, font=self.default_style).pack()

        Label(frame_pathway, text="Pathway Selection 2", font=self.header_2_style).pack(pady=5)

        # Create each radiobutton for the second pathway option
        for button_text, pathway_value in PATHWAYS_2:
            Radiobutton(frame_pathway, text=button_text, value=pathway_value, variable=self.pathway_2, font=self.default_style).pack()

        # ======== Display Preview =========
        # Instantiated signals class to generate signals
        self.ecg_signals = Signals()

        self.new_x = [0.0]
        self.new_y = [0.0]

        self.last_x = 0
        self.last_x_lim = 0

        self.position_to_show = 0

        self.variation = 0

        self.flat_span = False
        self.end_flat = 0
        self.flat_span_y = 0
        self.plot_point = 0

        # Creates plotting canvas
        self.fig = plt.Figure(figsize=(10, 4.5), dpi=100,facecolor='k',edgecolor='k')
        
        canvas = FigureCanvasTkAgg(self.fig, master=frame_right)
        canvas.get_tk_widget().pack()

        # Sets plot customisations
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(self.last_x_lim, 4)
        self.ax.set_ylim(-3.0, 3.0)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.xaxis.set_tick_params(width=1, top=True)
        self.ax.set_facecolor('black')

        self.line, = self.ax.plot(0, 0)
        self.ax.get_lines()[0].set_color("xkcd:lime")

        # Starts an animated plot for the ECG signal
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=24, blit=True)

    def animate(self, i):
        """Animation function that is called periodically
 
        Args:
            i (int): the current frame value (not used)

        Returns:
            line (matplotlib.line): The line to plot with the next value
        """

        # If currently overriding the student GUI, show the display preview
        if self.is_pos_overriding.get():
            # Set the position index value based on which source is responsible for the signal
            position_index = self.position.get()

            # Set initial heart rate to use
            hr_to_use = self.hr.get()

            # Adjust position and heart rate based on alternative pathways and pacer setting
            if position_index == 4:
                position_index = position_index + self.pathway_1.get()
            elif position_index == 6:
                position_index = position_index + self.pathway_2.get()

                # Show the paced signal if pacer override is active
                if not position_index == 16 and self.is_pacing.get():
                    position_index = 26
                    hr_to_use = self.hr_paced.get()
            else:
                # If no overrides or special settings, just keep the position the same
                position_index = position_index

            # Get the ECG signal values for the corresponding settings
            [x, y] = self.ecg_signals.get_signal(self.ecg_signals.signal_index[position_index], hr_to_use)

            # If not currently traveling between beats
            if not self.flat_span:
                # Set a variable to the potential next value
                x_val = self.last_x + x[self.plot_point]

                # If the potential new value is not going backwards
                if x_val > self.new_x[-1]:
                    # Add the new x and y values to the axis lists
                    self.new_x.append(x_val)
                    self.new_y.append(y[self.plot_point])

                    # Update the line
                    self.line.set_data(self.new_x, self.new_y)  # update the data
                
                # If at the end of the beat
                if self.plot_point== 29:
                    # Update where the last x value to build from is
                    self.last_x = self.new_x[-1]

                    # Start plotting for a flat area
                    self.end_flat = (x[-1] - x[-2]) + self.new_x[-1]
                    self.flat_span_y = y[-1]
                    self.flat_span = True
                    
                # Go back to the start of the heart beat if at the end of the beat
                if self.plot_point == 29:
                    self.plot_point = 0
                # Go to the next beat value otherwise
                else:
                    self.plot_point = self.plot_point + 1
            # If current traveling between beats
            else:
                # Add the new x and y values to the axis lists
                self.new_x.append(self.new_x[-1] + 0.05)
                self.new_y.append(self.flat_span_y)

                # Update the line
                self.line.set_data(self.new_x, self.new_y)  # update the data

                # If reached the end of the flat line area between beats
                if self.new_x[-1] >= self.end_flat:
                    # Stop plotting flat
                    self.flat_span = False
                    self.last_x = self.new_x[-1]
            
            # If at the end of the plotting window
            if self.new_x[-1] >= self.last_x_lim + 5:
                # Shift the plotting window (this is used instead of a reset to allow for future ECG output options)
                self.last_x_lim += 5
                self.ax.set_xlim(self.last_x_lim, self.last_x_lim + 5)

        # Returns the new line to the plot
        return self.line,

    def connect(self):
        """Connects the instructor GUI to the student GUI"""

        # Update the hostname
        self.client.set_hostname(self.host.get())

        # Actually connect
        self.client.start()

    def send_command(self, message):
        """Sends a message from the instructor GUI to the student GUI

        Args:
            message (str): Message to send through the socket connection
        """
        self.client.send_data(message)

    def send_customisations(self):
        """Sends updated customisation data from instructor GUI to the student GUI"""

        # Command code
        self.client.send_data("update")
        # Data
        self.client.send_data("{},{},{}".format(self.hr.get(), self.threshold.get(), self.hr_paced.get()))

    def toggle_pos_override(self):
        """Sends position override data from the instructor to the student GUI"""

        # Toggle if we are overriding
        self.is_pos_overriding.set(not self.is_pos_overriding.get())

        # If we are now overriding
        if self.is_pos_overriding.get():
            # Start command code
            self.client.send_data("start-pos")
            # Data
            self.client.send_data("%d" % self.position.get())
            # Switch the toggle button
            self.btn_pos_override.config(fg="red", text="Stop Override")

            self.ani.event_source.start()
        # If we are now not overriding
        else:
            # Stop command code
            self.client.send_data("stop-pos")
            # Switch the toggle button
            self.btn_pos_override.config(fg="green", text="Start Override")
            # Stop the preview plotting
            self.ani.event_source.stop()

    def toggle_pacing(self):
        """Toggles whether to be pacing"""

        # Toggles if we are pacing
        self.is_pacing.set(not self.is_pacing.get())

        # If we are now pacing
        if self.is_pacing.get():
            # Start pacing command code
            self.client.send_data("start-pace")
            # Send customisation network update
            self.send_customisations()
            # Switch the toggle button
            self.btn_pacing.config(fg="red", text="Stop Pacing")
        else:
            # Stop pacing command code
            self.client.send_data("stop-pace")
            # Switch the toggle button
            self.btn_pacing.config(fg="green", text="Start Pacing")
            
    def callback_pathway_1(self, *args):
        """Callback function for when the pathway is switched.

        This will automatically send an updated pathway.
 
        Args:
            *args: Variable length argument list
        """

        # Command code
        self.client.send_data("chpa1")
        # Data
        self.client.send_data("%d" % self.pathway_1.get())

    def callback_pathway_2(self, *args):
        """Callback function for when the pathway is switched.

        This will automatically send an updated pathway.
 
        Args:
            *args: Variable length argument list
        """
        
        # Command code
        self.client.send_data("chpa2")
        # Data
        self.client.send_data("%d" % self.pathway_2.get())
    
    def callback_manual_pos(self, *args):
        """Callback function for when the pathway is switched.

        This will automatically send an updated pathway.
 
        Args:
            *args: Variable length argument list
        """
        
        # If we are actively overriding
        if self.is_pos_overriding.get():
            # Command code
            self.client.send_data("manual-pos")
            # Data
            self.client.send_data("%d" % self.position.get())
    
    def stop_gui(self):
        """Stops the instructor GUI client"""
        self.client.stop()
