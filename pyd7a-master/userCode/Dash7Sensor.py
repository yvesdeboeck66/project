
import paho.mqtt.subscribe as subscribe
import time, datetime
from d7a.alp.parser import Parser as AlpParser
import paho.mqtt.publish as publish

from bitstring import ConstBitStream
import math
import operator
import pymongo
import threading

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


# ---------------------------------------------------------------------------------------------
# -------------------------------------------K N N---------------------------------------------
# ---------------------------------------------------------------------------------------------

def getmongodata():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["MergedCollection"]
    myquery = {}                                                    #Lege query --> zoek alles
    mydoc = mycol.find(myquery)                                     #alle docs in collection
    set=[]
    for x in mydoc:
        set.append(x)                                               #steek alle docs in een lijst
    return set

def euclideanDistance(instance1, instance2, length):                #Berekenen van euclidische afstand
    distance = 0
    for x in range(length):
        distance += pow((int(instance1[x]) - int(instance2[x])), 2)
    return int(math.sqrt(distance))

def getNeighborsDB(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance['RSSI'])
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance['RSSI'], trainingSet[x]["RSSI"], length)   #euclidische afstanden in een nieuwe lijst steken
        distances.append((trainingSet[x], dist))                                            #Sorteer de lijst op kleinste afstand
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x])                                                      #steek de K kleinste afstanden in een nieuwe lijst
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

# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------




def location():
    global lastSentCounter, msgCounter, measurement, readyToSend
    print("Test")

    for i in range(len(measurement)):
        if(measurement[i] == 0):
            measurement[i] = -1000
        else:
            measurement[i] = -1*measurement[i]


    # Find location using kNN
    dictmeasurement = {"RSSI": measurement}
    neighbors = getNeighborsDB(trainingSet, dictmeasurement, k)
    location = estimation(neighbors, k)
    print("Test")
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

    print("Test")
    tbMessage="{\""+gw_name+"\":[{\"ts\":"+timeStamp+",\"values\": {\"Temperature\": "+temp+",\"Humidity\":"+hum+",\"Reps\":"+reps+",\"Name\":"+name+",\"Weight\":"+weight+",\"goToSleep\":"+goToSleep+",\"location\":"+location+ "}}]}"

    
    #DEBUG prints
    print("---- Message is being sent ----")
    print("Amount of messages : " + str(msgCounter))
    print("measurements:\n 1: "+str(measurement[0]) +"\n2: "+str(measurement[1])+"\n3: "+str(measurement[2])+"\n4: "+str(measurement[3]))
    print("Found location: "+str(location))
    print("---- SENT ----")


    # Send to thingsboard
    publish.single("v1/gateway/telemetry", tbMessage, hostname="thingsboard.idlab.uantwerpen.be", port=1883, auth={'username': gw_access_id})

    lastSentCounter = lastSentCounter + 1
    msgCounter = 0
    measurement=[0,0,0,0]
    readyToSend = False


def on_message(client, userdata, message):
    global measurement, lastSentCounter, msgCounter, debug, timer, readyToSend, payload_data, gw_name, gw_access_id

    #
    #   Parsing the Gateway & getting some information
    #
    dataByteArray = bytearray(message.payload.decode("hex"))
    payload = AlpParser().parse(ConstBitStream(dataByteArray), len(dataByteArray))

    gateway_id = message.topic.split("/")[3]
    gw_name = gateway_name(gateway_id)
    gw_access_id = gateway_access_id(gateway_id)
    gw_index = gateway_index(gw_name)

    payload_data = payload.actions[0].operand.data
    payload_linkBudget = payload.interface_status.operation.operand.interface_status.link_budget
    currentCounter = payload_data[3]

    print("Link budget: "+ str(payload_linkBudget))



    # Condition: First time
    if(lastSentCounter == -1):
        lastSentCounter = currentCounter -1
        print("Initialized at counter "+str(currentCounter))


    # Condition : New Message came in before previous was correctly handled & before timer: Stop timer & send to mongoDB
    if(currentCounter > (lastSentCounter+1)):
        if(msgCounter > 0):
            print("Previous measurement ("+str(lastSentCounter+1)+") not fully received. Only got "+str(msgCounter)+"/4 messages. Pushing data to mongoDB!")
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
        print("...")

    msgCounter = msgCounter + 1
    print("Message from " + gw_name)
    print("Link budget: "+ str(payload_linkBudget))


    measurement[gw_index] = payload_linkBudget
    if(msgCounter >= 4):
        print("Got message from all four gateways. Pushing data to mongoDB.")
        timer.cancel()
        location()



trainingSet = getmongodata()
print(trainingSet[0])
print(trainingSet[0]['RSSI'])
k = 9
readyToSend = False
lastSentCounter = -1
measurement = [0,0,0,0]
msgCounter = 0
timer = threading.Timer(5.0, location)

subscribe.callback(on_message, "/d7/4836383700400043/#", hostname="student-04.idlab.uantwerpen.be")



#client1 = mqttclient.Client("student03server")
#client1.connect("http://student-03.idlab.uantwerpen.be", 8080, keepalive=600)




