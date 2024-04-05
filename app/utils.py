import re, os, yaml, json
  
regexEmailAddress = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def isValidEmailAddress(text):
    return re.search(regexEmailAddress, text)

def getEnvBool(key, defaultValue):
    if key in os.environ:
        v = ('%s' % os.environ[key]).lower()
        return v == '1' or v == 'true'
    return defaultValue

def getEnvValue(key, defaultValue):
    if key in os.environ:
        return os.environ[key]
    return defaultValue


def loadYaml(fp):
    with open(fp, encoding='utf8') as f:
        text = f.read()
        return yaml.load(text, yaml.SafeLoader)

def loadJson(fp):
    with open(fp, encoding='utf8') as f:
        text = f.read()
        return json.loads(text)

def loadText(fp):
    with open(fp, encoding='utf8') as f:
        return f.read()
        

def writeText(fp, text):
    with open(fp, 'w', encoding='utf8') as f:
        f.write(text)
        f.close()