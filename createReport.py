#!/usr/bin/env python3
import requests
import json
import os
import sqlite3
import time

## What needs to happen:
## load sqlite into memory, loop over each instance, checking each one if it goes over 
## in bounds. so save date (and temp/weather) and skip all that match date.

# ReportCSV Class
class ReportCSV:
    def __init__(self, databaseName):
        # Load JSON config variables
        with open("config.json", "r") as jsonFile:
            config = json.load(jsonFile)
            self.__minTemp = float(config["min_temperature"])
            self.__maxTemp = float(config["max_temperature"])
            self.__minHumid = float(config["min_humidity"])
            self.__maxHumid = float(config["max_humidity"])
        # Connect to database for logging climate data
        self.__connectToDatabase(databaseName)

    # Connects to climate database if it exists, otherwise creating one
    def __connectToDatabase(self, databaseName):
        # Connect to database file
        self.__database = sqlite3.connect(databaseName)
        with self.__database:
            # Get cursor for database
            cursor = self.__database.cursor()
            # Create table if it doesn't exist
            cursor.execute("CREATE TABLE IF NOT EXISTS ClimateData \
                (time DATETIME, temperature NUMERIC, humidity NUMERIC)")
            # Commit creating of table
            self.__database.commit()

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
            with self.__database:
                cursor = self.__database.cursor()
                cursor.execute("SELECT COUNT(*) FROM ClimateData WHERE \
                    DATE(time) = DATE(DATETIME('now', 'localtime')) AND \
                    temperature < ? OR temperature > ? OR \
                    humidity < ? OR humidity > ?",
                               (self.__minTemp, self.__maxTemp,
                                self.__minHumid, self.__maxHumid))
                recordCount = cursor.fetchone()[0]
            # If there is only one record, a notification can't have been
            # sent yet, otherwise a notification must have been sent
            if recordCount != 1:
                return
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

# Main method
if __name__ == "__main__":
    # Database name and access token variables
    databaseName = "climate_data.db"
    # Initialize report class
    report = ReportCSV(databaseName)
