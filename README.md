# _*Smarthalter Deluxe*_

Als frequent bezoeker van fitnesscentra, komt men vaak eenzelfde lastige situatie tegen. Je wilt graag oefeningen doen met een halter, maar deze blijkt niet op zijn plaats te liggen. De Smarthalter Deluxe is een "smart" fitnessaparaat dat deze kwaal tegengaat. Door middel van draadloze communicatie (adhv. Dash7 en LoRa) wordt de locatie van de halter steeds bijgehouden. Meer nog, met de Smarthalter Deluxe kan ook het aantal halter-oefeningen bijgehouden worden. 

Ook voor de fitness-eigenaar is de Smarthalter Deluxe een uitstekend staaltje techniek, zo houdt de halter de temperatuur en de luchtvochtigheid van de fitnessruimte overzichtelijk bij. De Smarthalter Deluxe komt nu ook met antidiefstal-functie. Zodra de halter zich buiten de directe omgeving van de fitness bevindt, wordt een bericht uitgezonden waarin wordt weergegeven dat de halter gestolen of verkeerdelijk meegepakt is.

## Stappenplan voor de gebruiker

1. Pick up dumbbel 
   - Device wakes up (putty) + localisation message
   - shows location thingsboard
   - gevoelige modus
2. BLE send weight 
   - Shows weight thingsboard
3. Press button 
   - Overgang naar repmodus (niet meer gevoelig)
   - show repmessage (putty)
   - thingsboard shows location 
   - show humidity and temperature 
4. show accelerometer rep interrupt → show putty reps
5. press button (stop repping)
   - show reps thingsboard
   - accelerometer terug naar gevoelige modus
6. inactivity timer 
   - show it goes to sleep after inactivity interval
7. tonen dat na 3 dash7-fails hij switcht naar LoraWAN → Stolen thingsboard


## Embedded

## Server
