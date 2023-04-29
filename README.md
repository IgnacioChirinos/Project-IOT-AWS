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

<img src="https://github.com/IgnacioChirinos/Project-IOT-AWS/blob/main/DataFlow.PNG"  width="800" height="250">

1. **IoT Core**

Se comenzará realizando las configuraciones necesarias en AWS IoT Core

- Iniciaremos pasando a la sección de Seguridad y en la opción de políticas crearemos una política de combinación que luego conectaremos al objeto creado, para el caso usaremos \* para determinar que es una política de uso sin restricciones.

- En la parte de “Todos los dispositivos” en la opción de objetos (Things) se pondrá la opción de crear un nuevo objeto. Para el caso de la implementación usaremos la creación de un único objeto.

- Usaremos la opción de generar automáticamente un certificado nuevo, con eso AWS nos generará algunos certificados que debemos descargar. Se recomienda guardar los certificados en una carpeta para tenerlos todos juntos.


2. **Configuración de la Raspberry Pi**

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


- Pasaremos en el mismo código a configurar la leída de datos del sensor DHT11 y crear un ID y el tiempo en que se toma cada muestra para pasar a enviar todos estos datos en el formato para que lo entienda el protocolo MQTT.


3. **Configuración de Lambda**
- Para la configuración de AWS Lambda Iniciaremos creado una función Lambda. En este ejemplo uso JSON como código para la función. Pero antes de configurar el código iremos a conectarla a IoT Core.

- Para esto vamos a necesitar configurar el motor de reglas para ello iremos a direccionamiento de mensajería, y en reglas crearemos una nueva. Para poder crear una regla se necesita usar el formato SQL. Para este proyecto se usará la regla [select \* from 'DHT11/data'] y en la parte de acciones escogeremos Lambda y la función Lambda que creamos.

Ahora regresaremos a la función Lambda y en la parte del código se usó el siguiente.


4. **Configuración de DynamoDB**
- La configuración en Dynamo tiene que estar en regla al código que se usa en la función Lambda. Para esto la clave de participación y la clave de ordenación tienen que ser las mismas que en el código JSON. En este caso se uso serialNumber y timeStamp. Los demás valores de la tabla se pueden configurar al gusto. Pero en el proyecto se usó Temperatura y Humedad.


5. **Resultados**

Lo que se espera en DynamoDB al correr en el código en Raspberry es lo siguiente.
<img src="https://github.com/IgnacioChirinos/Project-IOT-AWS/blob/main/Resultados.PNG"  width="600" height="300">

