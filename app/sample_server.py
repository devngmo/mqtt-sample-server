
import datetime
import random
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import json, os, utils, time, math
from munch import Munch
from scheduler import PublishScheduler

class SampleServer():
    def __init__(self, host, port, username, password, scenarioEndWillCloseServer = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.keepAlive=60
        self.scheduler : PublishScheduler = None
        self.client = paho.Client(protocol=paho.MQTTv311)
        self.scenarioEndWillCloseServer = scenarioEndWillCloseServer

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("dev/sample-server-config")

    def on_message(self, client, userdata, message):
        # try:
        #     if message.topic == "dev/sample-server-config":
        #         payloadStr = str(message.payload.decode("utf-8"))
        #         jsonModel = json.loads(payloadStr)
        #         if 'PUBLISH_RATE' in jsonModel:
        #             self.publishRate = jsonModel['PUBLISH_RATE']

        # except Exception as ex:
        #     print(ex)
        pass
        
    def on_log(self, client, userdata, level, buf):
        print('log: ', buf)

    def generateSampleDeviceData(self, d):
        data = { 'device_id': d.device_id, 'sample_time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S') }
        for p in d.params:
            data[p] = random.randint(10, 50)
        return data
        
    def useScenario(self, scenarioFileName: str):
        scenario = utils.loadYaml(f".\\scenarios\\{scenarioFileName}.yml")
        print(f"[SERVER] run with scenario: {scenario['title']}")
        self.scheduler = PublishScheduler(self.client, scenario)

    def go(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
    
        if self.username != '' and self.password != '':
            print('Auth: username="%s" password="%s"' % (self.username, self.password))
            self.client.username_pw_set( username=self.username, password=self.password)
            
        else:
            print('Auth: anonymous')

        print('Connect to: host %s:%s...' % (self.host, self.port))
        self.client.connect(self.host, self.port, self.keepAlive)

        # tempSensor = Munch(device_id = 'TS01', params=['TEMP'])
        # lightSensor = Munch(device_id = 'LS01', params=['BRIGHTNESS'])
        # ttsA = Munch(device_id = 'a', platform='tts')
        # devices = [ tempSensor, lightSensor ]

        # print('Publish counter text message to topic: dev/test')
        # print('Publish device data JSON to topic: iot/office')

        DELAY_INTERVAL_SECONDS = 0.1
        self.client.loop_start()

        while True:
            if self.client.is_connected():
                if self.scheduler != None:
                    scenarioEnded = self.scheduler.update(DELAY_INTERVAL_SECONDS * 1000)
                    if scenarioEnded:
                        if self.scenarioEndWillCloseServer:
                            print('----------------------------')
                            print('Scenario ended => Close server')
                            self.client.loop_stop()
                            break
                        else:
                            print('Scenario ended but server still running')
                else:
                    print("ERROR: Scheduler is not created yet!")
                time.sleep(DELAY_INTERVAL_SECONDS)
            else:
                time.sleep(0.1)
                print('xxx')
