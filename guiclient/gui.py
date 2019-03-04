import tkinter as tk
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import Radiobutton
from tkinter import StringVar

from client import Client

client = Client(port=911)

master = tk.Tk("Phantom - Client")

message = StringVar(master)
host = StringVar(master, value='127.0.0.1')

hr = StringVar(master, value=0)
threshold = StringVar(master, value=0)

position = StringVar(master)

def connect():
    client.start()

def send_command():
    client.send_data(message.get())

def send_customisations():
    client.send_data("update")
    client.send_data("{},{}".format(hr.get(), threshold.get()))

def send_position():
    client.send_data("position")
    client.send_data(position.get())

# ============ Connection Space ===============
frame_connection = Frame(master)
frame_connection.pack(pady=5)

Label(frame_connection, text="Hostname").pack(side=tk.LEFT)

entry_hostname = Entry(frame_connection, textvariable=host)
entry_hostname.pack(side=tk.LEFT)

btn_connect = Button(frame_connection, text="Connect", command=connect)
btn_connect.pack(side=tk.LEFT)

# ============ Customisation Space ===============
frame_signal = Frame(master)
frame_signal.pack(pady=5)

Label(frame_signal, text="Heart Rate").grid(row=0, column=0)

entry_hr = Entry(frame_signal, textvariable=hr)
entry_hr.grid(row=0, column=1)

Label(frame_signal, text="Pacing Threshold").grid(row=1, column=0)

entry_threshold = Entry(frame_signal, textvariable=threshold)
entry_threshold.grid(row=1, column=1)

btn_send_customisations = Button(frame_signal, text="Send", command=send_customisations)
btn_send_customisations.grid(row=2, columnspan=2)

# ============ Command Space ===============
frame_command = Frame(master)
frame_command.pack(pady=5)

Label(frame_command, text="Command").pack(side=tk.LEFT)

entry_command = Entry(frame_command, textvariable=message)
entry_command.pack(side=tk.LEFT)

btn_send_command = Button(frame_command, text="Send", command=send_command)
btn_send_command.pack(side=tk.LEFT)

# ============ Position Selection ===============
frame_position = Frame(master)
frame_position.pack(pady=5)

POSITIONS = [
    ("Superior Vena Cava", "SVC"),
    ("High Right Atrium", "HRA"),
    ("Mid Right Atrium", "MRA"),
    ("Low Right Atrium", "LRA"),
    ("Inferior Vena Cava", "IVC"),
    ("Right Ventricle", "RV"),
    ("Right Ventricular Wall", "RVW"),
    ("Pulmonary Artery", "PA"),
    ("Asystole", "RIP"),
]

position.set("SVC")

Label(frame_position, text="Heart Positions").pack()

for button_text, position_value in POSITIONS:
    Radiobutton(frame_position, text=button_text, value=position_value, variable=position).pack()

btn_send_position = Button(frame_position, text="Send", command=send_position)
btn_send_position.pack()

tk.mainloop()

client.stop()
