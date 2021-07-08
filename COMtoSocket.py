import serial
from time import sleep
from socket import *
import binascii  
import struct

HOST = 'localhost'
PORT = 20019
BUFSIZ =1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

def recv(serial):
    while True:
        data = serial.read_all().decode("gbk","ignore")
        if data == '':
            continue
        else:
            break
        sleep(0.2)
    return data

if __name__ == '__main__':
    serial = serial.Serial('COM3', 19200, timeout=1)
    if serial.isOpen():
        print("serial open success")
    else:
        print("serial open failed")
    while True:
        data = recv(serial)      
        tcpCliSock.send(data.encode('utf-8',"ignore"))
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            berak       
        print(data.decode('utf-8',"ignore"))
        
    tcpCliSock.close()
        
