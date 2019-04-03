#!/usr/bin/env python3
import sense_hat
import bluetooth
import json
import subprocess
import requests


# Bluetooth notification class
class BluetoothNotifier:
    # Initialization
    def __init__(self, accessToken):
        # Get sense hat access
        self.__sense = sense_hat.SenseHat()
        # Access token for pushbullet notification
        self.__accessToken = accessToken
        # Load JSON config variables
        with open("config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            self.__minTemp = float(config["min_temperature"])
            self.__maxTemp = float(config["max_temperature"])
            self.__minHumid = float(config["min_humidity"])
            self.__maxHumid = float(config["max_humidity"])

    # Checks if a paired device is nearby, returning true if so
    # Note: Avoids the use of bt-device to get paired devices
    #       Gets paired devices from bluetooth directory instead
    def checkIfPairedDeviceNearby(self):
        # Get controller addresses and put them into a list
        lsResult = str(subprocess.run(["sudo", "ls", "/var/lib/bluetooth/"],
                       stdout=subprocess.PIPE).stdout)
        controllers = lsResult.replace("b", "").replace("\\n", " ")\
            .replace("'", "").split()
        # Get all paired devices for each controller
        devices = []
        for ctrl in controllers:
            # Gets the devices from the controller directory
            lsResult = str(subprocess.run(
                ["sudo", "ls", "/var/lib/bluetooth/%s" % ctrl],
                stdout=subprocess.PIPE).stdout)
            # Adds all devices to the devices list
            devices.extend(lsResult.replace("b", "")
                           .replace("\\n", " ").replace("'", "").split())

        # Get all nearby devices
        nearby_devices = bluetooth.discover_devices()
        # Check all nearby devices to see if a paired device is present
        for neardev in nearby_devices:
            if neardev in devices:
                return True
        # Return false, since no paired device was detected
        return False

    # Sends notification
    def sendNotificaton(self):
        # Get temperature and humidity
        temperature = self.__sense.get_temperature()
        humidity = self.__sense.get_humidity()
        # Construct pushbullet message strings
        title = "Bluetooth climate alert"
        message = "Temperature is %s *C, Humidity is %s%%, "\
            % (round(temperature, 2), round(humidity, 2))
        if temperature < self.__minTemp or temperature > self.__maxTemp\
           or humidity < self.__minHumid or humidity > self.__maxHumid:
            message += "climate outside expected parameters."
        else:
            message += "climate within expected parameters."
        # Send pushbullet message
        dataToSend = {"type": "note", "title": title, "body": message}
        data = json.dumps(dataToSend)
        requests.post('https://api.pushbullet.com/v2/pushes', data=data,
                      headers={
                          'Authorization': 'Bearer %s' %
                          self.__accessToken,
                          'Content-Type': 'application/json'})

# Main method for script
if __name__ == "__main__":
    # Access token variable
    accessToken = ""
    # Initialize bluetooth nottifier
    blueNotifier = BluetoothNotifier(accessToken)
    # Check if any paired devices can be detected nearby
    # If there are, send a notification via pushbullet
    if(blueNotifier.checkIfPairedDeviceNearby()):
        blueNotifier.sendNotificaton()
