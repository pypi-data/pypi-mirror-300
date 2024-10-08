# Messaging Service Client SDK


Client library for accessing the SmartOcean ingestion and core messaging services.

The messaging services rely on the [MQTT Standard](https://mqtt.org/) 

This client SDK implementation utilises the [Paho MQTT](https://pypi.org/project/paho-mqtt/) library. The Paho MQTT library may also be used directly to access the messaging services in case more advanced use is required.

## Sample Client Code

A sample implementation accessing the messaging service is available in the [sample.py](subscriber_sample.py) script.

## Credentials

Credentials for accessing the service being consumed must be placed in a `.env` file with the following content

```
MESSAGE_SERVICE_USERNAME=<username>
MESSAGE_SERVICE_PASSWORD=<password>
```

