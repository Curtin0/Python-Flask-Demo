import socket
import asyncio
import websockets
import json
import time

#Socket绑定、监听端口
server = socket.socket() 
server.bind(('',20019))
server.listen() 

#当前时间
now = time.localtime()
nowt = time.strftime("%Y-%m-%d-%H:%M:%S", now)

#socke服务端接收数据
#收到的数据格式 21 41 01 00 1A 00 00 00 02 00 00 00 00 03 02 03 E8 00 28 00 6E 0B B8 0B B8 0B B8 00 00 4E 20 00 01 02 03 86 44
def recv():
    while True:
        data = conn.recv(1024)
        dataList = list(data) 
        #校验接收的数据长度是否符合,校验码0x8644正确则程序继续，否则忽略接收数据。
        if (dataList[35] == 134) & (dataList[36] == 68):
            print("数据格式正确") 
            break
        else:
            print("数据校验码错误，请确认")
            continue       
    return data

#循环等待socket客户端发来的数据  
while True:
  conn,addr = server.accept()
  while True:
      data = recv()     
      dataList=list(data)
      print("存入数组中为")
      print(dataList)     
      
      WebdataList =[]     
      WebdataList.append(nowt)
      WebdataList.append (dataList[8])#now
      #用于前端判定
      '''计算数值
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
      8 过温
      32 输出缺项
      64 输出短路
      128 风机堵转
      '''
      WebdataList.append(dataList[13])
      '''计算数值
      0 未识别
      1 DC 110V
      2 DC 600V
      3 AC 380V
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
      WebdataList.append(dataList[0])#添加设备地址
          
      async def echo(websocket, path):        
          while True:
              #发送数据给前端
              MessageJson = json.dumps(WebdataList)
              await websocket.send(MessageJson)
              await asyncio.sleep(3)
              
              #从前端接收数据             
              MessageRecive = await websocket.recv()
              MessageReciveJson = json.loads(MessageRecive)
              print("收到前端数据")
              print(MessageReciveJson)
              #打印json解析后的数组             
              t = bytes(MessageReciveJson)
              print(t)
              #发送给Socket客户端              
              conn.send(t)
   
      start_server = websockets.serve(echo,'',20020)
      asyncio.get_event_loop().run_until_complete(start_server)
      asyncio.get_event_loop().run_forever()        
      if not data:
          print("The connection has been disconnected")
          break
   #关闭socket连接     
  server.close()