import picamera
from time import sleep
from datetime import datetime
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
import time
import sys


image_stream = io.BytesIO()

# Instantiates a google vision client
vision_client = vision.Client()


def take_picture():
    answer = input('Take a picture? (y/n)')

    if answer == 'y':
        with picamera.PiCamera() as camera:
            camera.start_preview()
            # Camera warm-up time
            time.sleep(2)
            camera.capture(image_stream, 'jpeg')

            camera.start_preview()

            content = image_stream.getvalue()

            image = vision_client.image(
                content=content)

            # Performs label detection on the image file
            labels = image.detect_labels()

            print('Labels and confidence:')
            for label in labels:
                print('label:', label.description)
                print('score:', label.score)

            take_picture()

    if answer == 'n':
        print('Closing program...')
        sys.exit()

    if answer != 'n' or answer != 'y':
        print('What part of answering either y or n didn\'t you understand? ')
        take_picture()

    return

take_picture()
