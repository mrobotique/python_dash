#!/usr/bin/python
## http://stackoverflow.com/questions/20211990/sending-data-curl-json-in-python

"""
Created on Tue Oct 18 15:06:14 2017
@author: mromero
"""
import yaml #Pefs load
import paho.mqtt.client as paho #mqtt lib
import time
#import requests            #pip install requests
#import simplejson as json  #pip install simplejson
import WazeRouteCalculator

def getPrefs(PrefFile):
    f = open(PrefFile,"r")
    MyPrefs = f.read()
    return yaml.load(MyPrefs)
    
def on_publish(client, userdata, mid):
    #print("mid: "+str(mid))
    pass

def getDriveTime(From,to,region):
    try:
        routeTime = WazeRouteCalculator.WazeRouteCalculator(From,to, region,log_lvl=None) 
        ###log_lvl=None silence output and just get the return value
        routeTime_info = routeTime .calc_route_info()
        return round(routeTime_info[0])
    except:
        return 99

#def SendToDashboard(url,widget,token,value):
#    succes = 1
#    try:
#        message = {"auth_token": str(token), "value": value}
#    except:
#        message = {"auth_token": str(token), "value": 0}
#        succes = succes * 0
#        
#    try:        
#        fullUrl = "%s/widgets/%s" % (url,widget)
#        headers = {'Content-type': 'application/json'}
#        requests.post(fullUrl, data=json.dumps(message), headers=headers)    
#    except:
#        succes = succes * 0
#
#    return succes
    
    
   
    
if __name__ == "__main__":
    
    try:
        PrefFile =  "prefs.yaml"
        YamlPrefs = getPrefs(PrefFile)
        client = paho.Client()
        client.on_publish = on_publish
        client.connect(YamlPrefs['mosquitto']['server'],YamlPrefs['mosquitto']['port'])
        client.loop_start()
    
        while(True):
            for key in YamlPrefs['waze_users']:
                DriveTime = getDriveTime(YamlPrefs['waze_users'][key]['from'],YamlPrefs['waze_users'][key]['to'],YamlPrefs['waze_users'][key]['region'])
                TopicName = 'dashboard/waze/'+key
                (rc, mid) = client.publish(TopicName, DriveTime, qos=2)
                
            time.sleep(YamlPrefs['waze']['refreshing_rate'])  
    except:
        (rc, mid) = client.publish(TopicName, "KO", qos=2)	
        time.sleep(0.1)
        print "fatal error"
