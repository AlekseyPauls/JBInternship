from flask import Flask
from flask import request
from flask import make_response, Response
import os, json

app = Flask(__name__)


@app.route('/webhook', methods=['POST', 'GET'])
def hello_slack():
    print(request.data)
    slack_event = json.loads(request.data.decode("UTF-8"))
    print(slack_event)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    if "message.im" in slack_event:
        return make_response("ok", 200, {"content_type": "application/json"})


SLACK_WEBHOOK_SECRET = "xoxb-409605691809-409444378032-ktcVNWRxS8ziKtnkNnpWV1qW"


@app.route('/slack', methods=['POST', 'GET'])
def inbound():
    if request.form.get('token') == SLACK_WEBHOOK_SECRET:
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
