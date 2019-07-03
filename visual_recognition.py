from __future__ import print_function
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json 
import os
import sqlalchemy
from os.path import abspath
from ibm_watson import VisualRecognitionV3, ApiException 
from sqlalchemy import create_engine
import image_upload

app = Flask(__name__)
CORS(app)

engine = create_engine("mysql+pymysql://root:Z@tchywhitec1oud@localhost:3306/emma_bot_schema")
conn = engine.connect()
print(engine)

visual_recognition = VisualRecognitionV3(
    version="2019-06-24",
    iam_apikey="Yc0teDe2og9aFreP9f8OCoXakAIBWVDoVh--mPlTf8ve"
)

def image_to_upload_and_classify():
    image_upload.fileUpload()
    file_name = image_upload.file_name
    image_path = abspath(f"images/{file_name}")

    # data = open(f'images/{file_name}', 'rb').read()
    # sql = "INSERT INTO images (img) VALUES (%s)"
    # conn.execute(sql, (data))

    try:
        with open(image_path, 'rb') as images_file:
            image_results = visual_recognition.classify(
                images_file=images_file,
                threshold='0.1',
                classifier_ids=['driverslicenses_1133537186']).get_result()
            # classified_as = image_results["images"][0]["classifiers"][0]["classes"][0]["class"]
    except ApiException as ex:
        print(ex)
    return jsonify(image_results)

# classifiers = visual_recognition.list_classifiers(verbose=True).get_result()
# print(json.dumps(classifiers, indent=2))

# with open("resources/connecticut.zip", 'rb') as ct_dl, open(
#     "resources/florida.zip", 'rb') as fl_dl, open(
#         "resources/newyork.zip", 'rb') as ny_dl, open(
#             "resources/cars.zip", 'rb') as cars_zip:
#     model = visual_recognition.create_classifier(
#         "driverslicenses",
#         positive_examples={
#             'connecticut drivers license': ct_dl,
#             "florida drivers license": fl_dl, 
#             "newyork drivers license": ny_dl},
#             negative_examples=cars_zip).get_result()
# print(json.dumps(model, indent=2))

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)