import serial
from serial.tools import list_ports

def printSerialList():
    ports = list_ports.comports()
    for port in ports:
        print(port)
printSerialList()
port = "COM"+input("COM:")
baudrate = 115200
ser = serial.Serial(port, baudrate)

while(1):
    x = ser.read()
    print(x, end=" ")
    print(x.decode("utf-8"))
    if(x.decode("utf-8") == "$"):
        print("he")