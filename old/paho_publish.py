import paho.mqtt.client as paho
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("localhost", 1883)
client.loop_start()
temperature = 0
while True:
    temperature  += 1
    (rc, mid) = client.publish("hello/world", str(temperature), qos=1)
    time.sleep(2)
