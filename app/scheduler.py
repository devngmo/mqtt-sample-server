import utils, json
from datetime import datetime, timezone
import paho.mqtt.client as paho


class PublishScheduler:
    def __init__(self, mqttClient: paho.Client, scenario: dict):
        self.mqttClient = mqttClient
        self.scenario = scenario
        self.stepIndex = 0
        self.msPassed = 0
        self.loopCounter = 0

        scheduleSteps = self.scenario['schedule']
        print("Setup Scheduler:")
        print(f"  - {len(scheduleSteps)} Steps")

    def update(self, msPassed: int):
        
        scheduleSteps = self.scenario['schedule']
        if self.stepIndex >= len(scheduleSteps):
            return True
        
        self.msPassed += msPassed
        currentStep = scheduleSteps[self.stepIndex]
        stepType = currentStep['type']
        # print(f"Step [{self.stepIndex}] type {stepType} time={self.msPassed}")
        if stepType == 'loop_publish':
            self.updateForLoopPublish(currentStep)
        
        return False
    
    def publish(self, topic: str, payload):
        print("[SCHEDULER] publish topic=[{topic}]")
        print("payload:")
        print(payload)
        if isinstance(payload, str):
            self.mqttClient.publish(topic, payload=payload)
        else:
            self.mqttClient.publish(topic, payload=json.dumps(payload))
            
    def updateForLoopPublish(self, step: dict):
        delay = step['delay']
        deviceId = step['device']
        sampleId = step['sample']
        topic = step['topic']
        stepLimitCounter = step['counter']
        # print(f"device={deviceId} sample={sampleId} topic={topic} stepLimitCounter={stepLimitCounter}")
        
        if delay <= self.msPassed:
            sampleJson = utils.loadJson(f"devices\\{deviceId}\\samples\\{sampleId}.json")
            self.overrideVariables(sampleJson)
            self.publish(topic, sampleJson)
            self.loopCounter += 1
            if self.loopCounter >= stepLimitCounter and stepLimitCounter > 0:
                self.stepIndex += 1
                print(f"loop {self.loopCounter} > {stepLimitCounter} => Next step = {self.stepIndex}")
            else:
                print(f"loopCounter = {self.loopCounter}")
            self.msPassed = 0

    def overrideVariables(self, model: dict):
        for key, value in model.items():
            if value == "@UTC_ISO_TIME":
                model[key] = datetime.now(timezone.utc).isoformat()
            elif isinstance(value, dict):
                self.overrideVariables(value)
            elif isinstance(value, list) or isinstance(value, tuple):
                for x in value:
                    self.overrideVariables(x)