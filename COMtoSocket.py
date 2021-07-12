import serial
from time import sleep
from socket import *

HOST = '112.74.182.249'
PORT = 20019
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


def recv(serial):
    while True:
        data = serial.read_all().decode("utf-8","ignore")
        if data == '':
            continue
        else:
            break
    sleep(2)
    return data

if __name__ == '__main__':
    serial = serial.Serial('COM2', 19200, timeout=2)
    if serial.isOpen():
        print("serial open success")
    else:
        print("serial open failed")
    while True:
        data = recv(serial)      
        tcpCliSock.send(data.encode('utf-8'))
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break       
        print(data.decode('utf-8'))
        
    tcpCliSock.close()
