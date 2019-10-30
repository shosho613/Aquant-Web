from flask import Blueprint, render_template

AppBlueprint = Blueprint('AppBlueprint', 'AppBlueprint')

@AppBlueprint.route('/', methods=['GET', 'POST'])
def server_app():
    return render_template('index.html')