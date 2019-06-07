import os
import cv2
import numpy as np
import base64
from flask_cors import CORS, cross_origin

from flask import Flask, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    cors = CORS(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/testBase64', methods=['GET', 'POST', 'DELETE'])
    @cross_origin()
    def getBase64():
        data = request.form.get('imgBase64')
        return data

    @app.route('/getContours', methods = ['GET', 'POST', 'DELETE'])
    @cross_origin()
    def getMask():
        data_uri = request.form.get('imgBase64')
        img = data_uri_to_cv2_img(data_uri)

        height, width, channels = img.shape

        blank_image = np.zeros((height, width, 3), np.uint8)
        mask = get_mask(img)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            M = cv2.moments(contour)
            if (M["m00"] != 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(blank_image, (cX, cY), 7, (150, 150, 150), -1)

            # cv2.drawContours(blank_image, contour, -1, (150, 150, 150), 3)
            cv2.drawContours(img, contour, -1, (0, 255, 0), 3)

        tmp = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(blank_image)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        cv2.imwrite("../public/assets/img/test.png", dst)
        print("test.png")
        return 'test.png'

    return app

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    sensitivity = 20
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    return mask