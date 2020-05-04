#!/bin/python3

import asyncio
import websockets
import json
import logging
import getopt
import sys
import time
from threading import Thread
from rpi_rf import RFDevice
import queue
import subprocess


logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())

q = queue.Queue()

async def client(api):

    while True:
        try:
            print("connect ...")
            async with websockets.connect(api) as websocket:
                while True:
                    data = await websocket.recv()
                    action = json.loads(data)
                    if action['action'] == 'ping':
                        await websocket.send("pong")
                        print('[ping] pong!')
                    else:
                        q.put(action)
                        print("[queue] new queue item {}".format(action))

        except websockets.exceptions.InvalidStatusCode:
            print("invalid status code... retry")
            time.sleep(1)
        except websockets.ConnectionClosed:
            print("closed connection ... retry")
            time.sleep(1)
        except OSError:
            print("os error... retry")
            time.sleep(1)


def action_light(payload, repeat):
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = repeat
    tx_code(rfdevice, payload, 'light1', 279889, 279892)
    tx_code(rfdevice, payload, 'light2', 282961, 282964)
    rfdevice.cleanup()


def tx_code(rfdevice, payload, key, c1, c2):
    value = payload.get(key, None)
    if value is not None:
        code = c1 if payload[key] else c2
        print('> {}: {} - {}'.format(key, value, code))
        rfdevice.tx_code(code, 1, 302, 24)


def worker(webcam_command):
    while True:
        item = q.get()
        if item['action'] == 'light':
            print('[light] ...')
            action_light(item['data'], 20)
        elif item['action'] == 'light_changed':
            print('[light_changed] ...')
            action_light(item['data'], 5)
        elif item['action'] == 'webcam':
            print('[webcam] ...')
            subprocess.call(webcam_command.split(' '))
        else:
            print('[???] {}'.format(item))


def main():
    api = "ws://localhost:8081/v1/stream"
    webcam_command = None

    opts, args = getopt.getopt(sys.argv[1:], '', ['api=', 'webcam_command='])
    for opt, val in opts:
        if opt == "--api":
            api = val
        elif opt == "--webcam_command":
            webcam_command = val
        else:
            assert False, "unhandled option"

    Thread(target=worker, daemon=True, args=(webcam_command, )).start()
    asyncio.get_event_loop().run_until_complete(client(api))


if __name__ == '__main__':
    main()
