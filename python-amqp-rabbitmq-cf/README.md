A *Python* app which targetted to demo how to use the AMQP protocol to connect to a rabbitmq instance in the cloud foundry platform.

The app use the pika library, so add [pika](https://pika.readthedocs.io/en/stable/) in your *requirements.txt*.

The app also use [Flask](https://flask.palletsprojects.com/en/1.1.x/) to expose a endpoint to trigger the publish/subscribe operation, so finally, your *requirements.txt* will looks like below:

```yaml
Flask>0.12.2
Jinja2>2.9.6
pika>0.11.0
```



**How to use it:**

- Download and push the app to the cloud foundry platform.

  ```shell
  cf push -f manifest.yml
  ```

- Provision an rabbitmq instance and bind to the app.

- Restart/Restage the app.

- 

**How to test it:**

The app contains following urls:

- http://{link_to_app}/, show the links to publish message and subscribe message.

- http://{link_to_app}/amqp/publish, publish a message to the queue: _com.bosch.de.bics.demo.queue_
- http://{link_to_app}/amqp/subscribe, subscribe a message from the queue: _com.bosch.de.bics.demo.queue_

and check the app log for more information after you triggered the urls above.



**Setup the connection and queue:**

```python
exchange_name = "com.bosch.de.bics.demo.exchange"
    queue_name = "com.bosch.de.bics.demo.queue"
    routing_key = "com.bosch.de.bics.demo.routingKey"

    def __init__(self):
        try:
            vcap_services = json.loads(os.environ['VCAP_SERVICES'])
            if vcap_services != None:
                for service in vcap_services.keys():
                    if 'rabbitmq' in vcap_services[service][0]['tags']:
                        # Use the first 'rabbitmq' service.
                        uri = vcap_services[service][0]['credentials']['protocols']['amqp']['uri']
                        break

            connectionParameters = pika.URLParameters(uri + '?retry_delay=1&connection_attempts=3')
            connection = pika.BlockingConnection(connectionParameters)
            AmqpClient.channel = connection.channel()
            # AmqpClient.channel.confirm_delivery()
            AmqpClient.channel.exchange_declare(exchange=AmqpClient.exchange_name, durable=True,
                                                exchange_type='direct')
            AmqpClient.queue = AmqpClient.channel.queue_declare(queue=AmqpClient.queue_name, durable=False)
            AmqpClient.channel.queue_bind(exchange=AmqpClient.exchange_name, queue=AmqpClient.queue_name,
                                          routing_key=AmqpClient.routing_key)
            print('Connect to the rabbitmq successfully.')

        except UnboundLocalError as e:
            print('Probably no rabbitmq service been binded to the app ?')
            raise Exception("Can not setup connection to rabbitmq, because: ".format(e.message))
```

**Publish message:**
```python
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
            self.channel.add_on_return_callback(on_message_rejected)
            print("Message published to message broker successfully.")
            return True
        except Exception as e:
            raise e
```

**subscribe message:**
```python
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
```

Alternatively,  if you want to subscribe just one message from the queue, call *subscribe_one_message* which also in the AmqpClient class.

If you want to listen to queue, call *continuous_subscribe*.

The full code can be found in the [github](https://github.com/diaolanshan/python-rabbitmq-cf/tree/master/python-amqp-rabbitmq-cf).

