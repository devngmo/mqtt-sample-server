import datetime
import random, argparse
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

parser = argparse.ArgumentParser(description='Parse options in command-line')
parser.add_argument('-s', '--scenario', help='Scenario file name in folder .\scenarios')
parser.add_argument('-secs', '--scenarioEndWillCloseServer', help='yes/no')
args = parser.parse_args()

print('----------------------------------------------------------------------------------')
scenarioEndWillCloseServer = args.scenarioEndWillCloseServer == 'yes'
server = SampleServer(host, port, username, password, scenarioEndWillCloseServer)
server.useScenario(args.scenario)
server.go()