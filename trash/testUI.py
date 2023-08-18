import serial
from serial.tools import list_ports
import tkinter as tk

class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.printSerialList()
        self.ser = serial.Serial("COM" + input("COM?"), 115200)

        # Data
        # TargetANG, TargetRPM, CurrANG, CurrRPM, pwmANG, pwmRPM
        self.data = [0,0,0,0,0,0]

    
    def readSerialData(self):
        while(self.ser.readable()):
            recvByte = self.ser.read()

    def printSerialList(self):
        ports = list_ports.comports()
        for port in ports:
            print(port)


root = tk.Tk()
app = App(root)
app.mainloop()