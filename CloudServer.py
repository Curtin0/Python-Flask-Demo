import socket
import asyncio
import websockets
import json
import time

# Socket绑定、监听端口
server = socket.socket()
server.bind(('', 20019))
server.listen()

# socke服务端接收数据
# 收到的数据格式 21 41 01 00 1A 00 00 00 02 00 00 00 00 03 02 03 E8 00 28 00 6E 0B B8 0B B8 0B B8 00 00 4E 20 00 01 02 03 86 44


def recv(conn):
    while True:
        # 异常处理 如果检测到丢包则重新接收数据
        data = conn.recv(1024)
        try:
            dataList = list(data)
            # 检测校验码0x8644
            if (dataList[35]) & (dataList[36]):
                print("数据格式正确，HEX为")
                print(data)
                break
            else:
                print("数据格式错误，校验码错误，请确认")
                continue
        except IndexError:
            print("数据格式错误，长度与预期不符")
    return data

# 通信协议解析计算


def Webdata(dataList):
    # 当前时间
    now = time.localtime()
    nowt = time.strftime("%Y-%m-%d-%H:%M:%S", now)

    WebdataList = []
    WebdataList.append(nowt)
    WebdataList.append(dataList[8])  # now
    # 用于前端判定
    '''计算数值
      0 空闲
      1 启动
      2 运行
      3 故障
      4 故障锁死
      5 停机
      '''
    WebdataList.append(dataList[10])  # bug
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
    WebdataList.append(dataList[14])  # modul
    '''计算数值
      0 停机
      1 设置转速
      2 风量等级
      3 电压调速
      '''
    WebdataList.append(dataList[15]*16*16+dataList[16])  # rpm
    WebdataList.append(dataList[17]*16*16+dataList[18])  # ℃
    WebdataList.append(dataList[19]*16*16+dataList[20])  # U
    WebdataList.append(dataList[21]*16*16+dataList[22])  # u
    WebdataList.append(dataList[23]*16*16+dataList[24])  # v
    WebdataList.append(dataList[25]*16*16+dataList[26])  # w
    WebdataList.append(dataList[29]*16*16+dataList[30])  # t
    WebdataList.append(dataList[32]*100+dataList[33]
                       * 10+dataList[34])  # version
    WebdataList.append(dataList[0])  # 添加设备地址
    return WebdataList


# 主函数 循环等待socket客户端发来消息
if __name__ == '__main__':
    while True:
        conn, addr = server.accept()
        while True:
            async def echo(websocket, path):
                while True:
                    data = recv(conn)
                    dataList = list(data)
                    print("数据转换DEC存入数组后为")
                    print(dataList)

                    # 转码json发送数据给前端
                    MessageJson = json.dumps(Webdata(dataList))
                    await websocket.send(MessageJson)
                    await asyncio.sleep(3)

                    # 从前端接收json数据
                    MessageRecive = await websocket.recv()
                    MessageReciveJson = json.loads(MessageRecive)

                    # 打印json解码后的数组
                    print("收到前端数据")
                    print(MessageReciveJson)

                    # dec数据转换hex
                    bytedata = bytes(MessageReciveJson)
                    print(bytedata)

                    # 发送hex格式给Socket客户端
                    conn.send(bytedata)

            start_server = websockets.serve(echo, '', 20020)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
