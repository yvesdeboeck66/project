# _*Smart Dumbbell Deluxe*_

### _Dutch_
Als frequent bezoeker van fitnesscentra, komt men vaak eenzelfde lastige situatie tegen. Je wilt graag oefeningen doen met een halter, maar deze blijkt niet op zijn plaats te liggen. De Smarthalter Deluxe is een "smart" fitnessaparaat dat deze kwaal tegengaat. Door middel van draadloze communicatie (adhv. Dash7 en LoRa) wordt de locatie van de halter steeds bijgehouden. Meer nog, met de Smart Dumbbell kan ook het aantal halter-oefeningen bijgehouden worden.

Ook voor de fitness-eigenaar is de Smart Dumbbell een uitstekend staaltje techniek, zo houdt de halter de temperatuur en de luchtvochtigheid van de fitnessruimte overzichtelijk bij. De Smarthalter Deluxe komt nu ook met antidiefstal-functie. Zodra de halter zich buiten de directe omgeving van de fitness bevindt, wordt een bericht uitgezonden waarin wordt weergegeven dat de halter gestolen of verkeerdelijk meegepakt is.

### _English_
As a frequent visitor to fitness centers, you often come across the same difficult situation. You would like to do exercises with a dumbbell, but it has not been placed back into the rack by the previous user. The Smart Dumbbell Deluxe is a "smart" fitness device that counteracts this problem. The location of the dumbbell is always kept up-to-date through wireless communication (using Dash7 and LoRa). Moreover, with the Smarthalter Deluxe you can also keep track of the of performed dumbbell exercises.

The Smart Dumbbell is also an excellent piece of technology for the fitness owner, since it keeps track of the temperature and humidity of the fitness room. The Smart Dumbbell now also comes with an anti-theft feature. As soon as the dumbbell is outside the immediate vicinity of the fitness, a message is sent out, stating that the dumbbell has been stolen or improperly packed.

## User Guide

1. Pick the Smart Dumbbell up from the rack 
   - The device wakes up and sends a localisation message
   - The location is shown on the thingsboard
   - The device is now in Idle-Mode
2. Connect to the Smart Dumbbell over Bluetooth
3. Send your weight (kg) to the device
   - Your weight is saved to the device
3. Press the button to start your Smart Dumbbell exercises
   - The device enters Rep-Mode
   - A new message including your weight and location is sent
   - Your location is pinpointed on the thingsboard
   - The thingsboard shows your weight, as well as the temperature and humidity
4. Press the button again once to stop the exercises
   - A message including your Rep-count is sent
   - The device enters Idle-Mode
5. Put the Smart Dumbbell back in the rack
6. After not moving for a small amount of time, the device will send its final location and go into Sleep-Mode

_Extra_: If the device is unable to connect to the Dash7-Network in the fitness, the device will send a "stolen" message which is displayed on the thingsboard.

## Embedded

Smart Dumbbell is implemented using the Octa-Board (By IMec) for Nucleo-144, based on STM32L496-ZG. The device utilises Stop-mode in order to save battery life whenever it is not being used. To register the moment in which the Smart Dumbbell is picked up from the rack, an LSM303AGR accelerometer is used. In order to recognize the dumbbell-exercises, the accelerometer is configured for operation in double-click mode. 

Wireless messages within the fitness area are sent through Dash7. If there is no connection to this network, a LoRa-WAN message (which has a longer range) is sent. If this message is received by a gateway, the device will be marked as "Stolen" on the Thingsboard.
Temperature and humidity are measured using a HTS221-sensor. Bluetooth connection (through apps like nRF Toolbox) is made possible thanks to the integrated Bluetooth-chip on the octa-board.

### Power Consumption


## Server

Before going any further, we assume the necessary infrastructure such as Dash7 gateways and LoRaWAN gateways have been setup correctly in your gym.

Concerning server side implementation it is rather easy to setup. The Dash7Sensor.py file contains the code that initializes the connections, listens to the messages, estimates the location and sends the information to thingsboard. However, before running this code on your server, you must build your database for determining the reference locations where the user can be located. Therefore, download mongodb on your server and setup the collections that you will be using. For building your database, use the DatabaseFill.py file that will allow you to map Received Signal Strength values to a location in your gym.
Don't forget to adjust the collection name in the DatabaseFill.py file.

If you have build this database, you can use the Dash7Sensor.py code. Some further explanation considering this code follows beneath.
Note: This file is compiled in python 2.7

1. Subscribe to mqtt broker of the things network to listen to LoRaWAN messages.
2. Load the data from your database.
3. Subscribe to the Dash7 devices you have.
4. Wait until a message arrives.
   On arrival of a Dash7 message:
      Save the payload, check message counter and timer (if not first message).
   Start localisation if all messages have been received or when the time exceeded its limit 
   or when the message counter indicates a new message.
   
   On arrival of a LoRaWAN message:
      This indicates that the device couldn't receive any Dash7 acknowledges and thus swapped to LoRaWAN mode
      to notify the device has been stolen. This notification is send to thingsboard.

5. Localisation:
      The RSSI values are used to determine the K Nearest Neighbours in the database using the euclidean distance.
      Through Classification, the location is estimated.
6. Send the location with the payload to thingsboard.
7. Repeat by listening to new messages.

