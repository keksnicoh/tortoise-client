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


def capture(fname):
    print("capturing ...")
    camera = PiCamera()
    camera.capture("webcam.jpg")


def send(api, stream):
    requests.post(
        api,
        files={
            "webcam": ("webcam.jpg", stream, "image/jpg")
        }
    )


def main():
    api = "http://localhost:8081/v1/webcam"

    opts, args = getopt.getopt(sys.argv[1:], '', ['api='])
    for opt, val in opts:
        print(opt)
        if opt == "--api":
            api = val
        else:
            assert False, "unhandled option"

    capture("webcam.jpg")
    print("send {}".format(api))
    send(api, open("webcam.jpg", "rb"))
    os.remove("webcam.jpg")
    exit(0)


if __name__ == "__main__":
    main()
