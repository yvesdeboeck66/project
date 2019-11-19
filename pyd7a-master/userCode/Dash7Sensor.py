
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
    print("Topic: "+message.topic)
    print("ALP payload: "+message.payload)

    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)


    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    print("Link budget: "+ str(payload_linkBudget))
    print("--- Message Payload ---")
    for i in range(len(payload_data)):
        print("Byte "+str(i)+": "+str(payload_data[i]))
    print("--- End of payload ---")
    #print("END OF MESSAGE")

    # TIME
    then = datetime.datetime.now()
    timeStamp = str(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)
    # -----

    #Here we try to assign each value. If the payload is smaller than expected, fill all other values with 0
    ctr = 6 #Might be 7 later
    try:
        temp = str(payload_data[6-ctr])
        ctr = ctr - 1
        hum = str(payload_data[6-ctr])
        ctr = ctr - 1
        reps = str(payload_data[6-ctr])
        ctr = ctr - 1
        name = str(payload_data[6-ctr])
        ctr = ctr - 1
        weight = str(payload_data[6-ctr])
        ctr = ctr - 1
        goToSleep = str(payload_data[6-ctr])
        #ctr = ctr + 1
        #isRepping = str(payload_data[ctr])

    except:
        print("INVALID PAYLOADS! failed at value "+str(6-ctr)+"... Expected 6 values in payload! Filling all following values with 0")
        goToSleep = "0"
        ctr = ctr - 1
        if ctr > 0:
            weight = "0"
            ctr = ctr -1
        if ctr > 0:
            name = "0"
            ctr = ctr - 1
        if ctr > 0:
            name = "0"
            ctr = ctr - 1
        if ctr > 0:
            reps = "0"
            ctr = ctr - 1



    print("Timestamp= "+str(timeStamp))
    print("Gateway name: "+gateway_name(gateway_id))
    print("Gateway ID: "+gateway_access_id(gateway_id))


    tbMessage="{\""+gw_name+"\":[{\"ts\":"+timeStamp+",\"values\": {\"Temperature\": "+temp+",\"Humidity\":"+hum+",\"Reps\":"+reps+",\"Name\":"+name+",\"Weight\":"+weight+",\"goToSleep\":"+goToSleep+"}}]}"

    #tbMessage="{\""+gateway_name(gateway_id)+"\":[{\"ts\":"+timeStamp+",\"values\": {\"Temperature\": "+str(payload_data[0])+",\"Humidity\":"+str(payload_data[1])+",\"Reps\":"+str(payload_data[2])+"}}]}"

    #tbMessage = "{\""+gateway_name(gateway_id)+"\":{\"Temperature\":"+str(payload_data[0])+",\"humidity\":"+str(payload_data[1])+"}}"

    #tbMessage = "{\""+gateway_name(gateway_id)+"\": [{\"values\":{\"Temperature\":"+str(payload_data[0])+",\"Humidity\":"+str(payload_data[1])+"}}]}"
    print("tbMessage: "+tbMessage)

    publish.single("v1/gateway/telemetry", tbMessage, hostname="thingsboard.idlab.uantwerpen.be", port=1883, auth={'username': gw_access_id})
    print("Published to Access ID "+gw_access_id+"!")



#publish.single(" v1/gateway/connect", "{\"device\":\"Device1\"}", hostname="thingsboard.idlab.uantwerpen.be", port=1883,
               #auth={'username': 'NMnF1RCV1m5BS4GYyDQw'})


subscribe.callback(on_message, "/d7/4836383700470033/#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)


