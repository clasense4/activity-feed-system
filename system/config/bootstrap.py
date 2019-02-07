import os, yaml, json, logging
from flask import request
from flask_api import FlaskAPI
from flask_orator import Orator

dir_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename='flask.log')

app = FlaskAPI(__name__)
with open(dir_path + "/database.yml", 'r') as stream:
    config = yaml.load(stream)

app.config['ORATOR_DATABASES'] = config['databases']
db = Orator(app)
