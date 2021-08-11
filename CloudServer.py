import socket
from datetime import datetime
from app import db, Data
from db import MyDB
from threading import Thread

# Socket绑定、监听端口
server = socket.socket()
server.bind(('', 20019))
server.listen(5)


# CRC校验算法


def calc_crc(bytedata):
    data = bytearray(bytedata)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))


# socke服务端接收数据

def recv(conn):
    print('recv')
    try:
        conn.settimeout(3)
        # 异常处理 如果检测到丢包则重新接收数据
        data = conn.recv(1024)
        # CRC计算 b c为示例0x8B7D拆分转换十进制 即139和125
        checkdata = data[5:48]
        crcrecv = calc_crc(checkdata)
        a = crcrecv.encode("utf-8")
        b = int(a[2:4], 16)
        c = int(a[4:6], 16)
        if data:
            try:
                dataList = list(data)
                if (dataList[48] == b) and (dataList[49] == c):
                #if (dataList[40]) and (dataList[41]):
                    print("数据格式正确，HEX为:", data)
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(str(data.hex()))
                    return dataList
                else:
                    print("数据格式错误，校验码错误，请确认")
                    return False
            except IndexError:
                print("数据格式错误，长度与预期不符")
                return False
        else:
            return 404
    except socket.timeout as e:
        print(e)
        return False


def transfer_data(dataList):
    data_dict = {}
    status_dict = {0: '空闲', 1: '启动', 2: '运行', 3: '故障', 4: '故障锁死', 5: '停机'}
    fault_dict = {0: '无故障', 1: '过压', 2: '欠压', 4: '过载', 8: '过温', 32: '输出缺项', 64: '输出短路', 128: '风机堵转'}
    source_dict = {0: '未识别', 1: 'DC 110v', 2: 'DC:600V', 3: 'AC 380v'}
    mode_dict = {0: '停机', 1: '设置转速', 2: '风量等级', 3: '电压调速'}

    status = status_dict.get(dataList[13], '数据错误')
    data_dict.update({'status': status})

    fault = fault_dict.get(dataList[15], '数据错误')
    data_dict.update({'fault': fault})

    source = source_dict.get(dataList[18], '数据错误')
    data_dict.update({'source': source})

    mode = mode_dict.get(dataList[19], '数据错误')
    data_dict.update({'mode': mode})

    data_dict.update({'socket_client': dataList[3]})
    data_dict.update({'rot_speed': dataList[20] * 16 * 16 + dataList[21]})
    data_dict.update({'ntc_temp': dataList[22] * 16 * 16 + dataList[23]})
    data_dict.update({'bus_voltage': dataList[24] * 16 * 16 + dataList[25]})
    data_dict.update({'u_current': dataList[26] * 16 * 16 + dataList[27]})
    data_dict.update({'v_current': dataList[28] * 16 * 16 + dataList[29]})
    data_dict.update({'w_current': dataList[30] * 16 * 16 + dataList[31]})
    data_dict.update({'run_time': dataList[42] * 16 * 16 + dataList[43]})
    data_dict.update({'version': dataList[45] * 100 + dataList[46] * 10 + dataList[47]})
    data_dict.update({'address': dataList[5]})

    print(data_dict)
    print(dataList)
    return data_dict


def send_socket(conn):
    my_db = MyDB()
    sql = "select * from tem_record"
    temp_records = my_db.runSql(sql)
    if temp_records:
        conn.send(temp_records[0][1])
        sql2 = 'DELETE FROM tem_record WHERE id= {0}'.format(temp_records[0][0])
        my_db.runSql(sql2)

if __name__ == '__main__':
    while True:
        try:
            conn, address = server.accept()
            i = 0
            while True:
                try:
                    i += 1
                    print(i)
                    send_socket(conn)
                    data_list = recv(conn)
                    if data_list:
                        if data_list == 404:
                            print('客户端断开连接')
                            break
                        else:
                            data_dict = transfer_data(data_list)
                            data = Data(socket_client=data_dict['socket_client'], address=data_dict['address'],
                                        version=data_dict['version'],
                                        run_time=data_dict['run_time'],
                                        w_current=data_dict['w_current'], v_current=data_dict['v_current'],
                                        u_current=data_dict['u_current'], bus_voltage=data_dict['bus_voltage'],
                                        ntc_temp=data_dict['ntc_temp'], rot_speed=data_dict['rot_speed'],
                                        mode=data_dict['mode'],
                                        source=data_dict['source'], fault=data_dict['fault'],
                                        status=data_dict['status'], now_time=datetime.now())
                            db.session.add(data)
                            db.session.commit()
                            print('插入数据成功')

                except Exception as e:
                    print(str(e))
                    break
        except Exception as e:
            print(str(e))
            continue
# def main():
#     while True:
#         conn, address = server.accept()
#         i = 0
#         while True:
#             i += 1
#             print(i)
#             send_socket(conn)
#             data_list = recv(conn)
#             if data_list:
#                 if data_list == 404:
#                     print('客户端断开连接')
#                     break
#                 else:
#                     data_dict = transfer_data(data_list)
#                     data = Data(socket_client=data_dict['socket_client'], address=data_dict['address'],
#                                 version=data_dict['version'],
#                                 run_time=data_dict['run_time'],
#                                 w_current=data_dict['w_current'], v_current=data_dict['v_current'],
#                                 u_current=data_dict['u_current'], bus_voltage=data_dict['bus_voltage'],
#                                 ntc_temp=data_dict['ntc_temp'], rot_speed=data_dict['rot_speed'],
#                                 mode=data_dict['mode'],
#                                 source=data_dict['source'], fault=data_dict['fault'],
#                                 status=data_dict['status'], now_time=datetime.now())
#                     db.session.add(data)
#                     db.session.commit()
#                     print('插入数据成功')


# threads = []
# for i in range(5):
#     t = Thread(target=main)
#     t.setDaemon(True)
#     threads.append(t)

# if __name__ == '__main__':
#     for i in range(5):
#         t = Thread(target=main())
#         t.start()
#     for i in range(5):
#         threads[i].join()
