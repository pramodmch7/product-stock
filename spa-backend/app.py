from logging import debug
from flask import Flask, app, jsonify, request
from flask_cors import CORS
from db import db

from resources.Rsparaw import *
from resources.Rspafinal import *
from resources.Rspaprocess import *

app = Flask(__name__, static_folder='./build', static_url_path='/')
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SPdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

db.init_app(app)


@app.before_first_request
def createTabels():
    db.create_all()


@app.errorhandler(404)
def notFound(e):
    return app.send_static_file('index.html')


@app.route('/')
def home():
    # return 'HanUmaN'
    return app.send_static_file('index.html')


app.register_blueprint(RawProduct)
app.register_blueprint(FinalProduct)
app.register_blueprint(ProcessProduct)

if __name__ == '__main__':
    #from db import db
    # db.init_app(app)
    app.run(host='0.0.0.0', debug=False)
