#!/bin/sh -e
if ( ! ps aux | grep -q [s]can ) ;
then
  echo "no scanner running"
  nohup python3 /home/pi/scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &
  echo "scanner started"
else
  echo "scanner is already running"
fi
