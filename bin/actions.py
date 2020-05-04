#!/bin/python3

import asyncio
import websockets
import json
import logging
import getopt
import sys
from threading import Thread
from rpi_rf import RFDevice
import queue
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
                    greeting = await websocket.recv()
                    action = json.loads(greeting)
                    if action['action'] in ['light', 'light_changed']:
                        q.put(action['data'])
                        print("[{}] light".format(action['action']))
                        #Thread(
                        #    target=action_light,
                        #    args=(action['data'], )
                        #).start()
                    elif action['action'] == 'ping':
                        print('got pinged...')
                        await websocket.send("pong")
                    else:
                        msg = '[???] cannot interpret payload {}'
                        print(msg.format(action))

        except websockets.ConnectionClosed:
            print("closed connection ...")
        except OSError:
            print("os error ...")


def action_light(payload):
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = 5
    for i in range(0, 1):
        if payload.get('light1', None) is not None:
            switch(rfdevice, 279889 if payload['light1'] else 279892)
        if payload.get('light2', None) is not None:
            switch(rfdevice, 282961 if payload['light2'] else 282964)
    rfdevice.cleanup()

def switch(rfdevice, code):
    print("code: {}".format(code))
    rfdevice.tx_code(code, 1, 302, 24)


def worker():
    while True:
        item = q.get()
        print(item)
        action_light(item)

def main():
    api = "ws://localhost:8081/v1/stream"

    opts, args = getopt.getopt(sys.argv[1:], '', ['api='])
    for opt, val in opts:
        if opt == "--api":
            api = val
        else:
            assert False, "unhandled option"

    Thread(target=worker, daemon=True).start()
    asyncio.get_event_loop().run_until_complete(client(api))


if __name__ == '__main__':
    main()
