import os
import cv2
import numpy as np
import base64
from flask_cors import CORS, cross_origin

from flask import Flask, request, jsonify


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

    @app.route('/mergePhotos', methods=['GET', 'POST', 'DELETE'])
    @cross_origin()
    def mergePhotos():
        mergeImage = request.form.get('mergeImage')
        mergeImage = data_uri_to_cv2_img(mergeImage)

        cv2.imwrite("mergeImageBase.png", mergeImage)
        # maskMergeImage = get_mask(mergeImage)
        # cv2.imwrite("maskMergeImage.png", maskMergeImage)
        # openCvMergeImage = cv2.imread("maskMergeImage.png")

        tmp = cv2.cvtColor(mergeImage, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 15, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(mergeImage)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        cv2.imwrite("mergeImageAfterExtrudeBlack.png", dst)
        l_img = cv2.imread("basePhoto.jpg")
        x_offset = y_offset = 0
        # l_img[y_offset:y_offset+s_img.shape[0], x_offset:x_offset+s_img.shape[1]] = s_img

        s_img = cv2.imread("mergeImageAfterExtrudeBlack.png", -1)

        # Merge 2 photos
        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]
        alpha_s = s_img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                                      alpha_l * l_img[y1:y2, x1:x2, c])

        cv2.imwrite("../public/assets/img/merge.png", l_img)

        return "merge.png"

    @app.route('/getContours', methods = ['GET', 'POST', 'DELETE'])
    @cross_origin()
    def getMask():
        data_uri = request.form.get('imgBase64')
        img = data_uri_to_cv2_img(data_uri)
        cv2.imwrite("basePhoto.jpg", img)
        height, width, channels = img.shape

        blank_image = np.zeros((height, width, 3), np.uint8)
        mask = get_mask(img)

        #     M = cv2.moments(contour)
        #     if (M["m00"] < 10 and M["m00"] != 0 and M["m00"] > 4):
        #         cX = int(M["m10"] / M["m00"])
        #         cY = int(M["m01"] / M["m00"])
        #         cv2.circle(blank_image, (cX, cY), 1, (0, 255, 0), -1)

            # cv2.drawContours(img, contour, -1, (0, 255, 0), 3)

        #Create Sketch
        cv2.imwrite("mask.png", mask)
        cv2.imwrite("hintTestColor.png", blank_image)
        contour = cv2.imread("mask.png")
        tmp = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(contour)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        contours, _ = cv2.findContours(dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            cv2.drawContours(dst, contour, -1, (0, 0, 150), 3)
        cv2.imwrite("../public/assets/img/sketch.png", dst)

        # Create Hint
        cv2.imwrite("maskHint.png", blank_image)
        contour = cv2.imread("maskHint.png")
        tmp = cv2.cvtColor(contour, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(contour)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        cv2.imwrite("../public/assets/img/hint.png", dst)

        data = {'sketch': 'sketch.png', 'hint': 'hint.png'}
        return jsonify(data)

    return app

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def get_mask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    sensitivity = 80
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    return mask