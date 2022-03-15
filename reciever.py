# python3.6

import random

from paho.mqtt import client as mqtt_client
import json
import base64
import cv2
import codecs

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt/chalice"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(1)
        m_decode = msg.payload.decode("utf-8", "ignore")
        print(2)
        m_in = json.loads(m_decode)  # decode json data
        print('Recieved!')
        jpg_original = codecs.decode(codecs.encode(m_in['msg'], 'utf8'), 'base64')
        cv2.imshow('frame', jpg_original)
        # print(f"Received `{m_in['msg']}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
