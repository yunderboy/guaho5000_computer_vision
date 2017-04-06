from capture_img import take_picture
from picamera import PiCamera

from object_recognition.label_and_size import label_and_size

camera = PiCamera()

def take_image_and_process(img_format):
    camera.start_preview()
    image_stream = take_picture(camera)
    label_and_size(image_stream, img_format)

    return

if __name__ == '__main__':
    take_image_and_process('JPEG')