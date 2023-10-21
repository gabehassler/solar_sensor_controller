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

def blink(t_on, t_off, n):
    for i in range(n):
        led.value = True
        time.sleep(t_on)
        led.value = False
        time.sleep(t_off)


def log_data():

    blink(1, 0.5, 3)
    for i in range(10):
        try:
            print("connecting to wifi...")
            pw.connect_wifi()
            print("connected")
        except:
            time.sleep(3)
    
    # requests = pw.setup_requests()
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()

    blink(0.5, 0.25, 3)


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
    mosquitto_client.connect()

    blink(1, 0.5, 2)

    SENSORS = sensors.setup_sensors()

    blink(0.5, 0.25, 2)


    while True:
        t0 = time.time()
        blink(0.25, 0.25, 6)
        # mqtt_client.loop()
        try:
            print("looping...")
            mosquitto_client.loop()
            print("success!")
        except Exception as e:
            print("failed, trying again")
            mosquitto_client.connect()
            mosquitto_client.loop()
            print("success after retry!")
        
        data = sensors.get_sensor_data(SENSORS)

        # for k in data.keys():
        #     feed = aio_user + '/feeds/sensor' + str(sensor_id) + '.' + k
        #     mqtt_client.publish(feed, data[k])
        
        mosquitto_client.publish('solar/sensor' + str(os.getenv('SENSOR_ID')) + '/temppower', 
                                 sensors.prepare_data_mqtt(data))

        blink(1, 0.5, 6)
        t1 = time.time()
        t_rem = max(0, 120 - (t1 - t0))
        time.sleep(t_rem)

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
    time.sleep(20)
    microcontroller.reset()







