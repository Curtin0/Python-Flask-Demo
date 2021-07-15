import socket
import asyncio
import websockets
import json
import time

server = socket.socket() 
server.bind(('',20019))
server.listen() 

now = time.localtime()#当前时间
nowt = time.strftime("%Y-%m-%d-%H:%M:%S", now)

def recv(hex):#socke服务端接收数据
    while True:
        data = conn.recv(1024)        
        if data == '':            
            continue
        else:
            break       
    return data
  
while True:
  conn,addr = server.accept()
  
  while True:
      data = recv(hex)
      
      #21 41 01 00 1A 00 00 00 02 00 00 00 00 03 02 03 E8 00 28 00 6E 0B B8 0B B8 0B B8 00 00 4E 20 00 01 02 03 86 44
      
      print(data)
      
      #b'!A\x01\x00\x1a\x00\x00\x00\x02\x00\x00\x00\x00\x00\x02\x03\xe8\x00(\x00n\x0b\xb8\x0b\xb8\x00\x00N \x00\x01\x02\x03\x86D'
      
      dataList = list(data)
      print(dataList)

      #[33, 65, 1, 0, 26,// 0, 0, 0, 2,// 0, 0, 0, 0(第12个),// 0, 2,// 3, 232,// 0, 40, //0, 110(第20个),// 11, 184, //11, 184(24),// 0, 0, 78, 32(第28个), //0, 1, 2, 3(第32个),// 134, 68]
      #[33, 65, 1, 0, 26,   0, 0, 0, 2,   0, 128, 0, 0,        3, 2,    3, 232,   0, 40,   0, 110,           11, 184,    11, 184, 11, 184, 0, 0（28）, 78, 32, 0, 1, 2, 3（34）, 134, 68]
      WebdataList =[]     
      WebdataList.append(nowt)
      WebdataList.append (dataList[8])#now
      '''计算数值 用于前端判定
      0 空闲
      1 启动
      2 运行
      3 故障
      4 故障锁死
      5 停机
      '''
      WebdataList.append(dataList[10])#bug
      '''计算数值
      0 无故障
      1 过压
      2 欠压
      4 过载
      //17 过载锁死
      8 过温
      //32 输出缺项未锁死
      32输出缺项
      //48 输出缺项锁死
      //64 输出短路未锁死
      64 输出短路
      //80 输出短路锁死
      //128 风机堵转未锁死
      //144 风机堵转锁死
      128 风机堵转
      '''
      WebdataList.append(dataList[13])
      '''
      0 未识别
      1 DC11V
      2 DC600V
      3 AC380V
      '''      
      WebdataList.append(dataList[14])#modul
      '''计算数值
      0 停机
      1 设置转速
      2 风量等级
      3 电压调速
      '''
      WebdataList.append(dataList[15]*16*16+dataList[16])#rpm
      WebdataList.append(dataList[17]*16*16+dataList[18])#℃
      WebdataList.append(dataList[19]*16*16+dataList[20])#U
      WebdataList.append(dataList[21]*16*16+dataList[22])#u
      WebdataList.append(dataList[23]*16*16+dataList[24])#v
      WebdataList.append(dataList[25]*16*16+dataList[26])#w
      WebdataList.append(dataList[29]*16*16+dataList[30])#t
      WebdataList.append(dataList[32]*100+dataList[33]*10+dataList[34])#version
      WebdataList.append(dataList[0])#加设备地址
          
      async def echo(websocket, path):        
          while True:
              #发送数据给前端
              MessageJson = json.dumps(WebdataList)
              await websocket.send(MessageJson)
              await asyncio.sleep(3)
              
              #从前端接收数据发给Socket客户端              
              MessageRecive = await websocket.recv()
              MessageReciveJson = json.loads(MessageRecive)
              print(MessageReciveJson)
              #打印json解析后的数组 [34,65,1,0,6,10,3,10,00,70,193]               
              t = bytes(MessageReciveJson)
              print(t)
              #21 41 01 00 06 0a 03 0a 00 46 c1 
              conn.send(t)#发送
   
      start_server = websockets.serve(echo,'',20020)
      asyncio.get_event_loop().run_until_complete(start_server)
      asyncio.get_event_loop().run_forever()        
      if not data:
          print("The connection has been disconnected")
          break
        
  server.close()

