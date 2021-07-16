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
    print("enter receive")
    while True:
        '读取串口数据'  
        data = serial.read_all().hex()        
        if data == '':            
            continue
        else:
            break       
    return data

if __name__ == '__main__':
    serial = serial.Serial('COM1', 19200, timeout=2)
    if serial.isOpen():
        print("serial open success")
    else:
        print("serial open failed")
    while True:
        '运行函数 读取数据'
        data = recv(serial)       
        
        '向服务器发数据'
        tcpCliSock.send(bytes.fromhex(data))

        '接收来自服务器的回复'
        dataRec = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        
        '将服务端回复发给串口'
        result =serial.write(dataRec)
        print("给串口写入字节数量",result)
              
    tcpCliSock.close()
