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
        # Initialize database to be none for now
        self.__database = None

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

    # Record the current temp data into database
    def recordClimate(self):
        # Update current climate information
        temperature = sense.get_temperature()
        humidity = sense.get_humidity()
        # Record climate information in database and send notification
        with self.__database:
            cursor = self.__database.cursor()
            cursor.execute("INSERT INTO ClimateData (time, temperature, humidity) \
                            VALUES (?, ?, ?)",
                           ("DATETIME('now')",
                            temperature,
                            humidity))
        self.__database.commit()
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
            # Check if notification has already been sent today by
            # checking if more than one record exists that is outside of
            # config range
            with __database:
                cursor = self.__database.cursor()
                cursor.execute("SELECT COUNT(*) FROM ClimateData WHERE \
                    DATE(time) = DATE(DATETIME('now')) AND \
                    temperature < ? OR temperature > ? OR \
                    humidity < ? OR humidity > ?",
                               (self.__minTemp, self.__maxTemp,
                                self.__minHumid, self.__maxHumid))
                recordCount = cursor.fetchone()[0]
            # If there is only one record, a notification can't have been
            # sent yet, otherwise a notification must have been sent
            if recordCount != 1:
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
            # Send pushbullet message
            dataToSend = {"type": "note", "title": title, "body": message}
            data = json.dumps(dataToSend)
            requests.post('https://api.pushbullet.com/v2/pushes', data=data,
                          headers={'Authorization': 'Bearer %s' % ACCESS_TOKEN,
                                   'Content-Type': 'application/json'})

# Main method
if __name__ == "__main__":
    # Initialize monitor class
    monitor = MonitorNotifier()
    # Placeholder database name TODO
    database = "climate_data"
    # Check climate conditions every minute
    while True:
        monitor.connectToDatabase(database)
        monitor.recordClimate()
        time.sleep(60)
