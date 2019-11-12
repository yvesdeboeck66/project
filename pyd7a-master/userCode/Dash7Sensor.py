
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

import paho.mqtt.client as mqttclient
from d7a.alp.parser import Parser as AlpParser
from bitstring import ConstBitStream

import logging

logging.basicConfig(level=logging.DEBUG)


def on_message(client, userdata, message):

    print("\nNEW MESSAGE")
    print("Topic: "+message.topic)
    print("ALP payload: "+message.payload)

    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    print("Link budget: "+ str(payload_linkBudget))
    print("--- Message Payload ---")
    for i in range(len(payload_data)):
        print("Byte "+str(i)+": "+str(payload_data[i]))
    print("--- End of payload ---")
    print("END OF MESSAGE")

    tbMessage = "{\"Temperature\":"+str(payload_data[0])+",\"humidity\":"+str(payload_data[1])+"}"
    print("tbMessage: "+tbMessage)

    publish.single("information", tbMessage, hostname="thingsboard.idlab.uantwerpen.be", port=1883, auth={'username': 'group3@lopow.iot.com', 'password': 'lopowiot3'})
    print("Published!")



publish.single("information", "{\"Temperature\":10}", hostname="thingsboard.idlab.uantwerpen.be", port=1883,
               auth={'username': 'group3@lopow.iot.com', 'password': 'lopowiot3'})


subscribe.callback(on_message, "#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)


