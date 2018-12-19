A *Python* app which target to demo how to use the MQTT protocol to connect to a rabbitmq instance in the cloud foundry platform.

The app use the paho-mqtt library, so add paho-mqtt(https://www.eclipse.org/paho/) in your *requirements.txt*

**How to use it:**

- Download and push the app to the cloud foundry platform.
- Provision an rabbitmq instance and bind to the app.
- Copy the cacrt information from the Environment Variables and save it to a file called cacrt.crt in the same directory of the app.
- push the app again.

**How to test it:**

The app contains following urls,

- http://{link_to_app}/mqtt/publish 
- http://{link_to_app}/mqtt/subscribe 

check the app log for more information.
 

the full code can be found in the [github](https://github.com/diaolanshan/python-rabbitmq-cf/tree/master/python-mqtt-rabbitmq-cf)