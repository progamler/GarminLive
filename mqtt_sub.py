import paho.mqtt.client as mqtt
import json
import time
import os

#display all changes inside the MQTT Topic garmin/*/trackpoints
def on_message(client, userdata, message):
    print(f"message received {str(message.payload.decode('utf-8'))}")
    print(f"message topic={message.topic}")
    print(f"message qos={message.qos}")
    print(f"message retain flag={message.retain}")
    
#connect to the MQTT Broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_start()
client.subscribe("garmin/+/trackpoints")

#keep the script running
while True:
    time.sleep(1)
