import serial
from time import sleep
from socket import *
import binascii  
import struct

#HOST = '112.74.182.249'
HOST = 'localhost'
PORT = 20019
BUFSIZ =1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

def recv(serial):
    while True:
        data = serial.read_all().decode()  # str
        #data =str(self.Read_Size(40))
        if data == '':
            continue
        else:
            break
        sleep(0.2)
    return data

if __name__ == '__main__':
    serial = serial.Serial('COM2', 19200, timeout=0.5)
    if serial.isOpen():
        print("serial open success")
    else:
        print("serial open failed")
    while True:
        data = recv(serial)
        #print(data)  # str
        
        
        
        tcpCliSock.send(data.encode())
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            berak       
        print(data.decode('utf-8'))
        #com = serial.Serial('COM1', 19200)
        #successbytes = com.write(data.decode('utf-8'))
        #print (successbytes)
        
    tcpCliSock.close()
        
