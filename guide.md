How to connect to RPIs
How to download from EC2 instance
How to see what machines are ON and Connected

Per PI:
Install StatsD to manage uptime w/ ec2 server
  Send IP Address
Ansible to manage devices


Isolate 5 value piece of dataset

I need to get rid of temp file with PY file
  send json direct to server instead of creating temp file
I need to put PY

EXPORT Server Data to LAMDA
Run PYTHON Script against Data (pull training files off of S3)
Write Result to S3
Batch Import from S3




OG: ssh pi@10.218.200.48, Address: B8:27:EB:68:CD:BB (Raspberry Pi Foundation)
AG: ssh pi@10.218.200.52, Address: B8:27:EB:68:A6:2E (Raspberry Pi Foundation)
AF: ssh pi@10.218.200.60, Address: B8:27:EB:4E:57:30 (Raspberry Pi Foundation)
AQ: ssh pi@10.218.200.72, Address: B8:27:EB:25:D3:86 (Raspberry Pi Foundation)
AN: ssh pi@10.218.200.73, Address: B8:27:EB:D3:3A:A3 (Raspberry Pi Foundation)
AK: ssh pi@10.218.200.74, Address: B8:27:EB:55:2D:4A (Raspberry Pi Foundation)
AJ: ssh pi@10.218.200.77, Address: B8:27:EB:8E:6D:C1 (Raspberry Pi Foundation)
AB: ssh pi@10.218.200.82, Address: B8:27:EB:85:05:43 (Raspberry Pi Foundation)
AO: ssh pi@10.218.200.84, Address: B8:27:EB:A7:D9:3F (Raspberry Pi Foundation)
AP: ssh pi@10.218.200.85, Address: B8:27:EB:31:0A:0B (Raspberry Pi Foundation)
AI: ssh pi@10.218.200.86, Address: B8:27:EB:00:3C:69 (Raspberry Pi Foundation)
AE: ssh pi@10.218.200.88, Address: B8:27:EB:C7:59:B8 (Raspberry Pi Foundation)
AM: ssh pi@10.218.200.89, Address: B8:27:EB:90:55:93 (Raspberry Pi Foundation)

ssh -o ConnectTimeout=10 pi@10.218.200.48 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.52 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.60 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.72 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.73 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.74 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.77 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.82 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.84 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.85 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.86 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.88 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"
ssh -o ConnectTimeout=10 pi@10.218.200.89 "sudo nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &"


#--------- Reboot daily
sudo nano /etc/cron.daily/zz-reboot

#!/bin/sh
shutdown -r now

sudo chmod a+x /etc/cron.daily/zz-reboot

sudo run-parts /etc/cron.daily


#--------- Beacons on Allure check if it's Sunday before running
#
#!/bin/sh -e
if ( date | grep -q "Sun" ) && ( ! ps aux | grep -q [s]can ) ;
then
  echo "Sun and no scanner running"
  nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &
  echo "scanner started"
else
  echo "Not Sun and scanner is already running"
fi
#--------- Beacons on Allure check if it's Sunday before running

#--------- Start scanning on boot
#
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
nohup python3 scan.py --interface wlan1 --time 10 --group rcclport18demo --server http://54.218.102.95:18072 < /dev/null > std.out 2> std.err &

exit 0
#--------- Start scanning on boot




# sudo nano /etc/udev/rules.d/72-wlan-geo-dependent.rules
# +---------------+
# | wlan1 | wlan1 |
# +-------+-------+
# | wlan1 | wlan1 |
# +---------------+ (RPI USB ports with position independent device names for a maximum of 1 optional wifi dongle)
#
# | wlan0 | (onboard wifi)
#
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="sdio", KERNELS=="mmc1:0001:1", NAME="wlan0"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.2",       NAME="wlan1"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.4",       NAME="wlan1"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.3",       NAME="wlan1"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.5",       NAME="wlan1"
