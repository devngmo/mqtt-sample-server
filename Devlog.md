# Devlog
Records everything I did while coding this project.

====================================
# You Need: Run CMD or PowerShell as Administrator
====================================
## - Upgrade pip
```
python.exe -m pip install --upgrade pip
```

## - Install Requirements
Requirements: you already install python and pip.

```
pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

## release version 0.0.1
- Features:
    + Publish sample data every 30 seconds ( -e PUBLISH_RATE=30 ) for 2 sample devices: temperature sensor, and light sensor

### * create docker image for version 0.0.1

