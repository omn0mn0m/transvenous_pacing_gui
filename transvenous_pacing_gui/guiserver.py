"""
.. module:: guiserver
    :platform: Windows
    :synopsis: Instructor GUI tkinter frame
 
.. moduleauthor:: Nam Tran, Richie Beck, Cooper Pearson
"""

# Standard Library imports
import tkinter as tk
from tkinter import ttk
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import Frame
from tkinter import StringVar
from tkinter import OptionMenu
from queue import Queue
import random

# Pip Dependency imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
from serial import SerialException
import serial.tools.list_ports

# Project Modules
from transvenous_pacing_gui.signals import Signals
from transvenous_pacing_gui.server import Server

class StudentGUI(tk.Frame):
    """Student GUI frame to be used in the main GUI
 
    This class contains multiple input widgets for the GUI,
    as well as the Server class used to connect with the
    socket client.
    """

    # Settings
    header_1_style = "TkDefaultFont 42 bold"
    header_2_style = "TkDefaultFont 18 bold"
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

        # Mutex for the networking thread
        self.socket_queue = Queue()

        # Socket server
        self.server = Server(port=25565)
        self.server.start(self.socket_queue)

        # Instantiated signals class to generate signals
        self.ecg_signals = Signals()

        # ============ GUI Variables ============ 
        # Instructor realtime setting variables
        self.hr = IntVar(self, value=80)
        self.threshold = IntVar(self, value=20)
        self.hr_paced = IntVar(self, value=80)

        # Manual Override variables
        self.position = IntVar(self, value=0)
        self.override_position = BooleanVar(self, value=False)

        self.hr1 = StringVar(self, value='0')

        self.pathway_1 = IntVar(self, value=0)
        self.pathway_2 = IntVar(self, value=0)
        self.is_paced = BooleanVar(self, value=False)

        # Serial in position
        self.serial_position = IntVar(self, value='0')

        # Command variables
        self.wait_for_update = BooleanVar(self, value=False)
        self.wait_for_position = BooleanVar(self, value=False)
        self.wait_for_pathway_1 = BooleanVar(self, value=False)
        self.wait_for_pathway_2 = BooleanVar(self, value=False)

        # ============ Main Frame Sides ===========
        # Signals frame
        frame_signals = Frame(self, bg='black')
        frame_signals.pack(side=tk.LEFT)

        # Monitor value frame
        frame_values = Frame(self, bg='black')
        frame_values.pack(side=tk.RIGHT, padx=10)

        # Take care of plotting
        self.plot_point = 0

        self.new_x = [0.0]
        self.new_y = [0.0]

        self.last_x = 0
        self.last_x_lim = 0

        self.position_to_show = 0

        self.variation = 0

        self.flat_span = False
        self.end_flat = 0
        self.flat_span_y = 0

        # HR Monitor setup
        tk.Label(frame_values, text="HR", font=self.header_2_style, bg="black", fg="lime green").pack()
        tk.Label(frame_values, textvariable=self.hr1,font=self.header_1_style,bg="black", fg="lime green").pack()
        
        # Serial selection setup
        Options=['']
        Options.extend(serial.tools.list_ports.comports())

        self.s = 'RIP'
        self.ser = None

        self.variable = StringVar(self)
        self.variable.set(Options[0]) #Default option

        w=OptionMenu(frame_signals, self.variable, *Options)
        w.grid(row=2, column=1)

        self.variable.trace('w', self.change_dropdown)

        # Create plotting canvas
        fig = plt.Figure(figsize=(14, 4.5), dpi=100,facecolor='k',edgecolor='k')

        canvas = FigureCanvasTkAgg(fig, master=frame_signals)
        canvas.get_tk_widget().grid(row=1, column=1)

        # Sets plot customisations
        self.ax = fig.add_subplot(111)
        self.ax.set_xlim(self.last_x_lim, 4)
        self.ax.set_ylim(-3.0, 3.0)
        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.xaxis.set_tick_params(width=1, top=True)
        self.ax.set_facecolor('black')

        self.line, = self.ax.plot(0, 0)
        self.ax.get_lines()[0].set_color("xkcd:lime")

        # Starts an animated plot for the ECG signal
        self.ani = animation.FuncAnimation(fig, self.animate, interval=24, blit=True)

        # Polling Initialisation for socket connection
        self.after(10, self.read_socket)

    def animate(self, i):
        """Animation function that is called periodically
 
        Args:
            i (int): the current frame value (not used)

        Returns:
            line (matplotlib.line): The line to plot with the next value
        """

        # Set the position index value based on which source is responsible for the signal
        if self.override_position.get():
            position_index = self.position.get()
        else:
            position_index = self.serial_position.get()

        # Set initial heart rate to use
        hr_to_use = self.hr.get()

        # Adjust position and heart rate based on alternative pathways and pacer setting
        if position_index == 4:
            position_index = position_index + self.pathway_1.get()
        elif position_index == 6:
            position_index = position_index + self.pathway_2.get()

            # Show the paced signal if pacer override is active
            if not position_index == 16 and self.is_paced.get():
                position_index = 26
                hr_to_use = self.hr_paced.get()
        else:
            # If no overrides or special settings, just keep the position the same
            position_index = position_index

        # Print what position is being printed
        print(self.ecg_signals.signal_index[position_index])

        # Display heart rate value on GUI
        if position_index == 0:
            self.hr1.set(0)
        else:
            self.hr1.set(hr_to_use)

        # Get the ECG signal values for the corresponding settings
        [x, y] = self.ecg_signals.get_signal(self.ecg_signals.signal_index[position_index], hr_to_use, self.variation)

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

    def change_dropdown(self, *args):
        """Callback function for when a COM port is selected.

        This will automatically send an updated pathway.
 
        Args:
            *args: Variable length argument list
        """

        # If the current selected port is not empty
        if not self.variable.get() == '':
            # Try to connect
            try:
                choice = self.variable.get().split(' -')
                # Open the COM port
                self.ser = serial.Serial(choice[0], 9600)
                print('Connection established.')

                # Start the polling for the serial
                self.after(10, self.read_serial)
            # Print exception if it fails
            except SerialException as e:
                print('Error: {}'.format(e))


    def read_socket(self):
        """Reads the socket connection and interprets the contents for a command to run.

        The valid commands are as follows:
            - update: listen for an incoming ECG settings update
            - start-pos: start manual position override
            - stop-pos: stop manual position override
            - manual-pos: listen for a new override position
            - chpa1: listen for an updated alternative pathway 1
            - chpa2: listen for an updated alternative pathway 2
            - close: close the socket
            - start-pace: start pacing override
            - stop-pace: stop pacing override
            - cal: signal for the microcontroller to recalibrate
            - ressig: reset the student GUI signal
        """

        # If there is something in the socket queue
        if not self.socket_queue.empty():
            # Read from the queue
            message = self.socket_queue.get()

            # Print the value
            print(message)

            # If a previous command set the GUI to wait for a new ECG customisation
            if self.wait_for_update.get():
                # Strip the new value of any commas (for multivalue messages)
                result = [x.strip() for x in message.decode('utf-8').split(',')]

                # Set the ECG customisation values
                self.hr.set(result[0])
                self.threshold.set(result[1])
                self.hr_paced.set(result[2])
                
                # Stop waiting for an update
                self.wait_for_update.set(False)
            # If the previous command set the GUI to wait for a new manual override position
            elif self.wait_for_position.get():
                # Set the position to the new incoming value
                self.position.set(int(message.decode('utf-8')))
                # Stop listening for new value
                self.wait_for_position.set(False)
                # Override the position
                self.override_position.set(True)
            # If the previous command set the GUI to wait for a new pathway
            elif self.wait_for_pathway_1.get():
                # Set the new pathway
                self.pathway_1.set(int(message.decode('utf-8')))
                print(self.pathway_1.get())
                # Stop listening for a new pathway
                self.wait_for_pathway_1.set(False)
            # If the previous command set the GUI to wait for a new pathway
            elif self.wait_for_pathway_2.get():
                # Set the new pathway
                self.pathway_2.set(int(message.decode('utf-8')))
                print(self.pathway_2.get())
                # Stop listening for a new pathway
                self.wait_for_pathway_2.set(False)
            # Determine what command to run otherwise
            else:
                if message == b'update':
                    self.wait_for_update.set(True)
                elif message == b'start-pos':
                    self.wait_for_position.set(True)
                elif message == b'stop-pos':
                    self.override_position.set(False)
                elif message == b'manual-pos':
                    self.wait_for_position.set(True)
                elif message == b'chpa1':
                    self.wait_for_pathway_1.set(True)
                elif message == b'chpa2':
                    self.wait_for_pathway_2.set(True)
                elif message == b'close':
                    self.destroy()
                elif message == b'start-pace':
                    self.is_paced.set(True)
                elif message == b'stop-pace':
                    self.is_paced.set(False)
                elif message == b'cal':
                    self.write_serial(b'C')
                elif message == b'ressig':
                    self.position_to_show = 0
        
        # Put this function to call on another timer
        self.after(10, self.read_socket)

    def pause_plot(self):
        """Pause the plotting animation"""
        self.ani.event_source.stop()

    def start_plot(self):
        """Start the plotting animation"""
        self.ani.event_source.start()

    def write_serial(self, message):
        """Write a message to the microcontroller over serial
 
        Args:
            message (str): Message to write the microcontroller
        """

        # If a serial connection exists
        if not self.ser == None:
            # Try to write the message
            try:
                self.ser.write(message)
                print(message)
            # Print an exception if one occurs
            except Exception as e:
                print('Error: {}'.format(e))

    def read_serial(self):
        """Read from the serial"""

        # If a serial connection exists
        if not self.ser == None:
            # Try to read
            try:
                # If there is an incoming message
                if self.ser.in_waiting:
                    # Read in one byte
                    self.s = self.ser.read()
                    # Update the GUI position with that value
                    self.serial_position.set(int(self.s))
                    print(int(self.s))
            # Catch an exception and print it
            except Exception as e:
                print('Error: {}'.format(e))

        # Put read serial back on a timer
        self.after(10, self.read_serial)

    def stop_gui(self):
        """Cleanup any option connections"""
        # Try to close out of the serial and the server
        try:
            self.server.stop()
            self.ser.close()
        # Print any exceptions that occur
        except Exception as e:
            print(e)
