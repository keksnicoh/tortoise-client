#!/bin/python3

"""webcam send

todo:
- use stream, do not persist to disk

"""
from picamera import PiCamera
import requests
import os
import getopt
import sys
from requests.auth import HTTPBasicAuth


def capture(fname):
    print("capturing ...")
    camera = PiCamera()
    camera.capture(fname)


def send(api, stream, password=None):

    if password is not None:
        auth = HTTPBasicAuth("pi", password)
    else:
        auth = None

    requests.post(
        api,
        files={
            "webcam": ("webcam.jpg", stream, "image/jpg")
        },
        auth=auth
    )


def main():
    api = "http://localhost:8081/v1/webcam"
    basepath = "/home/pi/tortoise-client/bin"
    password = None

    opts, args = getopt.getopt(sys.argv[1:], '', ['api=', 'password='])
    for opt, val in opts:
        print(opt)
        if opt == "--api":
            api = val
        elif opt == "--password":
            password = val
        else:
            assert False, "unhandled option"

    filepath = os.path.join(basepath, "webcam.jpg")
    capture(filepath)
    print("send {}".format(api))
    rs = open(filepath, "rb")
    send(api, rs, password=password)
    os.remove(filepath)
    exit(0)


if __name__ == "__main__":
    main()
