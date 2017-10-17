import os
import glob
import time

import requests            #pip install requests
import simplejson as json  #pip install simplejson

url = "http://localhost:3030"
widget = "IndoorTemp"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

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
	
while True:
	Temp = read_temp()
	print Temp
	if (Temp[0]<0):
	    Temp[0] = round(Temp[0])
	else:
  	    Temp[0] = round(Temp[0],1)
  	    
	data = { "auth_token": "YOUR_AUTH_TOKEN","value":Temp[0]}
	fullUrl = "%s/widgets/%s" % (url, widget)
	headers = {'Content-type': 'application/json'}
	requests.post(fullUrl, data=json.dumps(data), headers=headers)
	time.sleep(60)
