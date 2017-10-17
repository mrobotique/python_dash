# http://stackoverflow.com/questions/20211990/sending-data-curl-json-in-python

import requests            #pip install requests
import simplejson as json  #pip install simplejson

url = "http://localhost:3030"
widget = "synergy"
data = { "auth_token": "YOUR_AUTH_TOKEN","value":5}

fullUrl = "%s/widgets/%s" % (url, widget)
headers = {'Content-type': 'application/json'}
print 'go'
requests.post(fullUrl, data=json.dumps(data), headers=headers)
print 'done'
