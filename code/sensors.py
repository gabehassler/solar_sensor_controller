import board
import time
import busio

from adafruit_onewire.bus import OneWireBus

import adafruit_ds18x20
import adafruit_ina260

def setup_sensors():
    ow_bus = OneWireBus(board.GP28)

    devices = ow_bus.scan()
    assert len(devices) == 1

    ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])

    i2c = busio.I2C(board.GP27, board.GP26)
    ina260 = adafruit_ina260.INA260(i2c)

    # return dictionary
    return {
        'ds18b20': ds18b20,
        'ina260': ina260
    }

def log_to_screen(iters = float('inf')):
    # setup sensors
    sensors = setup_sensors()
    ds18b20 = sensors['ds18b20']
    ina260 = sensors['ina260']

    count = 0
    while count < iters:
        print("Temp:", ds18b20.temperature)
        print("Current:", ina260.current)
        print("Voltage:", ina260.voltage)
        print("Power:", ina260.power)
        print("")
        time.sleep(2)
        count += 1



def get_sensor_data(sensors):
    # setup sensors
    ds18b20 = sensors['ds18b20']
    ina260 = sensors['ina260']

    # return dictionary
    return {
        'temp': ds18b20.temperature,
        'current': ina260.current,
        'voltage': ina260.voltage,
        'power': ina260.power
    }

def prepare_data_mqtt(data):
    vars = ['temp', 'current', 'voltage', 'power']
    s = [v + ':' + str(data[v]) for v in vars]
    return ','.join(s)



