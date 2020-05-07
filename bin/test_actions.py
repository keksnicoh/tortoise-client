#!/bin/python3

import asyncio
import websockets
import json
import logging
import getopt
import sys
import time
from threading import Thread
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
                    data = await websocket.recv()
                    action = json.loads(data)
                    if action['action'] == 'ping':
                        await websocket.send("pong")
                        print('[ping] pong!')
                    else:
                        q.put(action)
                        print("[queue] new queue item {}".format(action))
        except Exception as e:
            print(e)
            time.sleep(1)


def worker():
    while True:
        item = q.get()
        print(item)


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
