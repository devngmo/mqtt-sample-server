import datetime
import random
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import json, os, utils, time, math
from sample_server import SampleServer
from munch import Munch

print('=============================')
print('MQTT-SAMPLE-SERVER')
print('=============================')

host = utils.getEnvValue('MQTT_HOST', '127.0.0.1')
port = int(utils.getEnvValue('MQTT_PORT', '1883'))
username = utils.getEnvValue('MQTT_USER', '')
password = utils.getEnvValue('MQTT_PASS', '')
publishRate = utils.getEnvValue('PUBLISH_RATE', 30)

print('send { PUBLISH_RATE: 30 } to topic dev/sample-server-config to change publish rate')
print('----------------------------------------------------------------------------------')
server = SampleServer(host, port, username, password, publishRate)
server.go()