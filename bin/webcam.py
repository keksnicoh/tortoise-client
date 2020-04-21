from picamera import PiCamera
import time
import requests
import os

camera = PiCamera()
#camera.start_preview()
#time.sleep(0.1)
camera.capture("webcam.jpg")
#camera.stop_preview()

requests.post(
    "http://192.168.178.21:8081/v1/webcam",
    files={
        "foo": ("webcam.jpg", open("webcam.jpg", "rb"), "image/jpg")
    },
    #headers={
    #    "Content-Type": "multipart/form-data", 
    #    "Accept": "application/json"
    #}
)

os.remove("webcam.jpg")
