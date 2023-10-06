import sys
import json
import os



sys.path.append('./code/')
import pico_wifi as pw
# import wifi_test
import sensors

# sensors.log_to_screen()

pw.connect_wifi()
requests = pw.setup_requests()

data = sensors.get_sensor_data()
url = "https://us-central1-1.gcp.cloud2.influxdata.com:8086/api/v2/write?bucket=solar_power_temp/rp&precision=ns"
measurement = "power_temp"

data = {
    "measurement": measurement,
    "fields": {
        'temp': data['temp'],
        'current': data['current'],
        'voltage': data['voltage'],
        'power': data['power']
    }
}



payload = json.dumps(data)
headers = {"Authorization": "Token " + os.getenv('INFLUXDB_TOKEN')}
print(url)
print(headers)
print(payload)
response = requests.post(url, data=payload, headers=headers)
print(response)

# post to influxdb


# import time