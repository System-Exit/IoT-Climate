import requests
import json


# Class for sending pushbullet notifications
class PushbulletAPI():
    # Create pushbullet API access
    def __init__(self, token):
        # Set token for API access
        self.__token = token

    # Send pushbullet message
    def sendNotification(self, title, message):
        # Address for API call to be posted
        address = "https://api.pushbullet.com/v2/pushes"
        # Data to send to API
        data = json.dumps({"type": "note", "title": title, "body": message})
        # Header data for API
        headers = {'Authorization': 'Bearer %s' % self.__token,
                   'Content-Type': 'application/json'}
        # Post API request
        requests.post(address, data=data, headers=headers)
