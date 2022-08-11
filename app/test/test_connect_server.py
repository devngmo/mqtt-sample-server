import json
import paho.mqtt.client as paho

print('=============================')
print('TEST CONNECT SERVER')
print('=============================')

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("dev/test")

def on_message(client, userdata, message):
    payloadStr = str(message.payload.decode("utf-8"))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("message payload received=" , payloadStr)

def on_log(client, userdata, level, buf):
    print('log: ', buf)

client = paho.Client(protocol=paho.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log

client.username_pw_set( username='tester', password='12345')
client.connect('127.0.0.1', 1883, 50)
client.publish('dev/test', payload='hello')

client.loop_forever()
