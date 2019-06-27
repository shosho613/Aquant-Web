from flask import Flask, render_template, send_from_directory, request, send_file, Response
from models import db
from werkzeug import secure_filename
import os
from JSON_Converter import JSON_Converter 
from flask_cors import CORS, cross_origin
import json



aquantweb = Flask(__name__, static_folder='frontend/build/static', template_folder="frontend/build")
aquantweb.config.from_object('config')
aquantweb.config['CORS_HEADERS'] = 'Content-Type'

CORS(aquantweb)



db.init_app(aquantweb)
db.create_all(app=aquantweb)

jc = JSON_Converter()

@aquantweb.route('/')
def home():
    jc = JSON_Converter()
    return render_template('index.html')

@aquantweb.route('/upload', methods = ['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        print(request.form)
        f = request.files.get("file")
        f.save(f.filename)
        pagenum = int(request.form.get("pagenum"))
        jc.get_graph_from_filename(f.filename,pagenum)
        jc.get_json_graph()
        response = aquantweb.response_class(
            response=json.dumps(jc.json_rep),
            status=200,
            mimetype='application/json',)
        return response


@aquantweb.route('/GetNodes')
@cross_origin()
def create_Nodes():
    print(request)
    if request.method == 'GET':
        jc.get_json_graph()
        response = aquantweb.response_class(
            response=json.dumps(jc.json_rep),
            status=200,
            mimetype='application/json',)
        print(response)
        return response

@aquantweb.route('/downloadcsv', methods=['GET', 'POST'])
@cross_origin()
def download_csv():
    print(request)
    if request.method == 'POST':
        print(request.form.get('data'))
        events = json.loads(request.form.get('data'))
        print(events)
        jc.set_types(events)
        for i in jc.graph.get_events():
            print(repr(i))
        jc.run_algo()
        jc.create_csv()
        file = open('output.csv','r')
        return send_file('output.csv', mimetype='text/csv')



if __name__ == '__main__':
    aquantweb.debug=True
    aquantweb.run(
        host="localhost",
        port=5000
    )
