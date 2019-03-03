# Pip Modules
import tkinter as Tk
from tkinter import BooleanVar
from tkinter import IntVar
from tkinter import StringVar
from tkinter import OptionMenu

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import serial
from serial import SerialException
import serial.tools.list_ports

# Project Modules
import signals
from server import Server

from queue import Queue

socket_queue = Queue()

server = Server(port=911)
server.start(socket_queue)

root = Tk.Tk()

hr = IntVar(root, value=80)
threshold = IntVar(root, value=20)

position = StringVar(root, value='RIP')

# Take care of plotting
fig = plt.Figure(figsize=(14, 4.5), dpi=100)

new_x = []
new_y = []

last_x = 0
last_x_lim = 0

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
        [x, y] = signals.Default_Line()
    elif position.get() == 'LRA':
        [x, y] = signals.Default_Line()
    elif position.get() == 'IVC':
        [x, y] = signals.Default_Line()
    elif position.get() == 'RV':
        [x, y] = signals.Default_Line()
    elif position.get() == 'RVW':
        [x, y] = signals.Default_Line()
    elif position.get() == 'PA':
        [x, y] = signals.Default_Line()
    else:
        [x, y] = signals.Default_Line()

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
wait_for_update = BooleanVar(root, value=False)
wait_for_position = BooleanVar(root, value=False)

def read_socket():
    if not socket_queue.empty():
        message = socket_queue.get()

        print(message)

        if wait_for_update.get():
            result = [x.strip() for x in message.decode('utf-8').split(',')]

            hr.set(result[0])
            threshold.set(result[1])

            wait_for_update.set(False)
        elif wait_for_position.get():
            position.set(message.decode('utf-8'))
            wait_for_position.set(False)
        else:
            if message == b'update':
                wait_for_update.set(True)
            elif message == b'position':
                wait_for_position.set(True)
            elif message == b'close':
                root.destroy()
        
    root.after(10, read_socket)

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

root.after(10, read_socket)

Tk.mainloop()

server.stop()
