A *Python* app which targetted to demo how to use the MQTT protocol to connect to a rabbitmq instance in the cloud foundry platform.

The app use the paho-mqtt library, so add paho-mqtt(https://www.eclipse.org/paho/) in your *requirements.txt*.

The app also use [Flask](https://flask.palletsprojects.com/en/1.1.x/) to expose endpoints to trigger the publish/subscribe operation, so finally, your *requirements.txt* will looks like below:

```yaml
Flask==0.12.2
Jinja2==2.9.6
paho-mqtt==1.3.1
```



By default, the rabbitmq service in the Bosch IoT Cloud has disabled the mqtt plugin, thus, in order to use the mqtt protocol,  the rabbitmq_mqtt plugin should be enabled.

```
cf update-service my-rabbitmq-service -c '{ "plugins": ["rabbitmq_mqtt"]}'
#or 
cf update-service my-rabbitmq-service -c PATH_TO_JSON_FILE
# the content of json file is:
# { "plugins": ["rabbitmq_mqtt"]}
```

it take few minutes(3-5 minutes) to make the change.

you can use *cf service my-rabbitmq-service* to check the update status:

```
cf service my-rabbitmq-service

Service instance: my-rabbitmq-service
Service: a9s-rabbitmq37
Bound apps: python-mqtt-rabbitmq,python-amqp-rabbitmq
Tags:
Plan: rabbitmq-single-small
Description: This is a service creating and managing dedicated RabbitMQ service instances, powered by the anynines Service Framework.
Documentation url: https://inside-docupedia.bosch.com/confluence/x/Q7mrKw
Dashboard: https://a9s-rabbitmq-dashboard.dashboards.cn1.bosch-iot-cloud.cn/service-instances/1a9e76bb-075a-43df-bf3d-75af6bc7505b

Last Operation
Status: update succeeded
Message:
Started: 2020-03-10T05:21:33Z
Updated: 2020-03-10T05:24:51Z
```



**How to use it:**

- Download and push the app to the cloud foundry platform.

  ```shell
  cf push -f manifest.yml
  ```

- Bind the rabbitmq service which has mqtt plugin enabled to the app.

- Restart the app. 

  

**How to test it:**

The app contains following urls:

- https://{link_to_app}/ : Display the publish and subscribe link

  

- https://{link_to_app}/mqtt/publish 
- https://{link_to_app}/mqtt/subscribe 

check the app log for more information.


The full code can be found in the [github](https://github.com/diaolanshan/python-rabbitmq-cf/tree/master/python-mqtt-rabbitmq-cf)