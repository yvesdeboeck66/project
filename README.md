# _*Smarthalter Deluxe*_

Als frequent bezoeker van fitnesscentra, komt men vaak eenzelfde lastige situatie tegen. Je wilt graag oefeningen doen met een halter, maar deze blijkt niet op zijn plaats te liggen. De Smarthalter Deluxe is een "smart" fitnessaparaat dat deze kwaal tegengaat. Door middel van draadloze communicatie (adhv. Dash7 en LoRa) wordt de locatie van de halter steeds bijgehouden. Meer nog, met de Smarthalter Deluxe kan ook het aantal halter-oefeningen bijgehouden worden.

Ook voor de fitness-eigenaar is de Smarthalter Deluxe een uitstekend staaltje techniek, zo houdt de halter de temperatuur en de luchtvochtigheid van de fitnessruimte overzichtelijk bij. De Smarthalter Deluxe komt nu ook met antidiefstal-functie. Zodra de halter zich buiten de directe omgeving van de fitness bevindt, wordt een bericht uitgezonden waarin wordt weergegeven dat de halter gestolen of verkeerdelijk meegepakt is.

## Stappenplan voor de gebruiker

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

_Extra_ If the device is unable to connect to the Dash7-Network in the fitness, the device will send a "stolen" message which is displayed on the thingsboard.

## Embedded

## Server
