import math
import operator
import pymongo

def getmongodata():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["TrainingDatabase"]
    myquery = {}                                                    #Lege query --> zoek alles
    mydoc = mycol.find(myquery)                                     #alle docs in collection
    set=[]
    for x in mydoc:
        set.append(x)                                               #steek alle docs in een lijst
    return set
def getmongoMeasurement():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["Measurement"]


    myquery = {}                                                    #Lege query --> zoek alles

    mydoc = mycol.find(myquery)                                     #alle docs in collection
    set=[]
    for x in mydoc:
        set.append(x)                                               #steek alle docs in een lijst
    return set
def writemongo(measurementset):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")    #Connect met database
    mydb = myclient["IOT"]
    mycol = mydb["Measurement"]
    mycol.replace_one({},measurementset[0]) # {} --> eerste doc in collection, measurementset is een list van docs eigenlijk dus neem de 1ste doc uit de lijst
    return 0


def loadtestset(filename):
    f=open(filename,'r')
    lines = f.read().split(', ')
    return lines
def loadtrainingset(filename):
    f = open(filename, 'r')
    lines = f.read().splitlines()
    for i in range(len(lines)):
        lines[i]=lines[i].split('; ')
        for j in range(len(lines[i])):
            lines[i][j]=lines[i][j].split(', ')
    return lines

def euclideanDistance(instance1, instance2, length):                #Berekenen van euclidische afstand
    distance = 0
    for x in range(length):
        distance += pow((int(instance1[x]) - int(instance2[x])), 2)
    return int(math.sqrt(distance))

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)
    for x in range(len(trainingSet)):
        for y in range(len(trainingSet[x])):
            dist = euclideanDistance(testInstance, trainingSet[x][y], length)
            distances.append((trainingSet[x][y], dist,x))                           #euclidische afstanden in een nieuwe lijst steken
    distances.sort(key=operator.itemgetter(1))                                      #Sorteer de lijst op kleinste afstand
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x])                                              #steek de K kleinste afstanden in een nieuwe lijst
    return neighbors

def getNeighborsDB(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance[0]["RSSI"])
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance[0]["RSSI"], trainingSet[x]["RSSI"], length)   #euclidische afstanden in een nieuwe lijst steken
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
    return num                                                      #locatie die het dichtst bij de fysieke positie ligt

def main():
     trainingSet=getmongodata()
     testset=getmongoMeasurement()
     k = 5                                                          #neem een k --> nodig voor betere estimation, k aanpassen (trial en error)
     neighbors = getNeighborsDB(trainingSet, testset,k)
     location = estimation(neighbors,k)
     testset[0].update(location = location)
     writemongo(testset)
     print("Mobile node location: "+ str(location))
main()