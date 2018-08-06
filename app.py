from flask import Flask
from flask import request
from flask import make_response, render_template
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from flask_socketio import SocketIO, join_room, leave_room
from slacker import Slacker
import os, json, configparser, json


try:
    config = configparser.RawConfigParser()
    config.read('settings.properties')
    SLACK_TOKEN = config['bot']['SLACK_TOKEN']
except Exception:
    print("Cant read config file")
    SLACK_TOKEN = ""


app = Flask(__name__)
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
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


@app.route('/datasets', methods=["POST", "GET"])
@mobile_template('{mobile/}Datasets.html')
def datasets(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


@app.route('/statistics', methods=["POST", "GET"])
@mobile_template('{mobile/}Statistics.html')
def statistics(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


@app.route('/feedback', methods=["POST", "GET"])
@mobile_template('{mobile/}Feedback.html')
def feedback(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        return render_template(template)


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')
