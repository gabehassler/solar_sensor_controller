import os
import time
import ssl
import wifi
import socketpool
import microcontroller
import adafruit_requests



def connect_wifi():
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))

def setup_requests():
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests
