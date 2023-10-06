import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import sys
import microcontroller
import storage


sys.path.append('./code/')
import pico_wifi as pw
import sensors

def log_data():

    pw.connect_wifi()
    # requests = pw.setup_requests()
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()


    aio_user = os.getenv('AIO_USERNAME')
    aio_key = os.getenv('AIO_KEY')
    sensor_id = os.getenv('SENSOR_ID')

    mqtt_client = MQTT.MQTT(
        broker="io.adafruit.com",
        port=1883,
        username=aio_user,
        password=aio_key,
        socket_pool=pool,
        ssl_context=ssl_context,
    )
    assert 1 == 2

    mqtt_client.connect()

    SENSORS = sensors.setup_sensors()

    while True:
        mqtt_client.loop()
        data = sensors.get_sensor_data(SENSORS)

        for k in data.keys():
            feed = aio_user + '/feeds/sensor' + str(sensor_id) + '.' + k
            mqtt_client.publish(feed, data[k])
        time.sleep(60)

try:
    log_data()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 10 seconds")
    # write to log to file
    with open('errors.log', 'a') as f:
        f.write(str(e))
        f.write('\n')
    time.sleep(10)
    microcontroller.reset()


