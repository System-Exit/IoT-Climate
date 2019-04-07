#!/usr/bin/env python3
import sense_hat
import bluetooth
import json
import subprocess
import requests
import time
from pushbullet_api import PushbulletAPI
from climate_util import ClimateUtil


# Bluetooth notification class
class BluetoothNotifier:
    # Initialization
    def __init__(self):
        # Get sense hat access
        self.__sense = sense_hat.SenseHat()
        # Load JSON config variables
        with open("config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            self.__minTemp = float(config["min_temperature"])
            self.__maxTemp = float(config["max_temperature"])
            self.__minHumid = float(config["min_humidity"])
            self.__maxHumid = float(config["max_humidity"])
        # Load Pushbullet API access
        self.__pushbulletAPI = PushbulletAPI()

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
        temperature = ClimateUtil.getCalibratedTemp(self.__sense)
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
        # Wait until program is able to connect to internet
        while not ClimateUtil.checkConnection():
            time.sleep(1)
        # Send pushbullet message
        self.__pushbulletAPI.sendNotification(title, message)


# Main method for script
if __name__ == "__main__":
    # Initialize bluetooth nottifier
    blueNotifier = BluetoothNotifier()
    # Check if any paired devices can be detected nearby
    # If there are, send a notification via pushbullet
    if(blueNotifier.checkIfPairedDeviceNearby()):
        blueNotifier.sendNotificaton()
