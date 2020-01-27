
import paho.mqtt.subscribe as subscribe
import time, datetime
from d7a.alp.parser import Parser as AlpParser
import paho.mqtt.publish as publish

import ttn


from bitstring import ConstBitStream
import math
import operator
import pymongo
import threading

import logging


# ----------------------------------
# Constants
# ----------------------------------
app_id = "woutor_antenne_bzzt"
access_key = "ttn-account-v2.a8uKxf524Yuc5cK5vE5Pp1sgVw_AXsAv8wxujwmObC8"

logging.basicConfig(level=logging.DEBUG)

gateway_access_id_D7 = "7P7BkK9ZDEHU805l4APK"
gateway_access_id_LW = "YYXWy8ORvnm2WBPRGqi2"
gateway_name_LW = "LORAWANGATEWAY"
gateway_name_D7 = "DASH7GATEWAY"

# ----------------------------------
# Conversion functions
#
# They map the gateway ID to the access ID or the name
# ----------------------------------

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

def locationConverter(param):
    xy = []
    cases = {
        "1" : [0.183, 0.398],
        "2" : [0.183, 0.261],
        "3" : [0.183, 0.189],
        "4" : [0.259, 0.398],
        "5" : [0.259, 0.261],
        "6" : [0.259, 0.189],
        "7" : [0.335, 0.398],
        "8" : [0.335, 0.261],
        "9" : [0.335, 0.189],
        "10" : [0.423, 0.398],
        "11" : [0.423, 0.261],
        "12" : [0.423, 0.189],
        "13" : [0.509, 0.398],
        "14" : [0.509, 0.261],
        "15" : [0.509, 0.189],
        "16" : [0.585, 0.398],
        "17" : [0.585, 0.261],
        "18" : [0.585, 0.189],
        "19" : [0.665, 0.398],
        "20" : [0.665, 0.261],
        "21" : [0.665, 0.189],
        "22" : [0.183, 0.485],
        "23" : [0.183, 0.571],
        "24" : [0.183, 0.661],
        "25" : [0.250, 0.485],
        "26" : [0.250, 0.571],
        "27" : [0.250, 0.661],
        "28" : [0.317, 0.485],
        "29" : [0.317, 0.571],
        "30" : [0.317, 0.661],
        "31" : [0.384, 0.485],
        "32" : [0.384, 0.571],
        "33" : [0.384, 0.661],
        "34" : [0.452, 0.485],
        "35" : [0.452, 0.571],
        "36" : [0.452, 0.661],
        "37" : [0.523, 0.485],
        "38" : [0.523, 0.571],
        "39" : [0.523, 0.661],
        "40" : [0.592, 0.485],
        "41" : [0.592, 0.571],
        "42" : [0.592, 0.661]
    }
    a = cases.get(param, {0,0})
    return a

# ---------------------------------------------------------------------------------------------
# -------------------------------------------K N N---------------------------------------------
# ---------------------------------------------------------------------------------------------

def getmongodata():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #Connect with database
    mydb = myclient["IOT"]
    mycol = mydb["MergedCollection"]
    myquery = {}                                                    # Empty query --> Search everything
    mydoc = mycol.find(myquery)                                     # All documents in collections
    set=[]
    for x in mydoc:
        set.append(x)                                               # Convert to list
    return set

def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((int(instance1[x]) - int(instance2[x])), 2)
    return int(math.sqrt(distance))

def getNeighborsDB(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance['RSSI'])
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance['RSSI'], trainingSet[x]["RSSI"], length)   # Dist in new list
        distances.append((trainingSet[x], dist))                                         # Sort on smallest dist
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x])                                                      # K smallest distances in new list
    return neighbors

def estimation(neighbors,k):
    locations = []
    for i in range(k):
        locations.append(neighbors[i][0]["location"])               #Steek de locations in een apparte lijst
    counter = 0
    num = locations[0]
    for i in locations:
        currentcount=locations.count(i)                             #Tel het aantal keer dat het huidig getal voorkomt in de lijst
        if(currentcount>counter):                                   #Als het aantal groter is dan het vorig aantal dan updaten
            counter = currentcount
            num = i
    return num





# --------------------------------------- Location --------------------------------------------
# This function is called whenever the location of an incoming message has to be calculated.
# It will change all non-received messages to "-1000 dB" and start to fill in the payload
# It will then compose a tbMessage in JSON format with all the parameters as well as the
# timestamp.
# After doing this, it sends the message to thingsboard & resets the global variables
# ---------------------------------------------------------------------------------------------

def location():
    global lastSentCounter, msgCounter, measurement, readyToSend

    for i in range(len(measurement)):
        if(measurement[i] == 0):
            measurement[i] = -1000
        else:
            measurement[i] = -1*measurement[i]


    # Find location using kNN
    dictmeasurement = {"RSSI": measurement}
    neighbors = getNeighborsDB(trainingSet, dictmeasurement, k)
    location = estimation(neighbors, k)
    x, y = locationConverter(str(location))

    # Get information out of message

    then = datetime.datetime.now()
    timeStamp = str(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)

    ctr = 6  # Might be 7 later
    try:
        temp = str(payload_data[6 - ctr])
        ctr = ctr - 1
        hum = str(payload_data[6 - ctr])
        ctr = ctr - 1
        reps = str(payload_data[6 - ctr])
        ctr = ctr - 1
        name = str(payload_data[6 - ctr])
        ctr = ctr - 1
        weight = str(payload_data[6 - ctr])
        ctr = ctr - 1
        goToSleep = str(payload_data[6 - ctr])
        # ctr = ctr + 1
        # isRepping = str(payload_data[ctr])

    except:
        print("INVALID PAYLOADS! failed at value " + str(
            6 - ctr) + "... Expected 6 values in payload! Filling all following values with 0")
        goToSleep = "0"
        ctr = ctr - 1
        if ctr > 0:
            weight = "0"
            ctr = ctr - 1
        if ctr > 0:
            name = "0"
            ctr = ctr - 1
        if ctr > 0:
            name = "0"
            ctr = ctr - 1
        if ctr > 0:
            reps = "0"
            ctr = ctr - 1

    tbMessage="{\""+gateway_name_D7+"\":[{\"ts\":"+timeStamp+",\"values\": {\"Temperature\": "+temp+",\"Humidity\":"+hum+",\"Reps\":"+reps+",\"Name\":"+name+",\"Weight\":"+weight+",\"goToSleep\":"+goToSleep+",\"x\":"+str(x)+",\"y\":"+ str(y)+",\"IsStolen\":"+"False"+"}}]}"


    #DEBUG prints
    print("---- Message is being sent ----")
    print("Amount of messages : " + str(msgCounter))
    print("measurements:\n 1: "+str(measurement[0]) +"\n2: "+str(measurement[1])+"\n3: "+str(measurement[2])+"\n4: "+str(measurement[3]))
    print("Found location: "+str(location))
    print("---- SENT ----")


    # Send to thingsboard
    publish.single("v1/gateway/telemetry", tbMessage, hostname="thingsboard.idlab.uantwerpen.be", port=1883, auth={'username': gateway_access_id_D7})

    lastSentCounter = lastSentCounter + 1
    msgCounter = 0
    measurement=[0,0,0,0]
    readyToSend = False

# --------------------------------------- Callbacks --------------------------------------------
# on_message and on_message_lora are the callback functions that are called whenever the
# D7 or lorawan (respectively) broker sends a message that we're subscribed to.

# !!! On_message has 3 criteria to send the data to thingsboard !!!
# 1) All 4 gateways received the message -> best case
# 2) The 5 second timer, waiting for the 4 gateways, has passed
# 3) A new message (with a higher message counter) comes in before the 4 messages are received and
#    no 5 seconds have passed
# ---------------------------------------------------------------------------------------------
def on_message(client, userdata, message):
    global measurement, lastSentCounter, msgCounter, debug, timer, readyToSend, payload_data, gw_name

    #
    #   Parsing the Gateway & getting some information
    #
    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_index = gateway_index(gw_name)

    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    currentCounter = payload_data[3]




    # Condition: First time
    if(lastSentCounter == -1):
        lastSentCounter = currentCounter -1
        print("Initialized at counter "+str(currentCounter))


    # Condition : New Message came in before previous was correctly handled & before timer: Stop timer & send to mongoDB
    if(currentCounter > (lastSentCounter+1)):
        if(msgCounter > 0):
            print("Previous measurement ("+str(lastSentCounter+1)+") not fully received. Only got "+str(msgCounter)+"/4 messages.")
            timer.cancel()
            location()
        else:
            # 0/4 received -> don't send.
            lastSentCounter = currentCounter - 1


    # First message
    if(msgCounter == 0):
        if(timer.isAlive()):
            print("WAT WAT")
            timer.cancel()
        print("Starting timer")
        timer = threading.Timer(5.0, location)
        timer.start()


    msgCounter = msgCounter + 1
    print("Message from " + gw_name)
    print("Link budget: "+ str(payload_linkBudget))


    measurement[gw_index] = payload_linkBudget
    if(msgCounter >= 4):
        print("Got message from all four gateways. Pushing data to mongoDB.")
        timer.cancel()
        location()


def on_message_lora(msg, client):
    then = datetime.datetime.now()
    timeStamp = str(time.mktime(then.timetuple())*1e3 + then.microsecond/1e3)
    tbMessage = "{\"" + gateway_name_D7 + "\":[{\"ts\":" + timeStamp + ",\"values\": {\"IsStolen\": "+"True"+"}}]}"
    publish.single("v1/gateway/telemetry", tbMessage, hostname="thingsboard.idlab.uantwerpen.be", port=1883, auth={'username': gateway_access_id_D7})
#LoraWan
handler = ttn.HandlerClient(app_id, access_key)
mqtt_client_lora = handler.data()
mqtt_client_lora.set_uplink_callback(on_message_lora)
mqtt_client_lora.connect()


trainingSet = getmongodata()

k = 9
readyToSend = False
lastSentCounter = -1
measurement = [0,0,0,0]
msgCounter = 0
timer = threading.Timer(5.0, location)

subscribe.callback(on_message, "/d7/4836383700260037/#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)




