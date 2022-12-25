from shapely.geometry import *
import argparse
import numpy as np
import time
from scipy import constants
import paho.mqtt.client as mqtt
import confluent_kafka as kafka
from test_pb2 import *

class test_mqtt():
    def __init__(self):
        super().__init__()
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message =self.on_message
            self.client.connect(host="127.0.0.1", port=1883, keepalive=10)   # 订阅频道
            self.client.subscribe('mqtt',0)
            self.client.loop_start()
        except Exception as e:
            print(e)

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self,client, obj, msg):
       print('mqtt_recieve:',msg.payload)
    
    def close(self):
        self.client.disconnect()

def test_proto():
    person=MsgPerson()
    person.id=1
    print(person.id)
    return person
def test_argparse():
    parser = argparse.ArgumentParser(description='Demo of argparse')
    parser.add_argument('--line', type=int, default=1)
    args = parser.parse_args()
    if args.line:
            print('argparse:',args.line)
    print(args.line)
    return args.line

def test_shapely():
    line = LineString([(0, 0), (1, 1)])
    print(line)
    return line

def test_numpy():
    a=np.array([1,2,3])
    print(a)
    return a
def test_scipy():
    p=constants.pi
    print(p)
    return p

def test_kafka():
    try:
        conf = {'bootstrap.servers':'127.0.0.1:9092', 'group.id':f"utc_{time.time()}",'session.timeout.ms': 6000,'auto.offset.reset': 'latest', 'enable.auto.commit': True} 
        topics ='kafka'
        consumer = kafka.Consumer(conf) 
        consumer.subscribe([topics])
        msg = consumer.poll(timeout=1.0) 
        while 1:         
            msg = consumer.poll(timeout=1.0)   
            try:
                if msg is None:
                    continue
                else:
                    print('kafka_recieve:',msg.value())
            except Exception as e:
                print(e)
                break
    except Exception as e:
        print(e)
          
if __name__=='__main__':
    test_proto()
    test_argparse()
    test_numpy()
    test_scipy()
    test_shapely()
    test_mqtt()
    test_kafka()
