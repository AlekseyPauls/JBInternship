from flask import Flask
from flask import request
from flask import make_response, render_template
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_httpauth import HTTPBasicAuth
from slacker import Slacker
from respondent import make_answer
import os, json, configparser, json, csv, ast


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
        print(data)
        answer = make_answer(data["question"], data["dataset"])
        return make_response(json.dumps({"action": "setAnswer", "answer": answer}), 200, {"content_type": "application/json"})
    else:
        dataset_names = json.dumps(get_dataset_names())
        return render_template(template, dataset_names=dataset_names)


@app.route('/info', methods=["POST", "GET"])
@mobile_template('{mobile/}Info.html')
def datasets(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        print(data)
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        d = json.dumps(get_datasets_info())
        s = json.dumps(get_statistics_info())
        return render_template(template, datasets=d, statistics=s)


@app.route('/development', methods=["POST", "GET"])
@auth.login_required
@mobile_template('{mobile/}Development.html')
def feedback(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "getDatasetInfo":
            info = get_dataset(data["name"])
            return make_response(json.dumps({"action": "setDatasetInfo", "data": info}), 200, {"content_type": "application/json"})
        elif data["action"] == "getStatisticInfo":
            info = get_statistic(data["name"])
            return make_response(json.dumps({"action": "setStatisticInfo", "data": info}), 200, {"content_type": "application/json"})
        return make_response("ok")
    else:
        d = json.dumps(get_dataset_names())
        s = json.dumps(get_statistic_names())
        t = json.dumps(['number', 'date', 'special'])
        return render_template(template, dataset_names=d, statistic_names=s, types=t)


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


def get_datasets_info():
    res = []
    with open('datasets/datasets.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            features = ast.literal_eval(row[2])
            s = ""
            for feature in features:
                s += "" + feature["name"] + " (" + feature["type"] + "), "
            s = s[:-2]
            res.append([row[0], row[1], s])
    return res


def get_dataset(name):
    with open('datasets/datasets.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0] == name:
                return {"name": row[0], "description": row[1], "features": ast.literal_eval(row[2]), "file": row[3]}
    return None


def get_dataset_names():
    res = []
    with open('datasets/datasets.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            res.append(row[0])
    return res


def get_statistics_info():
    res = []
    with open('statistics/statistics.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            templates = ast.literal_eval(row[2])
            s = ""
            for template in templates:
                s += template["question"] + "..."
                if template["delimiter"] is not None:
                    s += template["delimiter"] + "..."
                s += "?  "
            res.append([row[0], row[1], s])
    print(res)
    return res


def get_statistic(name):
    with open('statistics/statistics.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0] == name:
                return {"name": row[0], "description": row[1], "templates": ast.literal_eval(row[2]), "file": row[3]}
    return None


def get_statistic_names():
    res = []
    with open('statistics/statistics.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[3] == "file":
                continue
            res.append(row[0])
    return res


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
