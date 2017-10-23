#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""

## http://stackoverflow.com/questions/20211990/sending-data-curl-json-in-python

import requests            #pip install requests
import simplejson as json  #pip install simplejson
import time
import paho.mqtt.client as paho

url = "http://localhost:3030"
widgets = ["WazeTimeMiguel","WazeTimeGloria","WeatherCanada","IndoorTemp"]
token = "YOUR_AUTH_TOKEN"
TakePicture = False
HomeAlone = False

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

    
def SendToDashboard(widget,payload):
    fullUrl = "%s/widgets/%s" % (url, widget)
    headers = {'Content-type': 'application/json'}
    requests.post(fullUrl, data=json.dumps(payload), headers=headers)


def on_message(client, userdata, msg):
    widget_index = 99
    payload = ""
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))    
    Data = str(msg.topic).split("/")

##TopicNames:   sensors/indoortemp, sensors/motion_01, sensors/homealone,
##              waze/gloria, waze/miguel, alerts/winnipeg
    
    if (len(Data)>0):
        #print Data
        if (Data[1] == "sensors"):
            if (Data[2] == "indoortemp"):
                SendToDashboard
                widget_index = 3
                payload = {"auth_token": token,"value":msg.payload}
                SendToDashboard(widgets[widget_index],payload)

            if (Data[2] == "motion_01"):
                if(HomeAlone):
                    print "TakePicture"

            if (Data[2] == "homealone"):
                HomeAlone = msg.payload


        if (Data[1] == "waze"):
            
            #print Data[1]
            if (Data[2] == "miguel"):
                widget_index = 0
                payload = { "auth_token": token,"value":msg.payload}
                SendToDashboard(widgets[widget_index],payload)

            if (Data[2] == "gloria"):
                widget_index = 1
                payload = { "auth_token": token,"value":msg.payload}
                SendToDashboard(widgets[widget_index],payload)
                    
        if (Data[1] == "alerts"):
            widget_index = 2
            payload = { "auth_token": token,"value":msg.payload}
            SendToDashboard(widgets[widget_index],payload)




client = paho.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("dashboard/#", qos=1)

if __name__ == "__main__":    
    global Data
    Data = 0
    a = 1
    print "Go"
    while (True):
        client.loop(0.5)
        #print a,'   ', Data, '   ', client.msg.topic
        #a += 1
    
