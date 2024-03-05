# GarminLive
Garmin Lvetracker Data to MQTT


run HiveQM     
docker run -p 8080:8080 -p 1883:1883 -p 8000:8000 hivemq/hivemq4

Run the Script:
python example.py --host <mailserver> --user <user> --password <password> --protocol IMAP 
this will search for the last mail from garmin and find the link to the session (only IMAP support ATM)

Open die Displayvalues.html to see the MQTT updates On a webpage