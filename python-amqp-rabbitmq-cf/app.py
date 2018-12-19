from flask import Flask
import os
import json
from rmqamqp import AmqpClient

app = Flask(__name__)
app.config.from_object(__name__)

port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/amqp/publish')
def publish_message():
    # Publish one message to the rabbitmq message broker.
    client = AmqpClient()
    message = 'Messages to be sent'
    publish_result = client.publish_message(message)

    # Prepare the return value based on the publish result.
    rmqresult = {}
    rmqresult['status_code'] = 200 if publish_result else 0
    rmqresult['message_published_count'] = 1
    rmqresult['message_consumed_count'] = 0

    return json.dumps(rmqresult)


@app.route('/amqp/subscribe')
def subscribe_message():
    client = AmqpClient()
    subscribe_result, count = client.subscribe_message()

    rmqresult = {}
    rmqresult['status_code'] = 200 if subscribe_result else 0
    rmqresult['message_published_count'] = 0
    rmqresult['message_consumed_count'] = count
    return json.dumps(rmqresult)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
