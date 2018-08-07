from flask import Flask
from flask import request
from flask import make_response, render_template
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_httpauth import HTTPBasicAuth
from slacker import Slacker
from respondent import Respondent
import os, json, configparser, json, csv


try:
    config = configparser.RawConfigParser()
    config.read('settings.properties')
    SLACK_TOKEN = config['bot']['SLACK_TOKEN']
    ADMIN = config['service']['ADMIN']
    PASSWORD = config['service']['PASSWORD']
except Exception:
    print("Cant read config file")
    SLACK_TOKEN = ""


app = Flask(__name__)
auth = HTTPBasicAuth()
Mobility(app)
slack = Slacker(SLACK_TOKEN)


@app.route("/webhook", methods=["POST", "GET"])
def hello_slack():
    json_request = json.loads(request.data.decode("UTF-8"))
    print(json_request)
    if "challenge" in json_request:
        return make_response(json_request["challenge"], 200, {"content_type": "application/json"})
    slack_event = json_request["event"]
    if slack_event["type"] == "message":
        if "subtype" in slack_event:
            return make_response("ok", 200, {"content_type": "application/json"})
        else:
            slack.chat.post_message(slack_event["channel"], slack_event["text"])
            return make_response("ok", 200, {"content_type": "application/json"})


@app.route('/', methods=["POST", "GET"])
@mobile_template('{mobile/}StartPage.html')
def start(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        r = Respondent
        answer = r.answer(r, data["question"])
        return make_response(json.dumps({"answer":answer}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


@app.route('/info', methods=["POST", "GET"])
@mobile_template('{mobile/}Info.html')
def datasets(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        d = json.dumps(get_datasets())
        s = json.dumps(get_statistics())
        return render_template(template, datasets=d, statistics=s)


@app.route('/development', methods=["POST", "GET"])
@auth.login_required
@mobile_template('{mobile/}Development.html')
def feedback(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


def get_datasets():
    res = []
    with open('datasets/datasets.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            res.append([row[0], row[1], row[2]])
    return res


def get_statistics():
    res = []
    with open('statistics/statistics.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            res.append([row[0], row[1], row[2]])
    return res



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
