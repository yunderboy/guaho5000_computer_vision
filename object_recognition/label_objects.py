# Imports the Google Cloud client library
from google.cloud import vision
import time
import sys

# Instantiates a google vision client
vision_client = vision.Client()


def label_objects(image_bytes):
    content = image_bytes.getvalue()

    image = vision_client.image(
        content=content)

    # Performs label detection on the image file
    labels = image.detect_labels()

    return labels