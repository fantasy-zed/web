#!/bin/bash
clear
ps -ef|grep 'main.py 80' > 1
PID=`awk '{print $2}' 1 | head -n 1`
sudo kill -9 ${PID}
echo "sudo kill -9 ${PID}"
sudo python3 main.py 80