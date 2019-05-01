import os
import errno
import sys
from base64 import b64decode
from datetime import datetime
import time
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SAVE_DIR = './uploads/'

WORD = 'phone'

def ensure_upload_dir():
    try:
        os.makedirs(SAVE_DIR)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# saves a data uri as a png image to a file
def save_image(word, data):
    header, encoded = data.split(",", 1)
    data = b64decode(encoded)

    filename = SAVE_DIR+word+datetime.fromtimestamp(time.time()).strftime('-%Y-%m-%dT%H:%M:%S.png')
    with open(filename, "wb") as f:
        f.write(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'img' in request.form and 'word' in request.form:
            save_image(request.form.get('word'), request.form.get('img'))
            return render_template('index.html')
    else: 
        return render_template('index.html', word=WORD)

if __name__ == '__main__':
    ensure_upload_dir()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    debug = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'debug':
            debug = True

    app.run(host='0.0.0.0', port=7070, debug=debug)
