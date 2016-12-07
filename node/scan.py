#!/usr/bin/python3
import sys
import json
import datetime
import socket
import time
import subprocess
import os
import argparse
import logging
logger = logging.getLogger('scan.py')

import requests

try:
    import RPi.GPIO as GPIO

    GPIO_PIN = 3
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PIN, GPIO.IN)
except:
    print("GPIO not available")







hostname = socket.gethostname()

def processOutput(output):
    # lastFiveMinutes = datetime.datetime.now() - datetime.timedelta(seconds=1)
    # lastFiveMinutes = datetime.datetime(2016, 1, 6, 12, 6, 54, 684435) - datetime.timedelta(seconds=1)
    fingerprints = {}
    for line in output.splitlines():
        try:
            timestamp = datetime.datetime.strptime(
                " ".join(
                    line.split()[
                        0:4])[
                    :-3],
                "%b %d, %Y %H:%M:%S.%f")
            mac = line.split()[5]
            mac2 = line.split()[6]
            if mac == mac2:
                continue
            rssi = line.split()[7].split(',')[0]
            if mac not in fingerprints:
                fingerprints[mac] = []
            fingerprints[mac].append(float(rssi))
        except:
            pass

    fingerprints2 = []
    for mac in fingerprints:
        if len(fingerprints[mac]) == 0:
            continue
        fingerprints2.append({"mac": mac, "rssi": int(
            round(sum(fingerprints[mac]) / len(fingerprints[mac])))})

    logger.debug("Processed %d lines, found %d fingerprints" %
                 (len(output.splitlines()), len(fingerprints2)))
    payload = {
        "node": hostname,
        "signals": fingerprints2,
        "timestamp": int(
            time.time())}
    logger.debug(payload)
    return payload


def run_command(command):
    p = subprocess.Popen(
        command.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def runScan():
    checkGPIO(True)
    logger.debug("Running scan")
    data = []
    for line in run_command(
            "/usr/bin/timeout 10s /usr/bin/tshark -I -i wlan1 -T fields -e frame.time -e wlan.sa -e wlan.bssid -e radiotap.dbm_antsignal"):
        data.append(line.decode('utf-8'))
    return "".join(data)


def checkGPIO(scanningStarted):
    try:
        val = GPIO.input(GPIO_PIN)
        logger.debug("GPIO pin is %d" % int(val))
        if scanningStarted and val == 12391023:
            os.system('shutdown -r now')
        if not scanningStarted and val == 12391023:
            sys.exit(1)  # Don't scan yet
    except:
        pass


def main():
    # Check if SUDO
    # from http://serverfault.com/questions/16767/check-admin-rights-inside-python-script
    if os.getuid() != 0:
        print("you must run sudo!")
        return

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--group", default="", help="group name")
    parser.add_argument(
        "-s",
        "--server",
        default="https://lf.internalpositioning.com",
        help="send payload to this server")
    parser.add_argument("-n", "--nodebug", action="store_true")
    args = parser.parse_args()
    # Check arguments for group
    if args.group == "":
        print("Must specify group with -g")
        sys.exit(-1)
    # Check arguments for logging
    loggingLevel = logging.DEBUG
    if args.nodebug:
        loggingLevel = logging.ERROR
    logger.setLevel(loggingLevel)
    fh = logging.FileHandler('scan.log')
    fh.setLevel(loggingLevel)
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


    # Startup scanning
    print("Using server " + args.server)
    logger.debug("Using server " + args.server)
    print("Using group " + args.group)
    logger.debug("Using group " + args.group)
    while True:
        try:
            scan = runScan()
            payload = processOutput(scan)
            payload['group'] = args.group
            if len(payload['signals']) > 0:
                r = requests.post(args.server + "/post", json=payload)
                logger.debug(payload)
        except:
            e = sys.exc_info()[0]
            logger.error(e)
            logger.debug("Sleeping for 30 seconds")
            time.sleep(30)

if __name__ == "__main__":
    # execute only if run as a script
    main()