from flask import Flask
from flask_mobility import Mobility
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
import configparser, os

try:
    config = configparser.RawConfigParser()
    config.read('settings.properties')
    SLACK_TOKEN = config['bot']['SLACK_TOKEN']
    ADMIN = config['service']['ADMIN']
    PASSWORD = config['service']['PASSWORD']
    print("Get config")
except Exception:
    print("Cant read config file")
    SLACK_TOKEN = ""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bot"
auth = HTTPBasicAuth()
Mobility(app)
slack = Slacker(SLACK_TOKEN)
db = SQLAlchemy(app)
