import io

import cv2
import numpy as np
from PIL import Image
from label_objects import label_objects

from object_recognition.detect_object_size import detect_object_size


def label_and_size(img, img_format, img_from_memory=True):

    if not img_from_memory:
        cv2_img, img_bytes = img_to_bytes(img, img_format, img_from_memory=False)

    labels = label_objects(img_bytes)
    for label in labels:
        print(label.description)

    orig = detect_object_size(cv2_img, 22.25)

    return orig


def img_to_bytes(img, img_format, img_from_memory=True):
    if not img_from_memory:
        PIL_img = Image.open(img)
        img_bytes = io.BytesIO()
        PIL_img.save(img_bytes, format=img_format)

        img_bytes.seek(0)
        img_array = np.asarray(bytearray(img_bytes.read()), dtype=np.uint8)
        cv2_img = cv2.imdecode(img_array, 1)
        return cv2_img, img_bytes
    else:
        return img


if __name__ == '__main__':
    label_and_size('./images/moar_test.jpg', 'JPEG', img_from_memory=False)