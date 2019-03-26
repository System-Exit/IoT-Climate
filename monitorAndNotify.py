#!/usr/bin/env python3
import requests
import json
import os
import sqlite3
import sense_hat

# Access token for sending pushbullet notifications
ACCESS_TOKEN = ""


# Monitor and notification class
class MonitorNotifier:
    def __init__(self):
        # Get sense hat access
        self.__sense = sense_hat.SenseHat()
        # Load JSON config variables
        with open("config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            self.__minTemp = config["min_temperature"]
            self.__maxTemp = config["max_temperature"]
            self.__minHumid = config["min_humidity"]
            self.__maxHumid = config["max_humidity"]
        # Initialize other variables to none for now
        self.__database = None
        self.__temperature = None
        self.__humidity = None

    # Connects to database if it exists, otherwise creating one
    def connectToDatabase(self, database):
        # Connect to database file
        self.__database = sqlite3.connect(database)
        with self.__database:
            # Get cursor for database
            cursor = self.__database.cursor()
            # Create table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS ClimateData \
                (time DATETIME, temperature NUMERIC, humidity NUMERIC)")
            # Commit creating of table
            self.__database.commit()

    # TODO
    # Record the current temp data into database
    def recordClimate(self):
        # Update current climate information
        self.__temperature = sense.get_temperature()
        self.__humidity = sense.get_humidity()
        # Record climate information in database and send notification
        with self.__database:
            cursor = self.__database.cursor()
            cursor.execute("INSERT INTO ClimateData (time, temperature, humidity) \
                            VALUES (?, ?, ?)",
                           ("DATETIME('now')",
                            self.__temperature,
                            self.__humidity))
        self.__database.commit()
        # If out of config range, send a notification
        if self.__temperature < self.__minTemp or\
           self.__temperature > self.__maxTemp or\
           self.__humidity < self.__minHumid or\
           self.__humidity > self.__maxHumid:
            self.sendNotification()

    # TODO
    # Sends pushbullet notification
    def sendNotification(self):
        # Check if notification has already been sent today by checking if
        # more than one record exists that is outside of config range
        with __database:
            cursor = self.__database.cursor()
            # Check if notification has already been sent today by checking if
            # more than one record exists that is outside of config range
            cursor.execute("SELECT COUNT(*) FROM ClimateData WHERE \
                DATEPART(DAY, time) = DATEPART(DAY, now) AND \
                DATEPART(MONTH, time) = DATEPART(MONTH, now) AND \
                DATEPART(YEAR, time) = DATEPART(YEAR, now) AND \
                temperature < ? OR temperature > ? OR \
                humidity < ? OR humidity > ?",
                           (self.__minTemp, self.__maxTemp,
                            self.__minHumid, self.__maxHumid))

# Main method
if __name__ == "__main__":
    pass
