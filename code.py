import os
import ipaddress
import wifi
import socketpool
import board
import time
import busio

from adafruit_onewire.bus import OneWireBus

import adafruit_ds18x20
import adafruit_ina260

print()
print("Connecting to WiFi")
#  connect to your SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
print("My IP address is", wifi.radio.ipv4_address)

#  pings Google
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

print(dir(board))
ow_bus = OneWireBus(board.GP17)

devices = ow_bus.scan()
assert len(devices) == 1

ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])

i2c = busio.I2C(board.GP19, board.GP18)
ina260 = adafruit_ina260.INA260(i2c)

# while True:
#     print("Temp:", ds18b20.temperature)
#     print("Current:", ina260.current)
#     print("Voltage:", ina260.voltage)
#     print("Power:", ina260.power)
#     time.sleep(10)
# print('Temperature: {0:0.3f} °C'.format(ds18b20.temperature))