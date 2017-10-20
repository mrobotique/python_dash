#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""
import yaml #Pefs load
import paho.mqtt.client as paho #mqtt lib
import RPi.GPIO as GPIO
import time

PIR_Input_pin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_Input_pin, GPIO.IN)         #Read output from PIR motion sensor

def getPrefs(PrefFile):
    f = open(PrefFile,"r")
    MyPrefs = f.read()
    return yaml.load(MyPrefs)

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    
def readPin(pin,delay=0.1):
    i=GPIO.input(pin)
    time.sleep(delay)
    return i

if __name__ == "__main__":
    TopicName = "dashboard/sensors/motion_01"
    PrefFile =  "prefs.yaml"
    
    YamlPrefs = getPrefs(PrefFile)
    
    client = paho.Client()
    client.on_publish = on_publish
    client.connect(YamlPrefs['mosquitto']['server'],YamlPrefs['mosquitto']['port'])
    client.loop_start()
    
    try:
        toggle = 0
        while(True):
            LastDetection = readPin(YamlPrefs['motion']['gpio_pir_pin'],YamlPrefs['motion']['delay'])
            if (toggle <> LastDetection):
                toggle = LastDetection
                (rc, mid) = client.publish(TopicName, str(LastDetection), qos=2)
    except:
        (rc, mid) = client.publish(TopicName, "KO", qos=2)	
        time.sleep(0.1)
        print "fatal error"

