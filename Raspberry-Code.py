import time 
import serial
import random
import uuid #para generar un ID a cada envio de datos
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient # para importar las librerias necesarias de SDK AWS
from datetime import date, datetime  #To get date and time
import Adafruit_DHT #Import DHT Library for sensor
myMQTTClient = AWSIoTMQTTClient("RishabClientID") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1l83aslu1wtwg-ats.iot.us-east-1.amazonaws.com", 8883)  #se configura el endpoint y el Puerto de aws 

myMQTTClient.configureCredentials("CA1.pem", "private.pem.key", "certificate.pem.crt") #en esta parte configuraremos las keys que se descargaron de AWS IoT Core
myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Initiating Realtime Data Transfer From Raspberry Pi...')
myMQTTClient.connect() #se intenta la comunicacion con aws
sensor_name = Adafruit_DHT.DHT11 #we are using the DHT11 sensor
sensor_pin = 17 #The sensor is connected to GPIO17 on Pi
while 1: #Infinite Loop
    now = datetime.now() #get date and time
    current_time = now.strftime('%Y-%m-%d/%H:%M:%S') #get current time in string format
    ID=str(uuid.uuid4())
    humidity, temperature = Adafruit_DHT.read_retry(sensor_name, sensor_pin)     #read from sensor
  #prepare the payload in string format
    payload = '{ "Id": "' + ID + '", "timestamp": "' + current_time + '","temperature": ' + str(temperature) + ',"humidity": '+ str(humidity) + ' }'
    print (payload) #print payload for reference 
    myMQTTClient.publish("DHT11/data", payload, 0) #publish the payload
