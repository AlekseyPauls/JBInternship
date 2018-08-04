from flask import Flask
from flask import request
from flask import make_response, Response
import os, json

app = Flask(__name__)

@app.route('/webhook')
def hello_slack():
    request_json = request.get_json(silent=True, force=True)
    response_body_json = "ok"
    response_body = json.dumps(response_body_json)
    response = make_response(response_body)
    response.headers['Content-Type'] = 'application/json'
    return response


SLACK_WEBHOOK_SECRET = os.environ.get('SLACK_WEBHOOK_SECRET')


@app.route('/slack', methods=['POST'])
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
