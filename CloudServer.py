from socket import *
from time import ctime
 
HOST = '127.0.0.1'
PORT = 20020
BUFSIZ = 1024
ADDR = (HOST,PORT)
 
tcpSerSock = socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
 
while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connnecting from:', addr)
 
    while True:
   
            
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        #tcpCliSock.send('[%s] %s' %(bytes(ctime(),'utf-8'),data))
        tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
    tcpCliSock.close()
tcpSerSock.close()
