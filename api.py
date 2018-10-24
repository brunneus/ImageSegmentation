from __future__ import print_function
import os
from flask import Flask, flash, request, redirect, url_for, send_file, jsonify  , make_response
from werkzeug.utils import secure_filename
import sys
from thresholding import segment_image

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_file_path)

        pixel_size = request.form['pixel_size']
        x = int(float(request.form['x']))
        y = int(float(request.form['y']))
        w = int(float(request.form['w']))
        h = int(float(request.form['h']))

        result_path, leaf_percentage_affected, area_total = segment_image(img_file_path, pixel_size, x, y, w, h)

        print(area_total, file=sys.stderr)

        response = send_file(result_path, mimetype='image/png', attachment_filename=area_total)
        response.headers['percentage_affected'] = leaf_percentage_affected
        response.headers['total_area_affected'] = area_total

        return response

@app.route('/infected_area', methods=['POST'])
def get_infected_area():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        img_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(img_file_path)
        result_path, leaf_percentage_affected, area_total = segment_image(img_file_path, request.form['pixel_size'])

        data = {}

        data['percentage'] = leaf_percentage_affected
        data['area'] = area_total

        return jsonify(data)