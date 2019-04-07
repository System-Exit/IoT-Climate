import requests
import json


# Class for sending pushbullet notifications
class PushbulletAPI():
    # Create pushbullet API access
    def __init__(self):
        # Get API token form token.json and Set token for API access
        with open("token.json", "r") as jsonFile:
            token = json.load(jsonFile)
            self.__token = token["PB_api_token"]

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
