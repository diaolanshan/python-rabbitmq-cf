from flask import Flask, request
import os
import json
from rmqamqp import AmqpClient

app = Flask(__name__)
app.config.from_object(__name__)

port = int(os.getenv('VCAP_APP_PORT', 8080))


@app.route('/amqp/publish')
def publish_message():
    # Publish one message to the rabbitmq message broker.
    try:
        client = AmqpClient()
        message = 'Messages to be sent'
        publish_result = client.publish_message(message)

        # Prepare the return value based on the publish result.
        rmqresult = dict()
        rmqresult['status_code'] = 200 if publish_result else 0
        rmqresult['message_published_count'] = 1
        rmqresult['message_consumed_count'] = 0

        return json.dumps(rmqresult), 200
    except Exception as e:
        return repr(e), 500


@app.route('/amqp/subscribe')
def subscribe_message():
    try:
        client = AmqpClient()
        subscribe_result, count = client.subscribe_message()

        rmqresult = dict()
        rmqresult['status_code'] = 200 if subscribe_result else 0
        rmqresult['message_published_count'] = 0
        rmqresult['message_consumed_count'] = count
        return json.dumps(rmqresult)

    except Exception as e:
        return repr(e), 500


@app.route('/')
@app.route("/index")
def index():
    publish_url = request.host_url + 'amqp/publish'
    subscribe_url = request.host_url + 'amqp/subscribe'

    return "<a href='" + publish_url + "'>Publish URL</a><br>" + "<a href='" + subscribe_url + "'>Subscribe URL</a>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
