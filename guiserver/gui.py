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
from signals import Signals
from server import Server

from queue import Queue

socket_queue = Queue()

server = Server(port=911)
server.start(socket_queue)

ecg_signals = Signals()

root = Tk.Tk()

hr = IntVar(root, value=80)
threshold = IntVar(root, value=20)

position = StringVar(root, value='RIP')
serial_position = IntVar(root, value='0')

override_position = BooleanVar(root, value=True)

# Take care of plotting
fig = plt.Figure(figsize=(14, 4.5), dpi=100)

new_x = []
new_y = []

last_x = 0
last_x_lim = 0

def animate(i):
    global hr
    global threshold
    global position
    global serial_position
    global override_position
    global last_x
    global last_x_lim
    
    if (override_position.get()):
        [x, y] = ecg_signals.get_signal(position.get(), hr.get())
    else:
        [x, y] = ecg_signals.get_signal(ecg_signals.signal_index[serial_position.get()], hr.get())

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
    global ser
    
    if not variable.get() == '':
        try:
            choice = variable.get().split(' -')
            ser = serial.Serial(choice[0], 9600)
            print('Connection established.')
            root.after(10, read_serial)
        except SerialException as e:
            print('Error: {}'.format(e))

    
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
            override_position.set(True)
        else:
            if message == b'update':
                wait_for_update.set(True)
            elif message == b'start-pos':
                wait_for_position.set(True)
            elif message == b'stop-pos':
                override_position.set(False)
            elif message == b'close':
                root.destroy()
        
    root.after(10, read_socket)

s = 'RIP'
ser = None

def read_serial():
    global s
    global ser
    global serial_position

    if not ser == None:
        try:
            if ser.in_waiting:
                s = ser.read()
                serial_position.set(int(s))
                print(int(s))
            
        except Exception as e:
            print('Error: {}'.format(e))

    root.after(10, read_serial)

Tk.Label(root,text="Simulation ECG").pack()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

variable = StringVar(root)
variable.set(Options[0]) #Default option

w=OptionMenu(root, variable, *Options)
w.pack()

variable.trace('w', change_dropdown)

# ===== ECG Signal Setup
ax = fig.add_subplot(111)
ax.set_xlim(last_x_lim, 5)
ax.set_ylim(-7, 7)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.xaxis.set_tick_params(width=1, top=True)
ax.set_facecolor('black')

line, = ax.plot(0, 0)
ax.get_lines()[0].set_color("xkcd:lime")
ani = animation.FuncAnimation(fig, animate, frames=30, interval=24, repeat=True, blit=True)

# Polling Initialisation
root.after(10, read_socket)

# Start GUI
Tk.mainloop()

# Clean-up
server.stop()
ser.close()