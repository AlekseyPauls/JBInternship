from flask import request
from flask import make_response, render_template
from flask_mobility.decorators import mobile_template
import os, json
from bot import app, slack, auth, ADMIN, PASSWORD, APPHOST, APPPORT, DEBUG
from bot.respondent import make_answer
from bot.respondent import types
import bot.service as serv


@app.route("/webhook", methods=["POST", "GET"])
def hello_slack():
    json_request = json.loads(request.data.decode("UTF-8"))
    if "challenge" in json_request:
        return make_response(json_request["challenge"], 200, {"content_type": "application/json"})
    slack_event = json_request["event"]
    if slack_event["type"] == "message":
        if "subtype" in slack_event:
            return make_response("ok", 200, {"content_type": "application/json"})
        else:
            answer = make_answer(slack_event["text"], "")
            slack.chat.post_message(slack_event["channel"], answer)
            return make_response("ok", 200, {"content_type": "application/json"})
    elif slack_event["type"] == "im_created":
        slack.chat.post_message(slack_event["channel"], "Hello once")
        return make_response("ok", 200, {"content_type": "application/json"})
    elif slack_event["type"] == "im_created":
        slack.chat.post_message(slack_event["channel"], "Hello again")
        return make_response("ok", 200, {"content_type": "application/json"})


@app.route("/commands", methods=["POST", "GET"])
def exec_command():
    command = request.form.get('command', None)
    text = request.form.get('text', None)
    if command == "/info":
        return "Datasets: \n\n" + serv.get_datasets_short_info() + "\nStatistics: \n\n" + serv.get_statistics_short_info() + \
            "\nTo get information about dataset features or statistic templates (possible questions) use commands " + \
            "'/info_dataset <dataset name>' and '/info_statistic <statistic name>'"
    elif command == "/info_dataset":
        d = serv.get_dataset_info(text)
        if d is None:
            return "Bad dataset name"
        return "Name: " + d[0] + "\nDescription: " + d[1] + "\nFeatures: " + d[2]
    elif command == "/info_statistic":
        s = serv.get_statistic_info(text)
        if s is None:
            return "Bad statistic name"
        return "Name: " + s[0] + "\nDescription: " + s[1] + "\nTemplates: " + s[2]
    elif command == "/rules":
        # TO DO: move it to settings or import from respondent
        return "1. Formulate simple questions consisting of a question, the main argument (what information is being " \
               "searched for), a delimiter (often a preposition), and a dependent argument (a condition, usually a " \
               "specific value or an interval of a feature)\n" \
               "2. To enter multiple arguments of the first or second type, separate them explicitly with the words " \
               "'and' and 'or'(don`t use commas)\n" \
               "3. Don`t use hard dependencies when one feature depends on another in one argument " \
               "(for example, 'Mean of users after 2017 year'). You can achieve the same effect by slightly changing " \
               "the question ('Mean of users in year after 2017') - now dependence of the features is explicit.\n" \
               "4. If you want to add an interval ('more', 'before', ...) for a group of arguments, make it for each " \
               "individual entity\n" \
               "5. Don`t use unnecessary words, like adjectives. If you did not receive an answer, try to delete " \
               "the unnecessary words and articles\n " \
               "6. If the bot replied that it did not find a suitable template, examine the list of statistics and " \
               "their templates and try asking a question again\n" \
               "7. If there was a problem with the recognition of the dataset, specify your arguments in the name of " \
               "the feature ('4535 users', 'month april') 7. If nothing helped, then leave a feedback and the problem " \
               "will be solved\n" \
               "8. If nothing helped, then leave a feedback and the problem will be solved"
    elif command == "/fb":
        serv.save_feedback(text)
        return "Thank you for the help!"
    return "ok"


@app.route('/health', methods=["POST", "GET"])
def health():
    return "Service is health!"


@app.route('/', methods=["POST", "GET"])
@mobile_template('{mobile/}StartPage.html')
def start(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "sendQuestion":
            answer = make_answer(data["question"], data["dataset"])
            return make_response(json.dumps({"action": "setAnswer", "answer": answer}), 200, {"content_type": "application/json"})
        elif data["action"] == "sendFeedback":
            serv.save_feedback(data["message"], data["question"], data["answer"])
            return make_response(json.dumps({"action": "setFeedback", "answer": "Thank you for the help!"}), 200, {"content_type": "application/json"})
    else:
        dataset_names = json.dumps(serv.get_dataset_names())
        return render_template(template, dataset_names=dataset_names)


@app.route('/info', methods=["POST", "GET"])
@mobile_template('{mobile/}Info.html')
def datasets(template):
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
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
        if "multipart/form-data" in request.headers["Content-Type"]:
            if request.values["action"] == "saveDatasetFile":
                file = request.files["file"]
                file.save("datasets/" + file.filename)
            elif request.values["action"] == "saveStatisticFile":
                file = request.files["file"]
                file.save("statistics/" + file.filename)
            return make_response("ok")
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "getDatasetInfo":
            info = serv.get_dataset(data["name"])
            return make_response(json.dumps({"action": "setDatasetInfo", "data": info}), 200, {"content_type": "application/json"})
        elif data["action"] == "getStatisticInfo":
            info = serv.get_statistic(data["name"])
            return make_response(json.dumps({"action": "setStatisticInfo", "data": info}), 200, {"content_type": "application/json"})
        elif data["action"] == "saveDataset":
            serv.save_dataset(data["name"], data["description"], data["features"], data["file"])
            d = json.dumps(serv.get_dataset_names())
            return make_response(json.dumps({"action": "reloadDatasets", "datasetNames": d}), 200, {"content_type": "application/json"})
        elif data["action"] == "saveStatistic":
            serv.save_statistic(data["name"], data["description"], data["templates"], data["file"])
            s = json.dumps(serv.get_statistic_names())
            return make_response(json.dumps({"action": "reloadStatistics", "statisticNames": s}), 200, {"content_type": "application/json"})
        elif data["action"] == "deleteDataset":
            serv.delete_dataset(data["name"])
            d = json.dumps(serv.get_dataset_names())
            return make_response(json.dumps({"action": "reloadDatasets", "datasetNames": d}), 200, {"content_type": "application/json"})
        elif data["action"] == "deleteStatistic":
            serv.delete_statistic(data["name"])
            s = json.dumps(serv.get_statistic_names())
            return make_response(json.dumps({"action": "reloadStatistics", "statisticNames": s}), 200, {"content_type": "application/json"})
        elif data["action"] == "getMessages":
            m = json.dumps(serv.get_messages(), default=str)
            return make_response(json.dumps({"action": "setMessages", "messages": m}), 200, {"content_type": "application/json"})
        elif data["action"] == "getLogs":
            l = json.dumps(serv.get_logs(), default=str)
            return make_response(json.dumps({"action": "setLogs", "logs": l}), 200, {"content_type": "application/json"})

        return make_response("ok")
    else:
        d = json.dumps(serv.get_dataset_names())
        s = json.dumps(serv.get_statistic_names())
        t = json.dumps(types)
        return render_template(template, dataset_names=d, statistic_names=s, types=t)


@auth.get_password
def get_pw(username):
    if username == ADMIN:
        return PASSWORD
    return None


if __name__ == '__main__':
    app.run(debug=bool(DEBUG), port=int(APPPORT), host=APPHOST)
