import argparse
import base64
import json
from datetime import datetime
import os

import numpy as np
import socketio
import eventlet
import eventlet.wsgi
import time
from PIL import Image
from PIL import ImageOps
from flask import Flask, render_template
from io import BytesIO

from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array
import cv2

# Fix error with Keras and TensorFlow
import tensorflow as tf
tf.python.control_flow_ops = tf


sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None

def preprocessImage(image):

	nrow, ncol, nchannel = image.shape
	start_row = int(nrow * 0.35)
	end_row = int(nrow * 0.875)
    
	# This removes most of the area above the road and small amount below including the hood
	new_image = image[start_row:end_row, :]

	# This is NVIDIA's input parameters
	new_image = cv2.resize(new_image, (220,66), interpolation=cv2.INTER_AREA)
	
	return new_image

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        # The current steering angle of the car
        steering_angle = data["steering_angle"]
        # The current throttle of the car
        throttle = data["throttle"]
        # The current speed of the car
        speed = data["speed"]
        # The current image from the center camera of the car
        imgString = data["image"]
        image = Image.open(BytesIO(base64.b64decode(imgString)))


        image = image.convert('RGB')

        image_array = np.asarray(image)

   
        image_preprocess = preprocessImage(image_array)

        transformed_image_array = image_preprocess[None, :, :, :]

        # This model currently assumes that the features of the model are just the images. Feel free to change this.
        steering_angle = float(model.predict(transformed_image_array, batch_size=1))
        # The driving model currently just outputs a constant throttle. Feel free to edit this.

	   # Adaptive throttle - Both Track
        if (abs(float(speed)) < 10):
            throttle = 0.5
        else:
		  # When speed is below 20 then increase throttle by speed_factor
            if (abs(float(speed)) < 25):
                speed_factor = 1.35
            else:
                speed_factor = 1.0

            if (abs(steering_angle) < 0.1): 
                throttle = 0.3 * speed_factor
            elif (abs(steering_angle) < 0.5):
                throttle = 0.2 * speed_factor
            else:
                throttle = 0.15 * speed_factor

        print(steering_angle, throttle, speed)
        send_control(steering_angle, throttle)
        # save frame
        if args.image_folder != '':
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            image_filename = os.path.join(args.image_folder, timestamp)
            image.save('{}.jpg'.format(image_filename))
    else:
        # NOTE: DON'T EDIT THIS.
        sio.emit('manual', data={}, skip_sid=True)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit("steer", data={
    'steering_angle': steering_angle.__str__(),
    'throttle': throttle.__str__()
    }, skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument('model', type=str,
    help='Path to model definition json. Model weights should be on the same path.')

    parser.add_argument(
        'image_folder',
        type=str,
        nargs='?',
        default='',
        help='Path to image folder. This is where the images from the run will be saved.'
    )

    args = parser.parse_args()
    with open(args.model, 'r') as jfile:
        #model = model_from_json(jfile.read())
        model = model_from_json(json.loads(jfile.read()))

    model.compile("adam", "mse")
    weights_file = args.model.replace('json', 'h5')
    model.load_weights(weights_file)

    if args.image_folder != '':
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")
    else:
        print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
