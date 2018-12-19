from flask import Flask
import os
import json
from rmqmqtt import MQTTClient

app = Flask(__name__)
app.config.from_object(__name__)

port = int(os.getenv('VCAP_APP_PORT', 8080))


@app.route('/mqtt/publish')
def mqtt_publish_message():
    client = MQTTClient()
    publish_result, count = client.publish_message()

    rmqresult = {}
    rmqresult['status_code'] = 200 if publish_result else 0
    rmqresult['message_count_published'] = count
    rmqresult['message_count_consumed'] = 0
    return json.dumps(rmqresult)

@app.route('/mqtt/subscribe')
def mqtt_subscribe_message():
    client = MQTTClient()
    client.subscribe_message()

    rmqresult = {}
    rmqresult['status_code'] = 200
    rmqresult['message_count_published'] = 0
    rmqresult['message_count_consumed'] = 0
    return json.dumps(rmqresult)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
