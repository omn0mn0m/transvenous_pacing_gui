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

server = Server(port=25565)
server.start(socket_queue)

ecg_signals = Signals()

root = Tk.Tk()

hr = IntVar(root, value=80)
threshold = IntVar(root, value=20)

position = StringVar(root, value='RIP')
serial_position = IntVar(root, value='0')
hr1=StringVar(root, value='0')

override_position = BooleanVar(root, value=False)

pathway_1 = IntVar(root, value=0)
pathway_2 = IntVar(root, value=0)

# Take care of plotting
fig = plt.Figure(figsize=(14, 4.5), dpi=100,facecolor='k',edgecolor='k')

new_x = [0.0]
new_y = [0.0]

last_x = 0
last_x_lim = 0

position_to_show = 0

def animate(i):
    global new_x
    global new_y
    global last_x
    global last_x_lim
    global position_to_show
    
    if override_position.get():
        [x, y] = ecg_signals.get_signal(position.get(), hr.get())
    else:
        position_index = serial_position.get()

        if position_index == 4:
            position_index = position_index + pathway_1.get()
        elif position_index == 6:
            position_index = position_index + pathway_2.get()
        else:
            position_index = position_index

        print(ecg_signals.signal_index[position_index])

        # if position_to_show <= position_index:
        #     position_to_show = position_index

        # [x, y] = ecg_signals.get_signal(ecg_signals.signal_index[position_to_show], hr.get())
            
        if position_index == 0:
            if position_to_show == 1:
                position_index = 0
            else:
                position_index = position_to_show
        else:
            position_to_show = position_index

        if position_index == 0:
            hr1.set(0)
        else:
            hr1.set(hr.get())

        [x, y] = ecg_signals.get_signal(ecg_signals.signal_index[position_index], hr.get())

    x_val = last_x + x[i]

    if x_val > new_x[-1]:
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
wait_for_pathway_1 = BooleanVar(root, value=False)
wait_for_pathway_2 = BooleanVar(root, value=False)

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
        elif wait_for_pathway_1.get():
            pathway_1.set(int(message.decode('utf-8')))
            print(pathway_1.get())
            wait_for_pathway_1.set(False)
        elif wait_for_pathway_2.get():
            pathway_2.set(int(message.decode('utf-8')))
            print(pathway_2.get())
            wait_for_pathway_2.set(False)
        else:
            if message == b'update':
                wait_for_update.set(True)
            elif message == b'start-pos':
                wait_for_position.set(True)
            elif message == b'stop-pos':
                override_position.set(False)
            elif message == b'chpa1':
                wait_for_pathway_1.set(True)
            elif message == b'chpa2':
                wait_for_pathway_2.set(True)
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
BPM="BPM "
#hr2=str(hr1)
whites="                                  "
Tk.Label(root, text="Simulation ECG",font="Times 30 bold", bg="black",fg="lime green").grid(row=0, column=1)
Tk.Label(root, textvariable=hr1,font='Times 24 bold',bg="black", fg="lime green").grid(row=0, column=3)
Tk.Label(root, text="BPM", font='Times 24 bold', bg="black", fg="lime green").grid(row=0, column=2)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=1)
root.configure(bg="black")

variable = StringVar(root)
variable.set(Options[0]) #Default option

w=OptionMenu(root, variable, *Options)
w.grid(row=2, column=1)

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
