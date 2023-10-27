import os
import time
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import sys

import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


sys.path.append('./code/')
import pico_wifi as pw
import sensors
import pico_mqtt as pmqtt

def blink(t_on, t_off, n):
    for i in range(n):
        led.value = True
        time.sleep(t_on)
        led.value = False
        time.sleep(t_off)


def log_data():

    pw.robust_connect()
    print(pw.is_connected())
    requests = pw.setup_requests()
    mosquitto_client = pmqtt.setup_mqtt()
    pmqtt.robust_connect_mqtt(mosquitto_client)

    SENSORS = sensors.setup_sensors()

    while True:
        t0 = time.time()
        blink(0.25, 0.25, 6)
        data = sensors.get_sensor_data(SENSORS)

        pmqtt.robust_loop(mosquitto_client)
        payload = sensors.prepare_data_mqtt(data)
        print(payload)

        mosquitto_client.publish('solar/sensor' + str(os.getenv('SENSOR_ID')) + '/temppower', 
                                 payload)

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

    blink(1, 1, 5)
    time.sleep(20)
    microcontroller.reset()







