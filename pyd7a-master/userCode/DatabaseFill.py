
import paho.mqtt.subscribe as subscribe
import time
import paho.mqtt.publish as publish
import time, datetime
import paho.mqtt.client as mqttclient
import pymongo
from d7a.alp.parser import Parser as AlpParser
from bitstring import ConstBitStream

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

flag=False
start=0
counter = 0
initTime = datetime.datetime.now()

def on_message(client, userdata, message):
    print("in onmessage")
    global flag,start, measurement, counter, initTime
    if flag==False :
        start = time.time()
    flag=True

    # If the time difference from the initial message has not exceeded 2 seconds, check if message comes in
    # If after 2 seconds the counter is not 3, do 'IncorrectMeasurement' function with data you have
    # If after 2 seconds the counter is 3, send to mongoDB
    timeDiff = initTime.timeDelta


    print("NEW MESSAGE")
    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))
    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)
    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    print("Gateway : "+ gw_name+" Link budget: "+ str(payload_linkBudget))
    cases={"Gateway1" : 0, "Gateway2" : 1, "Gateway3" : 2, "Gateway4": 3}
    measurement[cases.get(gw_name)] = payload_linkBudget

def WriteMongo():
    for i in measurement:
        if(i==0):
            i=-1000
    location=input("Give location plz")
    dictmeasurement={"RSSI":measurement,"location":location}
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["TrainingDatabase"]
    mycol.insert_one(dictmeasurement)  # {} --> eerste doc in collection, measurementset is een list van docs eigenlijk dus neem de 1ste doc uit de lijst
    return 0


print("begin")
measurement=[0,0,0,0]
subscribe.callback(on_message, "/d7/4836383700470033/#", hostname="student-04.idlab.uantwerpen.be")


print("na callback")
while(1):
    print("In de while loop")
    end = time.time()
    if(end-start>3):
        start=0
        flag= False
        WriteMongo()
        measurement = [0, 0, 0, 0]

