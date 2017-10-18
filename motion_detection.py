#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""
import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import time

PIR_Input_pin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_Input_pin, GPIO.IN)         #Read output from PIR motion sensor



def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
    
def readPin(pin,delay=0.1):
  i=GPIO.input(pin)
  time.sleep(delay)
  return i

if __name__ == "__main__":
  TopicName = "dashboard/sensors/motion_01"
  client = paho.Client()
  client.on_publish = on_publish
  client.connect("localhost", 1883)
  client.loop_start()
  try:
    toggle = 0
    while(True):
      LastDetection = readPin(PIR_Input_pin,0.2)
      if (toggle <> LastDetection):
        toggle = LastDetection
        (rc, mid) = client.publish(TopicName, str(LastDetection), qos=2)
  except:
    (rc, mid) = client.publish(TopicName, "error", qos=2)

