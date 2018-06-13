import os
import pathlib
import csv

from flask import Flask, redirect, render_template, request, flash, url_for
import time
from pack import kmeans

UPLOAD_FOLDER = 'client-upload'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# Create directory for the generated graphs
pathlib.Path('static/graphs').mkdir(parents=True, exist_ok=True)
pathlib.Path('client-upload').mkdir(parents=True, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'dataCSV' not in request.files:
            flash('No file part')
            print("exception1")
            return redirect(request.url)
        file = request.files['dataCSV']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or not allowed_file(file.filename):
            flash('No selected file or not CSV file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            name = f'{int(time.time())}-data'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{name}.csv'))
        return redirect(url_for('results', file_name=name))
    return redirect(request.url)


@app.route("/graphs/<file_name>", methods=['GET'])
def results(file_name):
    kmeans.KMeans(file_name).generate()
    rdr = csv.reader(open(f'static/graphs/{file_name}.csv', "r"))
    csv_data = [row for row in rdr]
    with open(f'static/graphs/{file_name}.txt') as f:
        new_file = f.read().rstrip("\n")
    return render_template('results.html', filename=file_name+".png", data=csv_data, highest=new_file)
