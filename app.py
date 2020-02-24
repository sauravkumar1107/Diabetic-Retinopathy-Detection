import os
import sys

# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Some utilites
import numpy as np
from util import base64_to_pil


# Declare a flask app
app = Flask(__name__)


# You can use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.mobilenet_v2 import MobileNetV2
#model = MobileNetV2(weights='imagenet')

#print('Model loaded. Check http://127.0.0.1:5000/')


# Model saved with Keras model.save()
MODEL_PATH = 'model.h5'

# Load your own trained model
model = load_model(MODEL_PATH)
#model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')
print('Model loaded. Check http://127.0.0.1:5000/')

def model_predict(img, model):
    img = img.resize((224, )*2, resample=Image.LANCZOS)
    x = np.empty((1, 224, 224, 3), dtype=np.uint8);
    x[0, :, :, :] = np.array(img)
    y = model.predict(x)
    y = y > 0.5
    y = y.astype(int).sum(axis=1) - 1
    preds = y[0]
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)

        # Save the image to ./uploads
        # img.save("./uploads/image.png")

        # Make prediction
        preds = model_predict(img, model)

        # Process your result for human
        if preds == 0:
            result = 'No DR'
        elif preds == 1:
            result = 'Mild'
        elif preds == 2:
            result = 'Moderate'
        elif preds == 3:
            result = 'Severe'
        else:
            result = 'Proliferative DR'
        # Serialize the result, you can add additional fields
        return jsonify(result=result)

    return None


if __name__ == '__main__':
    # app.run(port=5002, threaded=False)

    # Serve the app with gevent
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
