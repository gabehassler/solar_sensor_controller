import sys
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import ssl
import socketpool
import wifi
import os

sys.path.append('./code/')
import pico_wifi as pw

def setup_mqtt():
    pool = socketpool.SocketPool(wifi.radio)
    ssl_context = ssl.create_default_context()
    
    mosquitto_client = MQTT.MQTT(
        broker="52.89.139.124",
        port=1883,
        username=os.getenv("MOSQUITTO_USERNAME"),
        password=os.getenv("MOSQUITTO_PASSWORD"),
        socket_pool=pool,
        ssl_context=ssl_context,
    )

    return mosquitto_client

def robust_connect_mqtt(client):
    iter = 0
    while not client.is_connected() & iter < 10:
        try:
            print("trying to connect mqtt...")
            client.connect()
            print("success!")
            return
        except e:
            print(e)
            print("failed mqtt connect, trying again")
            time.sleep(3)
            iter += 1
    client.connect() # try one last time and dont' catch error
    print("success after retry!")


# def robust_setup_mqtt():
#     iter = 0
#     while iter < 10:
#         try:
#             print("trying to setup mqtt...")
#             return setup_mqtt()
#         except e:
#             print(e)
#             print("failed, trying again")
#             time.sleep(3)
#             iter += 1
#     return setup_mqtt() # try one last time and dont' catch error

def robust_loop(client):
    iter = 0
    while iter < 10:
        try:
            pw.connect_wifi()
            if not client.is_connected():
                client.connect()
            print("trying to loop mqtt...")
            client.loop()
            print("success!")
            return
        except e:
            print(e)
            print("failed mqtt loop, trying again")
            time.sleep(3)
            iter += 1


    client.loop() # try one last time and dont' catch error
    print("success after retry!")
