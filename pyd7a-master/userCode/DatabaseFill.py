
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, datetime
import paho.mqtt.client as mqttclient
from d7a.alp.parser import Parser as AlpParser
from bitstring import ConstBitStream
import pymongo

import logging

logging.basicConfig(level=logging.DEBUG)

def gateway_access_id(param):
    if param == "463230390032003e":
        return "RBgUaBO1TE9wwKO7uFSB"
    if param == "42373434002a0049":
        return "3QIBPaSGcqD4TvoVJwFO"
    if param == "433731340023003d":
        return "asyUKQEfgY7i7Yc5uDAL"
    if param == "4337313400210032":
        return "FKFDygGmIKScIaph0s7U"

def gateway_name(param):
    if param == "463230390032003e":
        return "Gateway1"
    if param == "42373434002a0049":
        return "Gateway2"
    if param == "433731340023003d":
        return "Gateway3"
    if param == "4337313400210032":
        return "Gateway4"

def gateway_index(param):
    cases={"Gateway1" : 0, "Gateway2" : 1, "Gateway3" : 2, "Gateway4": 3}
    return cases.get(param)

def sendToDatabase(param):

    #Fix the unknown data points
    for i in range(len(param)):
        if(param[i] == 0):
            param[i] = -1000

    #Get a location for the database
    location = input("What location did you test?")

    #make the entry & send it to the database
    dictmeasurement = {"RSSI": param, "location": location}
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["TrainingDatabase"]
    mycol.insert_one(dictmeasurement)  # {} --> eerste doc in collection, measurementset is een list van docs eigenlijk dus neem de 1ste doc uit de lijst
    #To do: Check if dictmeasurement is created as intended

msgCounter = 0
initMinute = 0
measurement = [0,0,0,0]

def on_message(client, userdata, message):
    global msgCounter, initMinute, measurement
    msgCounter = msgCounter + 1


    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)


    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    print("Message from " + gw_name)
    print("Link budget: "+ str(payload_linkBudget) + "\n")


    # TIME
    then = datetime.datetime.now()
    timeStamp = str(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)
    currentMinute = then.minute

    # We check if message have arrived in all four gateways by giving the broadcast a 2-second TTL
    # If the time difference from the initial message has not exceeded 2 seconds, check if message comes in
    # If after 2 seconds the counter is not 3, do 'IncorrectMeasurement' function with data you have
    # If after 2 seconds the counter is 3, send to mongoDB

    measurement[gateway_index(gw_name)] = payload_linkBudget

    # Debug#
    print(currentMinute - initMinute)

    if msgCounter <= 1:
        initMinute = currentMinute
        msgCounter = msgCounter + 1

    elif msgCounter < 4 & (currentMinute - initMinute) < 2:
        msgCounter = msgCounter + 1
        if msgCounter == 4 :
            sendToDatabase(measurement)
            msgCounter = 0
            measurement = [0,0,0,0]

    else:
        sendToDatabase(measurement)
        msgCounter = 0
        measurement = [0,0,0,0]


subscribe.callback(on_message, "/d7/4836383700470033/#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)


