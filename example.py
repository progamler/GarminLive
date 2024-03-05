from imaplib import IMAP4_SSL
from poplib import POP3_SSL
import garminlive
import argparse
import os
import logging
from pprint import pprint
import paho.mqtt.client as mqtt
import json
import time
### Get Latest Mail from Garmin via IMAP/POP3 and find the Link


# --host (Mail Server) Alternative get env garmin_mail_server
# --user (Mail User) Alternative get env garmin_mail_user
# --password (Mail User Password) Alternative get env garmin_mail_password
# --protocol (IMAP or POP3) Alternative get env garmin_mail_protocol
# --debug (Debug Mode 1 to 10) Alternative get env garmin_mail_debug

# Create Logger
logger = logging.getLogger(__name__)

# Parse Arguments
parser = argparse.ArgumentParser(description='Get Latest Mail from Garmin via IMAP/POP3 and find the Link')
parser.add_argument('--host', type=str, help='Mail Server')
parser.add_argument('--user', type=str, help='Mail User')
parser.add_argument('--password', type=str, help='Mail User Password')
parser.add_argument('--protocol', type=str, help='IMAP or POP3')
parser.add_argument('--folder', type=str, help='Mail Folder', default='inbox')
parser.add_argument('--debug', type=int, help='Debug Mode 1 to 4')
args = parser.parse_args()

# Get Environment Variables
garmin_mail_server = os.getenv('garmin_mail_server')
garmin_mail_user = os.getenv('garmin_mail_user')
garmin_mail_password = os.getenv('garmin_mail_password')
garmin_mail_protocol = os.getenv('garmin_mail_protocol')
garmin_mail_debug = os.getenv('garmin_mail_debug')
garmin_mail_folder = os.getenv('garmin_mail_folder')    

# Set Arguments
host = args.host if args.host else garmin_mail_server
user = args.user if args.user else garmin_mail_user
password = args.password if args.password else garmin_mail_password
protocol = args.protocol if args.protocol else garmin_mail_protocol
debug = args.debug if args.debug else garmin_mail_debug
folder = args.folder if args.folder else garmin_mail_folder


# Set Debug Level
match debug:
    case 1:
        logger.setLevel(logging.ERROR)
    case 2:
        logger.setLevel(logging.WARNING)
    case 3:
        logger.setLevel(logging.INFO)
    case 4:
        logger.setLevel(logging.DEBUG)
    case default:
        logger.setLevel(logging.NOTSET)

session =""
# Check if the protocol is IMAP
if protocol == "IMAP":
    # Establish a secure connection with the mail server
    with IMAP4_SSL(host) as mail:
        # Login to the mail server using the provided user and password
        mail.login(user, password)
        # Select the 'inbox' mailbox
        mail.select(folder)
        # Search for all messages in the 'inbox'
        status, messages = mail.search(None, '(FROM "noreply@garmin.com")')
        # Split the messages into a list
        messages = messages[0].split()
        # Get the ID of the latest message
        latest = int(messages[-1])
        # Fetch the latest message
        status, message = mail.fetch(str(latest), '(UID BODY[TEXT])')
        
        body=message[0][1].decode()
        # Print the fetched message
        #print(body)
        # find linke in message starting with https://livetrack.garmin.com/session/
        link = "".join(body.split('https://livetrack.garmin.com/session/')[1].split('"')[0].split("=\r\n"))
        print('Using Link: https://livetrack.garmin.com/session/%s' % link)
        session = link.split("/")[0]
        # Close the connection
        mail.close()
# Check if the protocol is POP3
elif protocol == "POP3":
    # raise NotImplementedError("POP3 is not implemented yet")
    raise NotImplementedError("POP3 is not implemented yet")

# check if link is found other withe rais an error
if not link:
    logger.error("No Link found in the Mail")
    logger.info("Message Body %s" % body)
    raise ValueError("No Link found in the Mail")


#
print("Getting Trackpoints from Garmin LiveTrack API")
g = garminlive.GarminLiveTrack('https://livetrack.garmin.com/session/%s' % link)
logger.info(f"Trackpoints: {g.getTrackpoints()}")
allT = g.getTrackpoints()
#sleep 60 seconds
pprint(allT)
# connect to mqtt
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)
print("Publishing Trackpoints to MQTT")
print(f"garmin/{session}/trackpoints")
for i in range(len(allT['trackPoints'])):
    client.publish(f"garmin/{session}/trackpoints", json.dumps(allT['trackPoints'][i]))
    
# run g.update() every x seconds and publish new trackpoints to mqtt
while True:
    print(f"garmin/{session}/trackpoints")
    g.update()
    #check if new trackpoints are available
    newT = g.getTrackpoints()
    for i in range(len(newT['trackPoints'])):
        client.publish(f"garmin/{session}/trackpoints", json.dumps(newT['trackPoints'][i]))
    if len(newT['trackPoints']) == 0:
        time.sleep(5)

