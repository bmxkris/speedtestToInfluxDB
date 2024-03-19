import subprocess
import json
from datetime import datetime
from influxdb import InfluxDBClient
from influxDBdeets import USERNAME, PASSWORD, ISTABLE

response = subprocess.Popen('/usr/local/bin/SpeedTest --output json', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
#response = subprocess.Popen('speedtest --json', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

#response = '{"client":{"ip":"143.58.132.124","lat":"51.4964","lon":"-0.1224","isp":"Hyperoptic Ltd."},"servers_online":"10","server":{"name":"St Neots","sponsor":"Ramenatte-IT","distance":"82.1699","latency":"6","host":"ramenatteryan.hopto.org:8080"},"ping":"6","jitter":"0","download":"814111797.877779","upload":"720472764.705206","_":"all ok"}'

speedtest_output = json.loads(response)

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "rpi3.local"
        },
        "fields" : {
            "download": round(int(float(speedtest_output["download"]))/1000000, 2),
            "upload": round(int(float(speedtest_output["upload"]))/1000000, 2),
            "ping": round(float(speedtest_output["ping"]), 2)
        }
    }
]

client = InfluxDBClient('localhost', 8086, USERNAME, PASSWORD, ISTABLE)

client.write_points(speed_data)

dt = datetime.now()
print("Ran successfully at:", dt)
