#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""
import yaml #Pefs load
import paho.mqtt.client as paho #mqtt lib
import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def getPrefs(PrefFile):
    f = open(PrefFile,"r")
    MyPrefs = f.read()
    return yaml.load(MyPrefs)
    
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return [temp_c, temp_f]

def main():
    PrefFile =  "prefs.yaml"
    TopicName = "dashboard/sensors/indoortemp"
    YamlPrefs = getPrefs(PrefFile)
    
    client = paho.Client()
    client.on_publish = on_publish
    client.connect(YamlPrefs['mosquitto']['server'],YamlPrefs['mosquitto']['port'])
    client.loop_start()
    
    while(True):
        Temp = read_temp()
        print Temp
        if (Temp[0]<0):
            Temp[0] = round(Temp[0])
        else:
            Temp[0] = round(Temp[0],1)

        (rc, mid) = client.publish(TopicName, str(Temp[0]), qos=2)
        time.sleep(YamlPrefs['temperature']['refreshing_rate'])    
    
    
if __name__ == "__main__":
    try:
        main()
    except:
        print "fatal error"
