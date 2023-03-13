# Project-IOT-AWS
Ignacio Chirinos Palacios (Solutions Architect Intern) 

Caleidos Media SAC

**Implementación de un sensor de humedad y temperatura “DHT11” con los servicios de AWS IoT**

En el siguiente proyecto se verá cómo se realizó la implementación de un framework simple que intenta explicar de forma práctica los servicios principales de AWS IoT.

Para realizar el siguiente proyecto se necesitará los siguientes materiales:

- Raspberry Pi (En este caso se usó el modelo 3 B+)
- Sensor DHT11
- Cuenta de AWS

El framework utilizado será el siguiente:

1. **IoT Core**

Se comenzará realizando las configuraciones necesarias en AWS IoT Core

- Iniciaremos pasando a la sección de Seguridad y en la opción de políticas crearemos una política de combinación que luego conectaremos al objeto creado, para el caso usaremos \* para determinar que es una política de uso sin restricciones.

- En la parte de “Todos los dispositivos” en la opción de objetos (Things) se pondrá la opción de crear un nuevo objeto. Para el caso de la implementación usaremos la creación de un único objeto.

- Usaremos la opción de generar automáticamente un certificado nuevo, con eso AWS nos generará algunos certificados que debemos descargar. Se recomienda guardar los certificados en una carpeta para tenerlos todos juntos.


1. **Configuración de la Raspberry Pi**

En este tutorial se sobre entiende que la Raspberry Pi ya está cargada con el sistema operativo Debian. 

- Iniciaremos enviando los certificados descargados a través del protocolo FTP o por algún medio virtual. No se recomienda el uso de un USB para mandarlos en la prueba genera errores. 

- El siguiente paso será descargar las librerías SDK necesarias para poder comunicar el dispositivo con AWS IoT Core. Lo realizamos en el Terminal 
- cd ~

python3 -m pip install awsiotsdk

- git clone <https://github.com/aws/aws-iot-device-sdk-python>
- python setup.py install
- El siguiente paso será descargar las librerías necesarias para que las Raspberry entienda la comunicación con el sensor DHT11 lo realizamos en el Terminal
- wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
- sudo python3 raspi-blinka.py
- pip3 install adafruit-circuitpython-dht
- sudo apt-get install libgpiod2

Ahora deberemos configurar el código para realizar el envió de mensaje con AWS. En este caso usaremos Python para dicha comunicación. Por lo tanto creamos un archivo .py e ingresamos lo siguiente. 

import time 

import serial

import random

import uuid #para generar un ID a cada envio de datos

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # para importar las librerias necesarias de SDK AWS

from datetime import date, datetime  #To get date and time

import Adafruit\_DHT #Import DHT Library for sensor

myMQTTClient = AWSIoTMQTTClient("RishabClientID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT

myMQTTClient.configureEndpoint("a1l83aslu1wtwg-ats.iot.us-east-1.amazonaws.com", 8883)  #se configura el endpoint y el Puerto de aws 

myMQTTClient.configureCredentials("/home/ignacio/AWSIoT/CA1.pem", "/home/ignacio/AWSIoT/8a86574c5e64a49aedad614b4ff7e564c2313c01e942375afaf5c0400fd67c66-private.pem.key", "/home/ignacio/AWSIoT/8a86574c5e64a49aedad614b4ff7e564c2313c01e942375afaf5c0400fd67c66-certificate.pem.crt") #en esta parte configuraremos las keys que se descargaron de AWS IoT Core

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing

myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz

myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec

myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec

print ('Initiating Realtime Data Transfer From Raspberry Pi...')

myMQTTClient.connect() #se intenta la comunicacion con aws

- Pasaremos en el mismo código a configurar la leída de datos del sensor DHT11 y crear un ID y el tiempo en que se toma cada muestra para pasar a enviar todos estos datos en el formato para que lo entienda el protocolo MQTT.

sensor\_name = Adafruit\_DHT.DHT11 #we are using the DHT11 sensor

sensor\_pin = 17 #The sensor is connected to GPIO17 on Pi

while 1: #Infinite Loop

`    `now = datetime.now() #get date and time

`    `current\_time = now.strftime('%Y-%m-%d/%H:%M:%S') #get current time in string format

`    `ID=str(uuid.uuid4())

`    `humidity, temperature = Adafruit\_DHT.read\_retry(sensor\_name, sensor\_pin)     #read from sensor

`  `#prepare the payload in string format

`    `payload = '{ "Id": "' + ID + '", "timestamp": "' + current\_time + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' }'

`    `print (payload) #print payload for reference 

`    `myMQTTClient.publish("DHT11/data", payload, 0) #publish the payload

1. **Configuración de Lambda**
- Para la configuración de AWS Lambda Iniciaremos creado una función Lambda. En este ejemplo uso JSON como código para la función. Pero antes de configurar el código iremos a conectarla a IoT Core.

- Para esto vamos a necesitar configurar el motor de reglas para ello iremos a direccionamiento de mensajería, y en reglas crearemos una nueva. Para poder crear una regla se necesita usar el formato SQL. Para este proyecto se usará la regla [select \* from 'DHT11/data'] y en la parte de acciones escogeremos Lambda y la función Lambda que creamos.

Ahora regresaremos a la función Lambda y en la parte del código se usó el siguiente.

console.log('Loading function');

const AWS = require('aws-sdk');

const dynamo = new AWS.DynamoDB.DocumentClient();

const collection ="IoTCatalog"

// Handler lamda function

exports.handler = function(event, context) {

console.log('Received event:', JSON.stringify(event, null, 2));

`   `const params = {

`    `TableName: collection,

`    `Item:{

`        `"serialNumber": event.Id,

`        `"timeStamp": event.timestamp,

`        `"Temperatura": event.temperature,

`        `"Humedad": event.humidity

`        `}

`    `};

`    `console.log("Saving Telemetry Data");

`    `dynamo.put(params, function(err, data) {

`        `if (err) {

`            `console.error("Unable to add device. Error JSON:", JSON.stringify(err, null, 2));

`            `context.fail();

`        `} else {

`            `console.log(data)

`            `console.log("Data saved:", JSON.stringify(params, null, 2));

`            `context.succeed();

`            `return {"message": "Item created in DB"}

`        `}

`    `});

}




1. **Configuración de DynamoDB**
- La configuración en Dynamo tiene que estar en regla al código que se usa en la función Lambda. Para esto la clave de participación y la clave de ordenación tienen que ser las mismas que en el código JSON. En este caso se uso serialNumber y timeStamp. Los demás valores de la tabla se pueden configurar al gusto. Pero en el proyecto se usó Temperatura y Humedad.


1. **Resultados**

Lo que se espera en DynamoDB al correr en el código en Raspberry es lo siguiente.




