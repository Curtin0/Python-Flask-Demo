from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import json
from flask_cors import *

from urllib.parse import quote_plus

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:passowrd@:3306/pmsm1000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%s@127.0.0.1:3306/pmsm1000' % quote_plus('ASIM01@2021.tongye')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

CORS(app, supports_credentials=True)


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


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operate = db.Column(db.String(64), nullable=True)
    socket_client = db.Column(db.String(64), nullable=True)
    socket_client_model = db.Column(db.String(64), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    source = db.Column(db.String(64), nullable=True)
    mode = db.Column(db.String(64), nullable=True)
    level = db.Column(db.String(64), nullable=True)
    rot_speed = db.Column(db.String(64), nullable=True)
    now_time = db.Column(db.DateTime, nullable=True)


class TemRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.BLOB)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    socket_client = db.Column(db.String(64), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(64), nullable=True)
    fault = db.Column(db.String(64), nullable=True)
    source = db.Column(db.String(64), nullable=True)
    mode = db.Column(db.String(64), nullable=True)
    rot_speed = db.Column(db.String(64), nullable=True)
    ntc_temp = db.Column(db.String(64), nullable=True)
    bus_voltage = db.Column(db.String(64), nullable=True)
    u_current = db.Column(db.String(64), nullable=True)
    v_current = db.Column(db.String(64), nullable=True)
    w_current = db.Column(db.String(64), nullable=True)
    run_time = db.Column(db.String(64), nullable=True)
    version = db.Column(db.String(64), nullable=True)
    now_time = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.now())


db.create_all()


@app.route('/record', methods=['POST'])
def record_send():
    data = request.get_data()
    data = json.loads(data)
    print(data)

    now_time = datetime.datetime.now()
    record = Record(operate=data['operate'], socket_client=data['socket_client'],
                    socket_client_model=data['socket_client_model'], address=data['address'],
                    source=data['source'], mode=data['mode'], level=data['level'], rot_speed=data['rot_speed'],
                    now_time=now_time)

    data_list = [0,0,0, int(data['socket_client']), int(data['socket_client_model']),
                 int(data['address']),65,1,0,6, int(data['source']), int(data['mode']),0,
                 int(data['level'])]
    rot_speed = str(data['rot_speed'])
    
    x=int(rot_speed)
    c=int((x-x%100)/256)
    data_list.append(c)
    d=x-c*256
    data_list.append(d)

    print(data_list)
    message = bytes(data_list)
    print(message)

    message_com =message[5:16]

    crcstr = calc_crc(message_com)
    t = crcstr.encode("utf-8")
    x = int(t[2:4], 16)
    y = int(t[4:6], 16)
    data_list.append(x)
    data_list.append(y)
    message = bytes(data_list)

    tem_record = TemRecord(data=message)
    db.session.add(tem_record)
    db.session.add(record)
    db.session.commit()

    return json.dumps({'msg': 'success'})

@app.route('/query', methods=['POST'])
def query_data():
    data = request.get_data()
    data = json.loads(data)
    print(data)
    sql_data = Data.query.filter_by(socket_client=data['socket_client'], address=data['address']).order_by(
        Data.now_time).all()
    if sql_data:
        data = sql_data[-1]
        result_dict = {
            'code': 0,
            'msg': 'success',
            'data': {
                "socket_client": data.socket_client,
                "address": data.address,
                "status": data.status,
                "fault": data.fault,
                "source": data.source,
                "mode": data.mode,
                "rot_speed": data.rot_speed,
                "ntc_temp": data.ntc_temp,
                "bus_voltage": data.bus_voltage,
                "u_current": data.u_current,
                "v_current": data.v_current,
                "w_current": data.w_current,
                "run_time": data.run_time,
                "version": data.version,
                "now_time": data.now_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    else:
        result_dict = {
            'code': 0,
            'msg': 'success',
            'data': None
        }

    #return json.dumps(result_dict)
    return result_dict

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port =80)
