from flask import Flask, render_template, send_from_directory, request, send_file, Response
from models import db
from werkzeug import secure_filename
import os
from JSON_Converter import JSON_Converter 
from flask_cors import CORS, cross_origin
import json



aquantweb = Flask(__name__, static_folder='./static', template_folder="./templates")
aquantweb.config.from_object('config')
aquantweb.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(aquantweb)

addedEvents = []
pdfFile = ""

db.init_app(aquantweb)
db.create_all(app=aquantweb)

jc = JSON_Converter()

@aquantweb.route('/')
def home():
    jc = JSON_Converter()
# addedEvents = []
    return render_template('index.html')

@aquantweb.route('/upload', methods = ['GET', 'POST'])
@cross_origin()
def upload_file():
    if request.method == 'POST':
        del addedEvents[:]
        print(request.form)
        f = request.files.get("file")
        f.save(f.filename)
        pdfFile = f.filename
        print(pdfFile)
        pagenum = int(request.form.get("pagenum"))
        jc.get_graph_from_filename(f.filename,pagenum)
        response = aquantweb.response_class(
            response=json.dumps(jc.json_rep),
            status=200,
            mimetype='application/json',)
        return response


@aquantweb.route('/GetBasicGraph')
@cross_origin()
def get_basic_graph():
    print(request)
    if request.method == 'GET':
        jc.get_json_basic_graph()
        response = aquantweb.response_class(
            response=json.dumps(jc.json_rep),
            status=200,
            mimetype='application/json',)
        print(response)
        return response


@aquantweb.route('/GetGraph', methods=["GET", "POST"])
@cross_origin()
def get_graph():
    print(request)
    if request.method == 'POST':
        print(pdfFile)
        pagenum = int(request.form.get("pagenum"))
        f = request.files.get("file")
        jc.get_graph_from_filename(f.filename,pagenum)
        jc.get_json_graph()
        del addedEvents[:]
        response = aquantweb.response_class(
            response=json.dumps(jc.json_rep),
            status=200,
            mimetype='application/json',)
        print(response)
        return response


@aquantweb.route('/GetRawGraph', methods=["GET", "POST"])
@cross_origin()
def get_raw_graph():
    if request.method == 'POST':
        print(pdfFile)
        pagenum = int(request.form.get("pagenum"))
        f = request.files.get("file")
        jc.get_graph_from_filename(f.filename,pagenum)
        result = jc.get_raw_graph()
        del addedEvents[:]
        response = aquantweb.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json',)
        print(response)
        return response

@aquantweb.route('/GetAnnots', methods = ['GET', 'POST'], )
@cross_origin()
def get_annots():
    print(request.form)
    print(addedEvents)
    currentID = request.form.get('size')
    rep = jc.convert_to_json_nodes(addedEvents)
    print(rep)
    response = aquantweb.response_class(
        response = json.dumps(rep),
        status = 200,
        mimetype='application/json'
       )
    return response





@aquantweb.route('/GetConnectionLabels')
@cross_origin()
def get_Graph():
    print(request)
    if request.method == 'GET':
        jc.get_JSON_connectors()
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
        jc.add_nodes(request.form.get('nodes'))
        jc.add_connections(request.form.get('connectors'))
        for i in jc.graph.get_events():
            print(repr(i))
        jc.run_algo()
        jc.create_csv()
        file = open('output.csv','r')
        return send_file('output.csv', mimetype='text/csv')

@aquantweb.route('/addEventFromPDF' , methods=['GET', 'POST'])
@cross_origin()
def addEventFromPDF():
    print(request.form.get('event'))
    addedEvents.append(request.form.get('event'))
    response = aquantweb.response_class(
            response=json.dumps({'data' : addedEvents}),
            status=200,
            mimetype='application/json',)
    print(addedEvents)
    return response

@aquantweb.route('/removeEventFromPDF' , methods=['GET', 'POST'])
@cross_origin()
def removeEventFromPDF():
    print(request.form.get('event'))
    addedEvents.remove(request.form.get('event'))
    response = aquantweb.response_class(
            response=json.dumps({'data' : addedEvents}),
            status=200,
            mimetype='application/json',)
    print(addedEvents)
    return response



@aquantweb.route('/modifyEventFromPDF' , methods=['GET', 'POST'])
@cross_origin()
def modifyEventFromPDF():
    #print(request.form.get('event'))
    #addedEvents.remove(request.form.get('event'))
    response = aquantweb.response_class(
            response=json.dumps({'data' : addedEvents}),
            status=200,
            mimetype='application/json',)
    print(addedEvents)
    return response




if __name__ == '__main__':
    aquantweb.debug=True
    aquantweb.run(
        host="localhost",
        port=5000
    )
