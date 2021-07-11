import socket
import asyncio
import websockets
import time
import json
import binascii  
import struct

server = socket.socket() 
server.bind(("localhost",20019)) 
server.listen() 

while True:
  conn,addr = server.accept()
  
  while True:
      data = conn.recv(1024)
      conn.send(data)

      data1 = bytes.decode(data)
      data2 = list(data1)
      
      async def echo(websocket, path):
        
          while True:
              message = json.dumps(data2)
              await websocket.send(message)
              await asyncio.sleep(3)
              
      start_server = websockets.serve(echo,'localhost',8080)
      asyncio.get_event_loop().run_until_complete(start_server)
      asyncio.get_event_loop().run_forever()
      
      if not data:
          print("The connection has been disconnected")
          break
        
  server.close()
