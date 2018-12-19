import pika
import os
import json


def on_message_rejected(channel, method, properties, body):
    print('Message %s been rejected', body)

class AmqpClient(object):
    exchange_name = "com.bosch.de.bics.demo.exchange"
    queue_name = "com.bosch.de.bics.demo.queue"
    routing_key = "com.bosch.de.bics.demo.routingKey"

    def __init__(self):
        print('Init been called ...')
        try:
            vcap_services = json.loads(os.environ['VCAP_SERVICES'])
            if vcap_services != None:
                for service in vcap_services.keys():
                    if 'rabbitmq' in vcap_services[service][0]['tags']:
                        # Use the first 'rabbitmq' service.
                        uri = vcap_services[service][0]['credentials']['protocols']['amqp']['uri']
                        break
        except Exception as e:
            print('Probablly no rabbitmq service been binded to the app ?')

        connectionParameters = pika.URLParameters(uri + '?retry_delay=1&connection_attempts=3')
        connection = pika.BlockingConnection(connectionParameters)
        AmqpClient.channel = connection.channel()
        #AmqpClient.channel.confirm_delivery()
        AmqpClient.channel.exchange_declare(exchange=AmqpClient.exchange_name, durable=True,
                                            exchange_type='direct')
        AmqpClient.queue = AmqpClient.channel.queue_declare(queue=AmqpClient.queue_name, durable=False)
        AmqpClient.channel.queue_bind(exchange=AmqpClient.exchange_name, queue=AmqpClient.queue_name,
                                      routing_key=AmqpClient.routing_key)
        print('Connection to the rabbitmq successfully.')

    def publish_message(self, *args):
        try:
            for message in args:
                ret = self.channel.basic_publish(exchange=AmqpClient.exchange_name,
                                           routing_key=AmqpClient.routing_key,
                                           properties=pika.BasicProperties(content_type='text/plain',
                                                                           delivery_mode=2),
                                           # 1 means Non-persistent， 2 means Persistent
                                           mandatory=True,
                                           # If rabbit don't know how to handle the message, it will return the message to this client.
                                           body=message)
                print(ret)
                self.channel.add_on_return_callback(on_message_rejected)
                print("Message published to message broker successfully.")
            return True
        except Exception as e:
            return False

    def subscribe_message(self):
        '''
        Subscribe all the messages in the specific queue
        :return: number of messages been subscribed
        '''
        print('Start to subscribe messages from rabbitmq broker.')
        message_consumed = 0
        try:
            message_count = AmqpClient.queue.method.message_count
            if message_count != 0:
                for method_frame, properties, body in self.channel.consume(AmqpClient.queue_name):
                    AmqpClient.channel.basic_ack(method_frame.delivery_tag)
                    message_consumed = message_consumed + 1
                    if message_consumed == message_count:
                        break
            print('%s messages received from borker.' % (message_consumed))

            return True, message_consumed
        except Exception as e:
            return False, 0

    def subscribe_one_message(self):
        '''
        Subscribe one message from message broker.
        :return: True if subscribe successfully, False if no message or exception happened.
                 this method will also return the body of message been subscribed.
        '''
        print('Start to subscribe message from rabbitmq broker.')
        try:
            method_frame, header_frame, body = self.channel.basic_get(AmqpClient.queue_name)
            if method_frame:
                print('%s messages received from borker.' % (body.decode("utf-8")))
                self.channel.basic_ack(method_frame.delivery_tag)
                return True, body.decode("utf-8")
            else:
                print('No message in the specific queue')
                return False, 'None'
        except Exception as e:
            print(e)
            return False, 'None'

    def on_message(self, channel, method_frame, header_frame, body):
        print(method_frame.delivery_tag)
        print('Message %s subscribed' % (body.decode("utf-8")))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def continuous_subscribe(self):
        # with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
        # executor.submit(self.subscribe)
        print('Start to subscribe message from rabbitmq broker.')
        self.channel.basic_consume(self.on_message, AmqpClient.queue_name)
        try:
            self.channel.start_consuming()
        except Exception as e:
            self.channel.stop_consuming()

    def destory(self):
        try:
            if self.connection != None:
                self.connection.close()
            print('Connection been destroyed.')
        except Exception as e:
            print(e)
