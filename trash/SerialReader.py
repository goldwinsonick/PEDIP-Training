import serial
from serial.tools import list_ports
import time
# import tkinter

def printSerialList():
    ports = list_ports.comports()
    for port in ports:
        print(port)

printSerialList()
port = "COM"+input("COM:")
baudrate = 115200

START_BYTE = "#"
STOP_BYTE = "$"

ser = serial.Serial(port, baudrate)
# def readSerial():
#     recievedBytes = ser.read()
#     recieved = recievedBytes.decode("utf-8")
#     return recieved
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum


# MAIN
msg = ""
while(1):
    while(ser.readable()):
        x = ser.read().decode("utf-8")
        if(x == START_BYTE):
            msg = ""
        elif(x == STOP_BYTE):
            print(msg)
        else:
            msg+=x


        
            