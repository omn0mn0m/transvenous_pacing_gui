import tkinter as tk
from tkinter import Button
from tkinter import Entry
from tkinter import StringVar

from client import Client

client = Client(port=911)

master = tk.Tk("Phantom - Client")

message = StringVar(master)
host = StringVar(master)

def connect():
    client.start()

def send_message():
    client.send_data(message.get())

btn_connect = Button(master, text="Connect", command=connect)
btn_connect.pack()

entry_message = Entry(master, textvariable=message)
entry_message.pack()

btn_send = Button(master, text="Send", command=send_message)
btn_send.pack()

tk.mainloop()

client.stop()
