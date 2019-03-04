# Pip Modules
import tkinter as Tk
from tkinter import StringVar
from tkinter import OptionMenu

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import multiprocessing

import sys
import serial
#import time
from serial import SerialException
import serial.tools.list_ports

# Project Modules
import signals
import server

# Socket Connection
out_queue = multiprocessing.Queue()
in_queue = multiprocessing.Queue()

# Take care of plotting
fig = plt.Figure(figsize=(14, 4.5), dpi=100)

new_x = []
new_y = []

global last_x
last_x = 0

global last_x_lim
last_x_lim = 0

global variable

def animate(i):
    # Switch statement for the serial location in order to get which one to do
    global hr
    global threshold
    global position
    global last_x
    global last_x_lim
   
    if position.get() == 'SVC':
        [x, y] = signals.Default_Line()
    elif position.get() == 'HRA':
        [x, y] = signals.High_RA_V1(hr.get())
    elif position.get() == 'MRA':
        [x, y] = signals.Mid_RA_V1(hr.get())
    elif position.get() == 'LRA':
        [x, y] = signals.Low_RA_V1(hr.get())
    elif position.get() == 'IVC':
        [x, y] = signals.IVC_V1(hr.get())
    elif position.get() == 'RV':
        [x, y] = signals.Default_Line()
    elif position.get() == 'RVW':
        [x, y] = signals.Default_Line()
    elif position.get() == 'PA':

        [x, y] = signals.Default_Line()
    else:
        try:
            ser = serial.Serial(variable.get(), 9600)
        except SerialException as e:
            print('Error: {}'.format(e))
        while ser.is_open
            s=ser.read()
            if s='1'
                [x, y] = signals.High_RA_V1(80)
            elif s='2'
                [x, y] = signals.Mid_RA_V1(80)
            elif s='3'
                [x, y] = signals.Low_RA_V1(80)
            elif s='4'
                [x, y] = signals.High_VA_V1(80)
            elif s='5'
                [x, y] = signals.Mid_VA_V1(80)
            elif s='6'
                [x, y] = signals.Low_VA_V1(80)
            elif s='7'
                [x, y] = signals.High_VA_V1(80)
            elif s='8'
                [x, y] = signals.RV_Wall_V1(80)
            elif s='9'
                [x, y] = signals.RV_Wall_V1(80)


    global last_x
    global last_x_lim
    
    x_val = last_x + x[i]
    
    new_x.append(x_val)
    new_y.append(y[i])
    
    line.set_data(new_x, new_y)  # update the data
    
    if i == 29:
        last_x = new_x[-1]
        
    if new_x[-1] >= last_x_lim + 5:
        last_x_lim += 5
        ax.set_xlim(last_x_lim, last_x_lim + 5)
    

    return line,

def change_dropdown(*args):
    variable.get()

Options=['']
Options.extend(serial.tools.list_ports.comports())

# GUI Utilisation
root = Tk.Tk()

Tk.Label(root,text="Simulation ECG").pack()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

variable = StringVar(root)
variable.set(Options[0]) #Default option

w=OptionMenu(root, variable, *Options)
w.pack()

variable.trace('w', change_dropdown)


ax = fig.add_subplot(111)
ax.set_xlim(last_x_lim, 5)
ax.set_ylim(-5, 5)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.xaxis.set_tick_params(width=1, top=True)
ax.set_facecolor('black')

line, = ax.plot(0, 0)
ax.get_lines()[0].set_color("xkcd:lime")
ani = animation.FuncAnimation(fig, animate, frames=30, interval=24, repeat=True, blit=True)

Tk.mainloop()