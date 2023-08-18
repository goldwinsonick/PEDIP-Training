# print("Ports: " + str(["hello", "apel"]))
from serial.tools import list_ports
def printSerialList():
    ports = list_ports.comports()
    for port in ports:
        print(str(port) + "hello")
printSerialList()