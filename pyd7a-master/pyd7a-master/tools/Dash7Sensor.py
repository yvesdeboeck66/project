
import paho.mqtt.subscribe as subscribe
from d7a.alp.parser import Parser as AlpParser
from bitstring import ConstBitStream



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
    #print("Received message payload: " + payload.actions[0].operand.data)


subscribe.callback(on_message, "#", hostname="student-04.idlab.uantwerpen.be")
