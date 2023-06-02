import argparse
import paho.mqtt.client as mqtt
import ips_blink_rx_pb2
import yaml,joblib
import subprocess,json
from sklearn.ensemble import RandomForestRegressor
# ["fp_index","fp_to_peak","mc","signal_power_diff"]
_mean=[734.28521653 , 10.60303173  , 0.74006788  , 8.87674453]
_var= [1.36714210e+02 ,2.32926236e+02 ,6.97745667e-02 ,2.98554498e+01]
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
anchor_id=config["anchors"]

los=dict()

def init():
    for anchor,id in anchor_id.items():
        los[id]=None

class client():
    def __init__(self,mq_addr,tag):
        host=mq_addr.split(":")[0]
        port=int(mq_addr.split(":")[1]) 
        self.tagid=tag
        self.localclient=mqtt.Client()
        self.localclient.connect("127.0.0.1",1883,60)
        self.localclient.reconnect_delay_set(5)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message =self.on_message
        self.client.connect(host=host, port=port, keepalive=60)   # 订阅频道
        self.client.reconnect_delay_set(5)
        self.ips_blink_rx=ips_blink_rx_pb2.BlinkRxDataMsg()
        self.model=joblib.load("model.joblib")
        self.localclient.loop_start()
        self.client.loop_forever()

    def on_connect(self,client, userdata, flags, rc):
        self.client.subscribe('ips_blink_rx',0)
        print("Connected with result code " + str(rc))

    def on_message(self,client, obj, msg):
       init()
       self.ips_blink_rx.ParseFromString(msg.payload)
       if self.ips_blink_rx.tag_id == self.tagid:
            for anchor in self.ips_blink_rx.rx_infos:
                try:
                    if anchor in anchor_id.keys():
                        mc=self.ips_blink_rx.rx_infos[anchor].quality.mc
                        fp_to_peak=self.ips_blink_rx.rx_infos[anchor].quality.fp_to_peak
                        fp_index=self.ips_blink_rx.rx_infos[anchor].quality.fp_index
                        signal_power_diff=self.ips_blink_rx.rx_infos[anchor].quality.rssi_rx-self.ips_blink_rx.rx_infos[anchor].quality.rssi_fp
                        los_scale=[[(fp_index-_mean[0]/_var[0]),(fp_to_peak-_mean[1]/_var[1]),(mc-_mean[2]/_var[2]),(signal_power_diff-_mean[3]/_var[3])]]
                        los[anchor_id[anchor]]=self.model.predict(los_scale)[0]
                except Exception as e:
                   print(e)
            self.localclient.publish("los",json.dumps(los),0)
    def close(self):
        self.client.disconnect()

parser = argparse.ArgumentParser(description='los esitimator')
parser.add_argument('--mq_addr', type=str,default="192.168.0.120:1883",action="store",
                    help='mqtt broker address')
parser.add_argument('--tag',type=int,default=14696083070419630555,action="store",
                    help='Specifies the tag sequence number to observe.')

args = parser.parse_args()

process = subprocess.Popen(['powershell.exe', '-Command', config["mqtt_waveform"] + " --topics los"],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True)


client(args.mq_addr,args.tag)