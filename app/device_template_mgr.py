import os, yaml

class DeviceTemplateManager():
    def __init__(self):
        self.templates = []

    def getDeviceTemplateFolder(self):
        return os.path.join(os.getcwd(), 'devices')

    def load(self):
        files = os.listdir(self.getDeviceTemplateFolder())
        for f in files:
            t = self.loadTemplate(os.path.join(self.getDeviceTemplateFolder(), f))
            self.templates = self.templates + [t]
        
    def loadTemplate(self, fp):
        with open(fp, encoding='utf8') as f:
            yamlStr = f.read()
            