#!/bin/python3

"""sensor status send script

sends sensor data to turle-servide status api.

"""

import requests
import getopt
import sys


def read_sensor(n):
    for i in range(n):
        yield 1, 1


def send(api, temperature, humidity):
    """sends temperature and humidity via post request to turtle-service."""
    requests.post(api, json={
        "temperature": temperature,
        "humidity": humidity
    })


def read(n):
    """reads n temperature and humidity values and returns
    the mean value, if at least one read is not `None`."""
    tL, hL = [], []
    for (t, h) in read_sensor(5):
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

    opts, args = getopt.getopt(sys.argv[1:], 'n:', ['api='])
    for opt, val in opts:
        if opt == "--api":
            api = val
        if opt == "-n":
            nread = int(val)
        else:
            assert False, "unhandled option"

    if nread < 1:
        print("arg -n: must be greater than zero")
        exit(2)

    temperature, humidity = read(nread)
    send(api, temperature=temperature, humidity=humidity)
    exit(0)


if __name__ == "__main__":
    main()
