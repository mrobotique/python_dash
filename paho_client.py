import paho.mqtt.client as paho
global Data


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    global Data
##    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
    Data = str(msg.payload)
client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("hello/world", qos=1)

Data = 0
a = 1
while (True):
    client.loop(0.5)
    print a,'   ', Data
    a += 1
