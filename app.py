from flask import Flask
from flask import request
from flask import make_response, Response
import os, json
from slacker import Slacker

SLACK_TOCKEN = "xoxb-409605691809-409444378032-ktcVNWRxS8ziKtnkNnpWV1qW"

app = Flask(__name__)
slack = Slacker(SLACK_TOCKEN)


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


@app.route('/', methods=["GET"])
def test():
    return Response('It works!')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
