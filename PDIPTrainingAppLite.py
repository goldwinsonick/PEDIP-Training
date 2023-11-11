import tkinter as tk
from serial.tools import list_ports
import pandas as pd

class DataManager():
    def __init__(self, path):
        self.path = path
        self.df = pd.read_csv(path)

        self.dist = 0
        self.rpm = 0
        self.ang = 0
        self.success = 0

    def getRow(self):
        return [self.dist, self.rpm, self.ang, self.success]

    def addRow(self):
        newRow = pd.DataFrame([{"dist":self.dist, "rpm":self.rpm, "ang":self.ang, "success":self.success}])
        self.df = pd.concat([self.df, newRow], ignore_index=True)
        self.df.to_csv(self.path, index=False)

class App(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.dm = DataManager("data/data.csv")

        self.root.geometry("1280x720")
        self.root.title("HEHEHE")
        # self.root.configure(bg="red")
        self.root.state('zoomed')
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Setter
        self.setDataEntry = tk.Entry(self.root, font=("Consolas", 50, "bold"))
        self.setDataEntry.grid(row=0, column=0, sticky="news")

        # Buttons
        self.addDataFrame = tk.Frame(self.root, bg="#fff")
        self.addDataFrame.grid(row=1, column=0, sticky="news")
        self.addDataFrame.rowconfigure(0, weight=1)
        self.addDataFrame.rowconfigure(1, weight=1)
        self.addDataFrame.rowconfigure(2, weight=1)
        self.addDataFrame.columnconfigure(0, weight=1)
        self.addDataFrame.columnconfigure(1, weight=1)

        self.updateBtn = tk.Button(self.addDataFrame, text="UPDATE", bg="#ffba4a", font=("Consolas", 20, "bold"), command= self.updateData)
        self.addBtn = tk.Button(self.addDataFrame, text="ADD", bg="#a933e8", font=("Consolas", 20, "bold"), command=self.dm.addRow)
        self.inBtn = tk.Button(self.addDataFrame, text="IN", bg="#b3ff9c", font=("Consolas", 20, "bold"), command=lambda:self.updateSuccess(1))
        self.outBtn = tk.Button(self.addDataFrame, text="OUT", bg="#db4540", font=("Consolas", 20, "bold"), command=lambda:self.updateSuccess(0))
        self.closeBtn = tk.Button(self.addDataFrame, text="CLOSE", bg="#a933e8", font=("Consolas", 20, "bold"), command=lambda:self.updateSuccess(0.5))
        self.dataDisplayStrVar = tk.StringVar()
        self.dataDisplay = tk.Label(self.addDataFrame, textvariable=self.dataDisplayStrVar,font=("Consolas", 10))
        self.updateBtn.grid(row=0, column=0, sticky="news")
        self.addBtn.grid(row=1, column=0, sticky="news")
        self.inBtn.grid(row=0, column=1, sticky="news")
        self.outBtn.grid(row=1, column=1, sticky="news")
        self.closeBtn.grid(row=2, column=1, sticky="news")
        self.dataDisplay.grid(row=2, column=0, sticky="news")

        self.data = [69,69,69]
        self.updateClock = 200
    
    def updateData(self):
        temp = self.setDataEntry.get().split(" ")
        for i in range(len(temp)):
            self.data[i] = float(temp[i])
        self.dm.dist = self.data[0]
        self.dm.rpm = self.data[1]
        self.dm.ang = self.data[2]
        self.updateDataDisplay()
    
    def updateSuccess(self, val):
        self.dm.success = val
        self.updateDataDisplay()
    
    def updateDataDisplay(self):
        temp = ""
        temp2 = self.dm.getRow()
        temp3 = ["dist", "rpm", "angle", "success"]
        for i in range(len(temp2)):
            temp += temp3[i] + ": " + str(temp2[i]) + "\n"
        self.dataDisplayStrVar.set(temp)

    
        
root = tk.Tk()
app = App(root)
app.mainloop()