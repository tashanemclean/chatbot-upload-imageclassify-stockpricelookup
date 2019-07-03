import os
from flask import Flask, flash, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

file_name = ''

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def fileUpload():
        global file_name
        target = os.path.join(UPLOAD_FOLDER)
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination ="/".join([target, filename])
        file.save(destination)
        file_name = file.filename
        session['uploadFilePath'] = destination
        return file_name




if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)