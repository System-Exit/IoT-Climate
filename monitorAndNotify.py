#!/usr/bin/env python3
import requests
import json
import os
import sqlite3
import sense_hat
import time
import urllib


# Monitor and notification class
class MonitorNotifier:
    def __init__(self, databaseName):
        # Get sense hat access
        self.__sense = sense_hat.SenseHat()
        # Load JSON config variables
        with open("config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            self.__minTemp = float(config["min_temperature"])
            self.__maxTemp = float(config["max_temperature"])
            self.__minHumid = float(config["min_humidity"])
            self.__maxHumid = float(config["max_humidity"])
        # Load Pushbullet access token from JSON file
        with open("token.json", "r") as jsonFile:
            token = json.load(jsonFile)
            self.__accessToken = token["PB_api_token"]
        # Connect to database for logging climate data
        self.__connectToDatabase(databaseName)

    # Connects to climate database if it exists, otherwise creating one
    def __connectToDatabase(self, databaseName):
        # Connect to database file
        self.__database = sqlite3.connect(databaseName)
        with self.__database:
            # Get cursor for database
            cursor = self.__database.cursor()
            # Create climate data table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS ClimateData \
                (time DATETIME, temperature NUMERIC, humidity NUMERIC)")
            # Create notification table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS Notifications \
                (timesent DATETIME)")
            # Commit creating of table
            self.__database.commit()

    # Record the current temp data into database
    def recordClimate(self):
        # Update current climate information
        # TODO make readings more accurate, perhaps put in own methods
        temperature = self.__sense.get_temperature()
        humidity = self.__sense.get_humidity()
        # Record climate information in database and send notification
        with self.__database:
            cursor = self.__database.cursor()
            cursor.execute("INSERT INTO ClimateData (time, temperature, humidity) \
                            VALUES (DATETIME('now', 'localtime'), ?, ?)",
                           (temperature, humidity))
        self.__database.commit()
        # print("[+] temperature, humidity", (temperature, humidity))
        # Check if notification sould be sent
        self.__checkAndNotify(temperature, humidity)
        # End of function
        return

    # Sends a pushbullet notification if temperature is out of range
    # and a notification has not already been sent today
    def __checkAndNotify(self, temperature, humidity):
        # If outside of config range, check database if notification
        # has already been sent today
        if temperature < self.__minTemp or temperature > self.__maxTemp or\
           humidity < self.__minHumid or humidity > self.__maxHumid:
            # Check if notification has already been sent today
            with self.__database:
                cursor = self.__database.cursor()
                cursor.execute(
                    "SELECT COUNT(*) \
                     FROM Notifications \
                     WHERE strftime('%d-%m-%Y', timesent) \
                     = strftime('%d-%m-%Y', DATETIME('now', 'localtime'))")
                recordCount = cursor.fetchone()[0]
            # If a notification has already been sent, return immediately
            if recordCount >= 1:
                return
            # Construct pushbullet message strings
            title = "Raspberry Pi climate alert"
            message = "Warning,"
            if temperature < self.__minTemp:
                message += " temperature is too low,"
            if temperature > self.__maxTemp:
                message += " temperature is too high,"
            if humidity < self.__minHumid:
                message += " humidity is too low,"
            if humidity > self.__maxHumid:
                message += " humidity is too high,"
            message = message.rstrip(',') + "."
            # Wait until program is able to connect to internet
            while not self.__checkConnection():
                time.sleep(1)
            # Send pushbullet message
            dataToSend = {"type": "note", "title": title, "body": message}
            data = json.dumps(dataToSend)
            requests.post('https://api.pushbullet.com/v2/pushes', data=data,
                          headers={
                              'Authorization': 'Bearer %s' %
                              self.__accessToken,
                              'Content-Type': 'application/json'})
            # Record sending of notification
            with self.__database:
                cursor = self.__database.cursor()
                cursor.execute("INSERT INTO Notifications (timesent) \
                                VALUES (DATETIME('now', 'localtime'))")

    # Returns true if able to connect to pushbullet api, otherwise false
    def __checkConnection(self):
        # Attempt connection
        try:
            host = urllib.request.urlopen("https://www.google.com")
            # Since connection was successful, return True
            return True
        except:
            # Since connection failed, return False
            return False


# Main method
if __name__ == "__main__":
    # Database name and access token variables
    databaseName = "climate_data.db"
    # Initialize monitor class
    monitor = MonitorNotifier(databaseName)
    # Check climate conditions every minute
    while True:
        monitor.recordClimate()
        time.sleep(60)
