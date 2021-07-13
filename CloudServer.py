import socket
import asyncio
import websockets
import time
import json
import binascii  
import struct
import time

server = socket.socket() 
server.bind(('',20019))
server.listen() 

now = time.localtime()
nowt = time.strftime("%Y-%m-%d-%H:%M:%S", now)

while True:
  conn,addr = server.accept()
  
  while True:
      data = conn.recv(1024)
      conn.send(data)

      #21 41 01 00 1A 00 00 00 02 00 00 00 00 00 02 03 E8 00 28 00 6E 0B B8 0B B8 00 00 4E 20 00 01 02 03 86 44

      dataString = data
      print(dataString)
      
      #b'!A\x01\x00\x1a\x00\x00\x00\x02\x00\x00\x00\x00\x00\x02\x03\xe8\x00(\x00n\x0b\xb8\x0b\xb8\x00\x00N \x00\x01\x02\x03\x86D'
      
      dataList = list(dataString)
      print(dataList)

      #[33, 65, 1, 0, 26,// 0, 0, 0, 2,// 0, 0, 0, 0(12),// 0, 2,// 3, 232(16),// 0, 40, //0, 110(20),// 11, 184, //11, 184(24),// 0, 0, 78, 32(28), //0, 1, 2, 3(32),// 134, 68]

      WebdataList =[]
      
      WebdataList.append(nowt)
      WebdataList.append (dataList[8])#now     
      WebdataList.append(dataList[9]+dataList[10])#bug     
      WebdataList.append(dataList[14])#modul
      
      WebdataList.append(dataList[15]*16*16+dataList[16])#rpm
      WebdataList.append(dataList[17]*16*16+dataList[18])#℃
      WebdataList.append(dataList[19]*16*16+dataList[20])#U
      WebdataList.append(dataList[21]*16*16+dataList[22])#u
      WebdataList.append(dataList[23]*16*16+dataList[24])#v
      WebdataList.append(dataList[25]*16*16+dataList[26])#w
      WebdataList.append(dataList[29]*16*16+dataList[30])#t
      WebdataList.append(dataList[32]*100+dataList[33]*10+dataList[34])#version
          
      async def echo(websocket, path):
        
          while True:
              
              MessageJson = json.dumps(WebdataList)
              await websocket.send(MessageJson)
              await asyncio.sleep(3)
              
      start_server = websockets.serve(echo,'',20020)
      asyncio.get_event_loop().run_until_complete(start_server)
      asyncio.get_event_loop().run_forever()
      
      if not data:
          print("The connection has been disconnected")
          break
        
  server.close()

