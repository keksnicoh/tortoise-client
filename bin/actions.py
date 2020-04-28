import asyncio
import websockets
from rpi_rf import RFDevice
import json
import logging
logger = logging.getLogger('websockets.server')
logger.setLevel(logging.ERROR)
logger.addHandler(logging.StreamHandler())
async def hello():
    uri = "ws://vps-ea1b2f2f.vps.ovh.net/wsapi/v1/stream"

    while True:
        try:
            print("connect ...")
            async with websockets.connect(uri) as websocket:
                while True:
                    greeting = await websocket.recv()

                    action = json.loads(greeting)
                    if action['action'] == 'light':
                        print("[action] light")
                        action_light(action['data'])

        except websockets.ConnectionClosed :
            print("closed connection ...")
        except OSError: 
            print("os error ...")

def action_light(payload):
    if payload.get('light1', None) is not None:
        switch(279889 if payload['light1'] else 279892)
    if payload.get('light2', None) is not None:
        switch(282961 if payload['light2'] else 282964)
      

def switch(code):
    print("code: {}".format(code))
    rfdevice = RFDevice(17)
    rfdevice.enable_tx()
    rfdevice.tx_repeat = 50
    rfdevice.tx_code(code, 1, 302, 24)
    rfdevice.cleanup()

asyncio.get_event_loop().run_until_complete(hello())

