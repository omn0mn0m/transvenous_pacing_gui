import sys
import serial
#import time
from serial import SerialException
import serial.tools.list_ports

print()
ser = None

while ser is None:
    print('Getting available ports...')
    ports = serial.tools.list_ports.comports()
    # List available ports
    for i in range(len(ports)):
        print(str(i+1) + ': ' + ports[i].device)

    # Get selection from user input
    choice = input('Select a bluetooth port: ')
    while int(choice) < 1 or int(choice) > len(ports):
        print('Please input a value between 1 and ' + str(len(ports)))
        choice = input('Select a bluetooth port: ')

    port = ports[int(choice) - 1].device
    print('Connecting to ' + port + '...')
    
     #Connect to serial port
    try:
        ser = serial.Serial(port, 9600)
    except SerialException as e:
        print('Error: {}'.format(e))

    print('Connection established.')

# Send position over serial connection (MC ESP 32)
# Change to interrupts
while ser.is_open:
    
    #if (ser.inWaiting()>0): #bytes waiting to be read from input buffer
        #data_str = ser.read(ser.inWaiting()).decode('ascii') #read bytes and convert to ASCII
        #print(data_str, end='')
    
    #time.sleep(0.0001) #breaks for rest of code to run for 10 ms
    s = ser.read()

    print(s)
