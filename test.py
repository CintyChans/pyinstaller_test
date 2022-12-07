from shapely.geometry import *
import argparse
import numpy as np
import time
from scipy import constants
import paho.mqtt.client as mqtt
import confluent_kafka as kafka
from threading import Thread
parser = argparse.ArgumentParser(description='Demo of argparse')
parser.add_argument('--line', type=int, default=1)

line = LineString([(0, 0), (1, 1)])
print('shapely:',line)

args = parser.parse_args()
if args.line:
    print('argparse:',args.line)

print('numpy:',np.array([1,2,3]))

print('scipy:',constants.pi)

class Recorder():
    def __init__(self):
        super().__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message =self.on_message
        self.client.connect(host="127.0.0.1", port=1883, keepalive=65535)   # 订阅频道
        self.client.subscribe('mqtt',0)
        self.client.loop_start()

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self,client, obj, msg):
       print('mqtt_recieve:',msg.payload)
    
    def close(self):
        self.client.disconnect()

Recorder()

conf = {'bootstrap.servers':'127.0.0.1:9092', 'group.id':f"utc_{time.time()}",'session.timeout.ms': 6000,'auto.offset.reset': 'latest', 'enable.auto.commit': True}
topics ='kafka'
consumer = kafka.Consumer(conf) 
consumer.subscribe([topics])

while 1:         
    msg = consumer.poll(timeout=1.0)   
    try:
        if msg is None:
            continue
        else:
            print('kafka_recieve:',msg.value())
    except Exception as e:
        print(e)
        continue
