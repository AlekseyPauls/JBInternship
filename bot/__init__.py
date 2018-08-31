from flask import Flask
from flask_mobility import Mobility
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
import configparser, os, logging, logmatic

try:
    config = configparser.RawConfigParser()
    config.read('settings.properties')
    SLACK_TOKEN = config['bot']['SLACK_TOKEN']
    ADMIN = config['service']['ADMIN']
    PASSWORD = config['service']['PASSWORD']
    APPHOST = config['service']['APPHOST']
    APPPORT = config['service']['APPPORT']
    DEBUG = config['service']['DEBUG']
    USER = config['db']['USER']
    PWD = config['db']['PWD']
    DB = config['db']['DB']
    HOST = config['db']['HOST']
    PORT = config['db']['PORT']
    print("Get config successfully")
except Exception:
    print("Cant read config file")
    SLACK_TOKEN = ""


app = Flask(__name__)
# Heroku
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# Local debug
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///bot"
# Docker
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://%s:%s@%s:%s/%s" % (USER, PWD, HOST, PORT, DB)
auth = HTTPBasicAuth()
Mobility(app)
slack = Slacker(SLACK_TOKEN)
db = SQLAlchemy(app)

log = logging.getLogger("logger")
handler = logging.FileHandler("feedback/logs.log")
handler.setFormatter(logmatic.JsonFormatter())
log.addHandler(handler)
log.setLevel(logging.INFO)
