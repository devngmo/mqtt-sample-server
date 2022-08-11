
import datetime
import random
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import json, os, utils, time, math
from munch import Munch

class SampleServer():
    def __init__(self, host, port, username, password, publishRate):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.publishRate = publishRate
        self.keepAlive=60

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("dev/sample-server-config")

    def on_message(self, client, userdata, message):
        try:
            if message.topic == "dev/sample-server-config":
                payloadStr = str(message.payload.decode("utf-8"))
                jsonModel = json.loads(payloadStr)
                if 'PUBLISH_RATE' in jsonModel:
                    self.publishRate = jsonModel['PUBLISH_RATE']

        except Exception as ex:
            print(ex)
        
    def on_log(self, client, userdata, level, buf):
        print('log: ', buf)

    def generateSampleDeviceData(self, d):
        data = { 'device_id': d.device_id, 'sample_time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') }
        for p in d.params:
            data[p] = random.randint(10, 50)
        return data
        
    def go(self):
        client = paho.Client(protocol=paho.MQTTv311)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log
    
        if self.username != '' and self.password != '':
            print('Auth: username="%s" password="%s"' % (self.username, self.password))
            client.username_pw_set( username=self.username, password=self.password)
            
        else:
            print('Auth: anonymous')

        print('Connect to: host %s:%s...' % (self.host, self.port))
        client.connect(self.host, self.port, self.keepAlive)

        tempSensor = Munch(device_id = 'TS01', params=['TEMP'])
        lightSensor = Munch(device_id = 'LS01', params=['BRIGHTNESS'])
        devices = [ tempSensor, lightSensor ]

        print('Publish counter text message to topic: dev/test')
        print('Publish device data JSON to topic: iot/office')

        counter = 1
        client.loop_start()
        while True:
            if client.is_connected():
                client.publish('dev/test', payload= 'counter %d' % counter)
                for d in devices:
                    client.publish('iot/office', payload= json.dumps(self.generateSampleDeviceData(d)))
                counter = counter + 1
                time.sleep(self.publishRate)
            else:
                time.sleep(1)

