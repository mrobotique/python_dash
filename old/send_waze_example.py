#!/usr/bin/python
# http://stackoverflow.com/questions/20211990/sending-data-curl-json-in-python

import requests            #pip install requests
import simplejson as json  #pip install simplejson
import WazeRouteCalculator
import time
import feedparser as fp


urlAlerts="https://weather.gc.ca/rss/battleboard/mb9_e.xml"


#url = "http://192.168.0.25:3030"
url="http://localhost:3030"
widgets = ["WazeTimeMiguel","WazeTimeGloria","WeatherCanada"]

from_Home = '795 Sterling Lyon Parkway, Winnipeg'
to_JCA = '117 Kind Edward Street, Winnipeg'
to_CCare = '555 Notre Dame Avenue, Winnipeg'
region = 'NA'
counter = 0


while(True):
    routeJCA = WazeRouteCalculator.WazeRouteCalculator(from_Home, to_JCA, region)
    routeJCA_info = routeJCA.calc_route_info()

    routeCCare = WazeRouteCalculator.WazeRouteCalculator(from_Home, to_CCare, region)
    routeCCare_info = routeCCare.calc_route_info()
      

    ##print route_info

    dataJCA = { "auth_token": "YOUR_AUTH_TOKEN", "value": int(routeJCA_info[0])} #Time to arrive Miguel
    dataCCare = { "auth_token": "YOUR_AUTH_TOKEN", "value":int(routeCCare_info[0])} #Time to arrive Gloria

    fullUrl = "%s/widgets/%s" % (url, widgets[0])
    headers = {'Content-type': 'application/json'}
    requests.post(fullUrl, data=json.dumps(dataJCA), headers=headers)

    fullUrl = "%s/widgets/%s" % (url, widgets[1])
    headers = {'Content-type': 'application/json'}
    requests.post(fullUrl, data=json.dumps(dataCCare), headers=headers)

    rss = fp.parse(urlAlerts)
    if (len(rss.entries)>0):
        rssMessage = rss.entries[0]['title_detail']['value']
        dataRSS = { "auth_token": "YOUR_AUTH_TOKEN", "text": rssMessage   } 
        fullUrl = "%s/widgets/%s" % (url, widgets[2])
        headers = {'Content-type': 'application/json'}
        requests.post(fullUrl, data=json.dumps(dataRSS), headers=headers)
        #print "RSS" + rssMessage
    
    lista = []
    for i in range(1,9):
        if (i<10):
            lista.append({'label':str(i)+"."})
        else:
            lista.append({'label':"."})
            
	
    data_lista = { "auth_token": "YOUR_AUTH_TOKEN","items":lista} #Time to arrive Miguel
    fullUrl = "%s/widgets/%s" % (url, "buzzwords")
    headers = {'Content-type': 'application/json'}
    requests.post(fullUrl, data=json.dumps(data_lista), headers=headers)

    counter +=1
    print 'done' + str(counter)	
    time.sleep(60)
