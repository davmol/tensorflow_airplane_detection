#!/bin/bash

#Start der Objekterkennung

#abweichende Pfade müssen eventuell angepasst werden

export PYTHONPATH=$PYTHONPATH:/home/pi/tensorflow/models/research:/home/pi/tensorflow/models/research/slim:/home/pi/Desktop/project/script:/home/pi/.local/lib/python3.7/site-packages
export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0
sleep 2
sudo rmmod dvb_usb_rtl28xxu rtl2832
sleep 1
cd /home/pi/dump1090
#lxterminal -e ./dump1090 --interactive --net --net-ro-size 500 --net-ro-rate 5 &
./dump1090 --interactive --net --net-ro-size 500 --net-ro-rate 5 &

sudo /etc/init.d/postgresql restart
sleep 2
clear
cd /home/pi/Desktop/project/script/
#/usr/bin/python3.7 mail.py
/usr/bin/python3.7 scan1090.py >> scan1090.log 2>&1
