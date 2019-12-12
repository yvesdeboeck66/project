
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
        else:
            param[i] = -1*param[i]


    #make the entry & send it to the database
    dictmeasurement = {"RSSI": param}
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")  # Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["Measurement"]
    mycol.delete_many({})
    mycol.insert_one(dictmeasurement)  # {} --> eerste doc in collection, measurementset is een list van docs eigenlijk dus neem de 1ste doc uit de lijst
    print("Sent!")
    execfile("kNNAlgorithm.py")
    #To do: Check if dictmeasurement is created as intended


measurement = [0,0,0,0]
lastSentCounter = 0
msgCounter = 0

def on_message(client, userdata, message):
    global measurement, lastSentCounter, msgCounter

    #
    #   Parsing the Gateway & getting some information
    #
    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))
    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    currentCounter = payload_data[3]

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)
    gw_index = gateway_index(gw_name)


    #
    #   Checking if this message is already receiving new payload
    #   = If the current counter is not equal to the last sent counter +1, it means that not all four gateways
    #     received the previous packet & it should be sent with -1000 for the gateway that did not receive packet
    #
    #   Example: Packet with counter "3" is received by all gateways. The database is updated and the lastSentCounter
    #   is set to "3".
    #   The following packet with counter "4" is only received by three gateways, the database is not yet sent.
    #
    #   A new packet with counter "5" comes in, but the lastSentCounter is only '3'. THe program knows it need to
    #   send the information of packet "4" with the non-received gateway a RSSI of -1000. The
    #
    #



    if(currentCounter > (lastSentCounter+1)):
        print("Previous measurement (ctr "+str(lastSentCounter+1)+") not fully received. Only got "+str(msgCounter)+"messages. Pushing data to mongoDB!")
        sendToDatabase(measurement)
        lastSentCounter=lastSentCounter+1
        measurement = [0,0,0,0]
        msgCounter = 0
        print("\n")

    msgCounter = msgCounter + 1
    print("Message from " + gw_name+"("+str(msgCounter)+"e gateway)")
    print("Link budget: "+ str(payload_linkBudget))


    measurement[gw_index] = payload_linkBudget
    if(msgCounter >= 4):
        print("Got message from all four gateways. Pushing data to mongoDB.")
        sendToDatabase(measurement)
        lastSentCounter = lastSentCounter + 1
        measurement = [0,0,0,0]
        msgCounter = 0
        print("\n")

subscribe.callback(on_message, "/d7/4836383700470033/#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)


