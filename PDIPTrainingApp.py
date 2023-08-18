import tkinter as tk
import serial
from serial.tools import list_ports
from threading import Thread

class Ser():
    def __init__(self):
        self.ser = serial.Serial()
        self.START_BYTE = b'#'
        self.STOP_BYTE = b'$'
        self.bufferByte = bytearray()
        self.loss_count = 0

    def getPortLists(self):
        ports = list_ports.comports()
        return ports

    def configureSerial(self, port, baudrate):
        self.ser.port = port
        self.ser.baudrate = baudrate

    def calcChecksum(self, byteArr):
        checksum = 0
        for byte in byteArr:
            checksum ^= byte
        return checksum

    def readSerial(self):
        while(self.ser.inWaiting() > 5):
            recvByte = self.ser.read()
            if(recvByte == self.START_BYTE):
                self.bufferByte.clear()
            elif(recvByte == self.STOP_BYTE):
                # Checksum
                recvChecksum = self.bufferByte[-1]
                self.bufferByte = self.bufferByte[:-1]
                if(recvChecksum == self.calcChecksum(self.bufferByte)):
                    return self.bufferByte.decode("utf-8")
                else:
                    self.loss_count += 1
            else:
                self.bufferByte += recvByte
        return None

class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.ser = Ser()

        self.root.geometry("1280x720")
        self.root.configure(bg="#ffffff")
        # self.root.attributes('-fullscreen', True)
        self.root.state('zoomed')

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=5)
        self.root.rowconfigure(0, weight=1)

        self.leftFrame = tk.Frame(self.root, bg="#fff")
        self.leftFrame.grid(row=0, column=0, sticky="news")
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=10)
        self.root.rowconfigure(2, weight=10)
        self.rightFrame = tk.Frame(self.root, bg="#fff")
        self.rightFrame.grid(row=0, column=0, sticky="news")

        # Port
        self.portFrame = tk.Frame(self.root, bg="#eee")
        self.portFrame.grid(row=0, column=0, sticky="news")
        self.portListStrVar = tk.StringVar()
        self.portList = tk.Label(self.portFrame, textvariable=self.portListStrVar, justify="left")
        self.refreshPort()
        self.portList.pack()
        self.portLabel = tk.Label(self.portFrame, text="Port: ")
        self.portLabel.pack()
        self.portEntry = tk.Entry(self.portFrame)
        self.portEntry.pack()
        self.portButton = tk.Button(self.portFrame, text="Refresh", command=self.refreshPort)
        self.portButton.pack()
        self.portButton = tk.Button(self.portFrame, text="Submit", command=self.submitPort)
        self.portButton.pack()

        # Data
        self.dataFrame = tk.Frame(self.root, bg="#ddd")
        self.dataFrame.grid(row=1, column=0, sticky="news")
        self.dataFrame.rowconfigure(0, weight=1)
        self.dataFrame.rowconfigure(1, weight=10)
        self.dataFrame.rowconfigure(2, weight=1)
        self.dataFrame.columnconfigure(0, weight=2)
        self.dataFrame.columnconfigure(1, weight=10)
        self.dataFrame.columnconfigure(2, weight=2)
        self.dataStrVar = tk.StringVar()
        self.dataLabel = tk.Label(self.dataFrame, textvariable=self.dataStrVar, bg="#fff", anchor="w", justify="left", font=("Consolas", 20))
        self.dataLabel.grid(row=1, column=1, sticky="news")
        # self.dataLabel.grid_propagate(0)

        # Buttons
        self.addDataFrame = tk.Frame(self.root, bg="red")
        self.addDataFrame.grid(row=2, column=0, sticky="news")
        self.addDataFrame.rowconfigure(0, weight=1)
        self.addDataFrame.rowconfigure(1, weight=1)
        self.addDataFrame.columnconfigure(0, weight=1)
        self.addDataFrame.columnconfigure(1, weight=1)

        self.addBtn = tk.Button(self.addDataFrame, text="ADD", bg="#ffba4a", font=("Consolas", 20, "bold") )
        self.inBtn = tk.Button(self.addDataFrame, text="IN", bg="#b3ff9c", font=("Consolas", 20, "bold"))
        self.outBtn = tk.Button(self.addDataFrame, text="OUT", bg="#db4540", font=("Consolas", 20, "bold"))
        self.delBtn = tk.Button(self.addDataFrame, text="DEL", bg="#a933e8", font=("Consolas", 20, "bold"))
        self.addBtn.grid(row=0, column=0, sticky="news")
        self.inBtn.grid(row=0, column=1, sticky="news")
        self.outBtn.grid(row=1, column=1, sticky="news")
        self.delBtn.grid(row=1, column=0, sticky="news")

        self.data = []
        self.updateClock = 200

    def updateDataLabel(self):
        recvData = self.ser.readSerial()
        if(recvData != None):
            # Data Parser
            self.dataVarNames = ["targetANG", "targetRPM", "currANG", "currRPM", "pwmANG", "pwmRPM"]
            self.data = recvData.split()
            temp = ""
            for i in range(len(self.data)):
                if(i < len(self.dataVarNames)):
                    temp += self.dataVarNames[i]
                else:
                    temp += "data[" + str(i) + "]"
                temp += " = " + str(self.data[i])
                temp+="\n"
                    
            self.dataStrVar.set(temp) 
        self.root.after(self.updateClock, self.updateDataLabel)

    def refreshPort(self):
        temp = "Ports:\n"
        for port in self.ser.getPortLists():
            temp += str(port)
            temp += "\n"
        self.portListStrVar.set(temp)

    def submitPort(self):
        self.ser.ser.close()
        self.ser.configureSerial(self.portEntry.get(), 115200)
        self.ser.ser.open()
        self.updateDataLabel()
    
        
root = tk.Tk()
app = App(root)
app.mainloop()