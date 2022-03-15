# python 3.6

import random
import time
import codecs

from paho.mqtt import client as mqtt_client
# import the opencv library
import cv2
import base64
import json

# define a video capture object
vid = cv2.VideoCapture(0)


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/chalice"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    # msg_count = 0
    while True:
        time.sleep(1)
        ret, frame = vid.read()
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = codecs.encode(buffer, 'base64').decode('utf8')
        # jpg_as_text = base64.b64encode(buffer)
        msg = {'msg': jpg_as_text}
        msg = json.dumps(msg)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"send frame to topic `{topic}`")
            # print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        # msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()