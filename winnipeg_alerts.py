#!/usr/bin/python
"""
Created on Tue Oct 19
@author: mromero
"""
import yaml #Pefs load
import paho.mqtt.client as paho #mqtt lib
import os
import time
import feedparser as fp #rss parser - get alerts  pip install feedparser

def on_publish(client, userdata, mid):
    #print("mid: "+str(mid))
    pass

def getPrefs(PrefFile):
    f = open(PrefFile,"r")
    MyPrefs = f.read()
    return yaml.load(MyPrefs)
    
def getAlerts(url):
    rss = fp.parse(url)
    if (len(rss.entries)>0):
        rssMessage = rss.entries[0]['title_detail']['value']
    else:
        rssMessage = "Null - no rss feed received"
    return rssMessage
    #print "RSS" + rssMessage

if __name__ == "__main__":
    try:
        PrefFile =  "prefs.yaml"
        TopicName = "dashboard/alerts/winnipeg"
        YamlPrefs = getPrefs(PrefFile)
        
        client = paho.Client()
        client.on_publish = on_publish
        client.connect(YamlPrefs['mosquitto']['server'],YamlPrefs['mosquitto']['port'])
        client.loop_start()
    
        while(True):
            CurentAlert = getAlerts(YamlPrefs['alerts']['rssfeedurl'])
            (rc, mid) = client.publish(TopicName, CurentAlert, qos=2)
            time.sleep(YamlPrefs['alerts']['refreshing_rate'])
    except:
        (rc, mid) = client.publish(TopicName, "KO", qos=2)	
        time.sleep(1)
        print "fatal error"