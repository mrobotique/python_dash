#!/bin/bash
dashing start &
echo "Dashing"
cd python_dash
echo "cd python_dash"

./dash_main.py &
echo "main"
./indoortemp_sender.py &
echo "indoor"
./motion_detection.py &
echo "motion"
./waze_sender.py &
echo "waze"
./whoisathome.py &
echo "whois"
./winnipeg_alerts.py &
echo "alerts"
echo "end!!!"
