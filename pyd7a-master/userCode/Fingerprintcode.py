
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time, datetime
import paho.mqtt.client as mqttclient
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



def on_message(client, userdata, message):

    print("\nNEW MESSAGE")

    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)


    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    print(" Gateway name: "+gateway_name(gateway_id)+" LB: "+str(payload_linkBudget))
    cases={"Gateway 1" : 1, "Gateway 2" : 2}
    measurement[cases.get(gateway_name(gateway_id))] = str(payload_linkBudget)

subscribe.callback(on_message, "/d7/4836383700470033/#", hostname="student-04.idlab.uantwerpen.be")

#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)
