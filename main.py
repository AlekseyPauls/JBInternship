from flask import request
from flask import make_response, render_template
from flask_mobility.decorators import mobile_template
import os, json, csv, ast
from bot.respondent import make_answer
from bot import app, slack, auth, ADMIN, PASSWORD
import bot.service as serv


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
        dataset_names = json.dumps(serv.get_dataset_names())
        return render_template(template, dataset_names=dataset_names)


@app.route('/info', methods=["POST", "GET"])
@mobile_template('{mobile/}Info.html')
def datasets(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        print(data)
        return make_response(json.dumps({"answer": data["question"]}), 200, {"content_type": "application/json"})
    else:
        d = json.dumps(serv.get_datasets_info())
        s = json.dumps(serv.get_statistics_info())
        return render_template(template, datasets=d, statistics=s)


@app.route('/development', methods=["POST", "GET"])
@auth.login_required
@mobile_template('{mobile/}Development.html')
def feedback(template):
    if request.method == 'POST':
        if request.headers["Content-Type"] == "application/form-data":
            print(request.args)
            return make_response("ok")
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "getDatasetInfo":
            info = serv.get_dataset(data["name"])
            return make_response(json.dumps({"action": "setDatasetInfo", "data": info}), 200, {"content_type": "application/json"})
        elif data["action"] == "getStatisticInfo":
            info = serv.get_statistic(data["name"])
            return make_response(json.dumps({"action": "setStatisticInfo", "data": info}), 200, {"content_type": "application/json"})
        elif data["action"] == "saveDataset":
            print(str(data))
            print(data["name"] + " " + str(data["features"]) + " " + str(data["description"]) + " " + str(data["file"]))
            print(request.files["file"])
            return make_response("ok")
        return make_response("ok")
    else:
        d = json.dumps(serv.get_dataset_names())
        s = json.dumps(serv.get_statistic_names())
        t = json.dumps(['number', 'date', 'special'])
        return render_template(template, dataset_names=d, statistic_names=s, types=t)


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
