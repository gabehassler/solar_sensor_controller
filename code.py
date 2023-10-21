import os
import time
import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import sys
import microcontroller

import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


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

    # mqtt_client = MQTT.MQTT(
    #     broker="io.adafruit.com",
    #     port=1883,
    #     username=aio_user,
    #     password=aio_key,
    #     socket_pool=pool,
    #     ssl_context=ssl_context,
    # )

    # print(os.getenv("MOSQUITTO_USERNAME"))
    # print(os.getenv("MOSQUITTO_PASSWORD"))
    mosquitto_client = MQTT.MQTT(
        broker="52.89.139.124",
        port=1883,
        username=os.getenv("MOSQUITTO_USERNAME"),
        password=os.getenv("MOSQUITTO_PASSWORD"),
        socket_pool=pool,
        ssl_context=ssl_context,
    )

    # mqtt_client.connect()
    print("A")
    mosquitto_client.connect()
    print("B")

    SENSORS = sensors.setup_sensors()

    while True:
        for i in range(3):
            led.value = True
            time.sleep(i + 1)
            led.value = False
            time.sleep(0.5)
        # mqtt_client.loop()
        mosquitto_client.loop()
        data = sensors.get_sensor_data(SENSORS)

        # for k in data.keys():
        #     feed = aio_user + '/feeds/sensor' + str(sensor_id) + '.' + k
        #     mqtt_client.publish(feed, data[k])
        
        mosquitto_client.publish('solar/sensor' + str(os.getenv('SENSOR_ID')) + '/temppower', 
                                 sensors.prepare_data_mqtt(data))

        for i in range(4):
            led.value = True
            time.sleep(0.5)
            led.value = False
            time.sleep(0.25)
        time.sleep(10)

try:
    log_data()
except Exception as e:
    print("Error:\n", str(e))
    print("Resetting microcontroller in 30 seconds")

    # for i in range(20):
    #     led.value = not led.value
    #     time.sleep(0.5)

    # # write to log to file
    # with open('errors.log', 'a') as f:
    #     f.write('Error:\n')
    #     f.write(str(e))
    #     f.write('\n')

    for i in range(10):
        led.value = not led.value
        time.sleep(1)
    # time.sleep(20)
    # microcontroller.reset()







