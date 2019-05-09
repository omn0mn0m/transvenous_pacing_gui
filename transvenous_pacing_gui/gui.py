"""
.. module:: gui
    :platform: Windows
    :synopsis: Main application frame for the entire GUI
 
.. moduleauthor:: Nam Tran <tranngocnam97@gmail.com>
"""

# Standard Library imports
import tkinter as tk
from tkinter import ttk
import os
import sys

# Appends the system path to allow absolute path imports due to the command line structure
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Project imports
from transvenous_pacing_gui.guiclient import InstructorGUI
from transvenous_pacing_gui.guiserver import StudentGUI

class MainApplication(tk.Frame):
    """Main application frame for the entire GUI
 
    This class contains a tkinter notebook with the student and instructor GUIs
    in their own tabs.
    """

    def __init__(self, parent, *args, **kwargs):
        """Constructor
 
        Args:
            parent (tk.widget): parent widget to make the frame a child of
            *args: Variable length argument list
            **kwargs: Arbitrary keyword argument list
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Black background style for ttk.Frame
        s = ttk.Style()
        s.configure('new.TFrame', background='black')

        # GUI design
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.bind("<Button-1>", self.on_click)

        # Student GUI design
        self.student_gui = StudentGUI(self.notebook, style='new.TFrame')

        # Teacher GUI design
        self.instructor_gui = InstructorGUI(self.notebook)

        # Building the notebook
        self.notebook.add(self.student_gui, text="Student")
        self.notebook.add(self.instructor_gui, text="Instructor")
        self.notebook.pack()

    def on_click(self, event):
        """on_click event for the notebook tabs

        This event pauses and unpauses the student GUI signal depending
        on if it is put in or out of focus.
 
        Args:
            event (tk.event): The event that called this event function
        """
        # Tcl function to determine tab at position
        clicked_tab = self.notebook.tk.call(self.notebook._w, "identify", "tab", event.x, event.y)
        active_tab = self.notebook.index(self.notebook.select())
        
        # If switching tabs
        if not clicked_tab == active_tab:
            # If the tab that was clicked is the student GUI
            if clicked_tab == 0:
                # Start/ resume the plot animation
                self.student_gui.start_plot()
            # If the tab that was clicked is the instructor GUI
            elif clicked_tab == 1:
                # Stop the plot animation
                self.student_gui.pause_plot()
            # Else do nothing
            else:
                pass

    def stop_gui(self):
        """Stops both the instructor and student GUI tabs

        This function is used to close any open connections from the student
        or instructor frames. This is useful when the GUI is closed.
        """
        self.instructor_gui.stop_gui()
        self.student_gui.stop_gui()

def main():
    """main function for the GUI software

    This function doubles as what is called for the transvenous_pacing_gui
    command.
    """

    # Root application window 
    root = tk.Tk()
    root.title("Tranvenous Pacing GUI")

    # Instantiating the main application frame and putting it on the root window
    main_app = MainApplication(root)
    main_app.pack(side="top", fill="both", expand=True)

    # GUI loop
    root.mainloop()

    # Closes GUI connections when the loop is exited
    main_app.stop_gui()

# Runs the main function when this script is called
if __name__ == "__main__":
    main()
