import os
import ssl
import wifi
import socketpool
import adafruit_requests



def connect_wifi():
    print("connecting to wifi...")
    wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    print("connected")

def setup_requests():
    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())
    return requests

def is_connected():
    print("checking wifi connection...")
    print(wifi.radio.connected)
    return wifi.radio.connected
    # return True

def robust_connect():
    iter = 0
    while not is_connected() & iter < 10:
        try:
            connect_wifi()
        except e:
            print(e)
            print("failed, trying again")
            inter += 1
            time.sleep(3)
    if not is_connected():
        connect_wifi() # try one last time and dont' catch error
    print("wifi connected")