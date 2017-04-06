import picamera
import io
import time


image_stream = io.BytesIO()


def take_picture(image_format):

    with picamera.PiCamera() as camera:
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(image_stream, image_format)
    return image_stream

if __name__ == '__main__':
    take_picture('jpg')