#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""
import yaml #Pefs load
import paho.mqtt.client as paho #mqtt lib
import os
import time

def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def getPrefs(PrefFile):
    f = open(PrefFile,"r")
    MyPrefs = f.read()
    return yaml.load(MyPrefs)
    
def checkHomeAlone(auth_list):
    sudoPassword = 'raspberry'
    command = 'arp-scan -l'
    home_alone = True
    arpscan_output = os.popen( "echo %s | sudo -S %s" % (sudoPassword,command) ).read()
    
    for key in   auth_list :
        #print auth_list[key]
        if (auth_list[key] in arpscan_output):
            home_alone = home_alone and False
            print auth_list[key]
            
    return home_alone
         
    
def main():
    PrefFile =  "prefs.yaml"
    TopicName = "dashboard/sensors/homealone"
    YamlPrefs = getPrefs(PrefFile)
    
    client = paho.Client()
    client.on_publish = on_publish
    client.connect(YamlPrefs['mosquitto']['server'],YamlPrefs['mosquitto']['port'])
    client.loop_start()
    
    while(True):
        HomeAlone =checkHomeAlone(YamlPrefs['mac_address_list'])
        (rc, mid) = client.publish(TopicName, str(HomeAlone), qos=2)
        if (HomeAlone):
            time.sleep(0.1)
        else:
            time.sleep(15)
    
    
if __name__ == "__main__":
    main()
#    try:
#        main()
#    except:
#        print "fatal error"
