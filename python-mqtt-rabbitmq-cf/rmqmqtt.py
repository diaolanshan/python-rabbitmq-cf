import paho.mqtt.client as paho
import os
import json
import time


class MQTTClient():
    mqtt_topic = "mqtt.demo.key"
    mqtt_host = None
    mqtt_pass = None
    mqtt_port = None
    Connected = False

    def __init__(self):
        vcap = os.environ['VCAP_SERVICES']
        if vcap != None:
            vcap_services = json.loads(vcap)
            if vcap_services != None:
                services = vcap_services.keys()
                for service in services:
                    if 'rabbitmq' in vcap_services[service][0]['tags']:
                        MQTTClient.mqtt_host = vcap_services[service][0]['credentials']['protocols']['mqtt']['host']
                        MQTTClient.mqtt_user = vcap_services[service][0]['credentials']['protocols']['mqtt'][
                            'username']
                        MQTTClient.mqtt_pass = vcap_services[service][0]['credentials']['protocols']['mqtt'][
                            'password']
                        MQTTClient.mqtt_port = vcap_services[service][0]['credentials']['protocols']['mqtt']['port']

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.Connected = True  # Signal connection
        else:
            print("Connection failed")

    def on_publish(self, client, userdata, mid):
        print('Message %s published' % (mid))

    def on_subscribe(self, client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, mosq, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload.decode('utf-8')))

    def publish_message(self):
        '''
        while using mqtt protocol, rabbitmq will select the amq.topic as exchange,
        and send the messages to the queue which using the topic key bind to it, in our case, it is the config.mqtt_topic
        '''
        client = paho.Client()
        # client.tls_set(ca_certs='cacrt.crt')
        client.username_pw_set(MQTTClient.mqtt_user, MQTTClient.mqtt_pass)
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.connect(MQTTClient.mqtt_host, MQTTClient.mqtt_port, 60)

        client.loop_start()

        while self.Connected != True:  # Wait for connection
            time.sleep(0.1)

        for value in range(0, 50):
            message = "test data" + str(value)
            (rc, mid) = client.publish(topic=MQTTClient.mqtt_topic, payload=str(message), retain=False)

        client.disconnect()
        client.loop_stop()

        return True, 50

    def subscribe_message(self):
        '''
        By running this, an queue will be created automatically and bind to the amq.topic exchange type use the mqtt_topic key.
        the messages send to the topic afterwards will be subscribed by this client.s
        :return:
        '''
        client = paho.Client()
        # client.tls_set(ca_certs='cacrt.crt')
        client.username_pw_set(MQTTClient.mqtt_user, MQTTClient.mqtt_pass)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe
        client.connect(MQTTClient.mqtt_host, MQTTClient.mqtt_port, 60)

        client.loop_start()

        while self.Connected != True:  # Wait for connection
            print("Not connected.")
            time.sleep(0.1)

        (rc, mid) = client.subscribe(MQTTClient.mqtt_topic, qos=1)

        time.sleep(5)
        client.loop_stop()
