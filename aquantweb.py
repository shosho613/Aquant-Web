from flask import Flask, render_template, send_from_directory, request
from models import db
from werkzeug import secure_filename
import os

aquantweb = Flask(__name__, static_folder='frontend/build/static', template_folder="frontend/build")
aquantweb.config.from_object('config')

db.init_app(aquantweb)
db.create_all(app=aquantweb)

@aquantweb.route('/')
def home():
    return render_template('index.html')

@aquantweb.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       print(request.files["fileupload"])
       f = request.files
       f.save(secure_filename(f.filename))
       return 'file uploaded successfully'
    



if __name__ == '__main__':
    aquantweb.debug=True
    aquantweb.run(host='0.0.0.0')