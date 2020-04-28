#!/bin/python3

"""sensor status send script

sends sensor data to turle-servide status api.

"""

import requests
from requests.auth import HTTPBasicAuth
import getopt
import sys

import time
import board
import adafruit_dht


def read_sensor(n, device):
    dhtDevice = adafruit_dht.DHT22(device)
    for i in range(n):
        try:
            yield dhtDevice.temperature, dhtDevice.humidity
        except RuntimeError as error:
            print(error.args[0])

        time.sleep(2.5)


def send(api, temperature, humidity, temperature_outside, humidity_outside, password=None):
    """sends temperature and humidity via post request to turtle-service."""
    print("send {}".format(api))

    if password is not None:
        http_auth = HTTPBasicAuth('pi', password)
    else:
        http_auth = None

    requests.post(api, auth=http_auth, json={
        "temperature": temperature,
        "humidity": humidity,
        "temperature_outside": temperature_outside,
        "humidity_outside": humidity_outside
    })


def read(n, device):
    """reads n temperature and humidity values and returns
    the mean value, if at least one read is not `None`."""
    tL, hL = [], []
    for (t, h) in read_sensor(n, device):
        print(device, t, h)
        if t is not None:
            tL.append(t)
        if h is not None:
            hL.append(h)

    if len(tL) == 0:
        print("read error: no temperature")
        exit(1)

    if len(hL) == 0:
        print("read error: no humidity")
        exit(1)

    return sum(tL) / len(tL), sum(hL) / len(hL)


def main():
    api = "http://localhost:8081/v1/status"
    nread = 5
    password = None

    opts, args = getopt.getopt(sys.argv[1:], 'n:', ['api=', 'password='])
    for opt, val in opts:
        print(opt)
        if opt == "--api":
            api = val
        elif opt == "-n":
            nread = int(val)
        elif opt == "--password":
            password = val
        else:
            assert False, "unhandled option"

    if nread < 1:
        print("arg -n: must be greater than zero")
        exit(2)

    temperature, humidity = read(nread, device=board.D18)
    temperature_outside, humidity_outside = read(nread, device=board.D4)
    send(
        api,
        temperature=temperature,
        humidity=humidity,
        temperature_outside=temperature_outside,
        humidity_outside=humidity_outside,
        password=password
    )
    exit(0)


if __name__ == "__main__":
    main()
