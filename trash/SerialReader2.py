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

START_BYTE = b'#'
STOP_BYTE = b'$'
def calcChecksum(byteArr):
    checksum = 0
    for byte in byteArr:
        checksum ^= byte
    return checksum

bufferByte = bytearray()
loss_count = 0
def readSerial():
    global bufferByte, loss_count
    while(ser.inWaiting() > 5):
        recvByte = ser.read()
        if(recvByte == START_BYTE):
            bufferByte.clear()
        elif(recvByte == STOP_BYTE):
            # Checksum
            recvChecksum = bufferByte[-1]
            bufferByte = bufferByte[:-1]
            if(recvChecksum == calcChecksum(bufferByte)):
                return bufferByte.decode("utf-8")
            else:
                loss_count += 1
        else:
            bufferByte += recvByte
    return None

while(1):
    temp = readSerial()
    if(temp != None):
        print(temp)
        print(loss_count)