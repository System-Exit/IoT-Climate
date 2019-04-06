#!/usr/bin/env python3
import json
import os
import sqlite3
from sqlite3 import Error
import time
import csv


class ReportCreator:
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

    def __connectToDatabase(self, dbfile):
        # Connect to database, error if doesn't exist
        try:
            self.__database = sqlite3.connect(databaseName)
        except Error as e:
            print(e)

    # Builds status record depending on parameters
    def __buildStatusRec(self, rowMaxTemp, rowMinTemp,
                         rowMaxHumid, rowMinHumid):
        # Initialize record string
        string = ""
        # Check max temperature, adding info if out of bounds
        if rowMaxTemp > self.__maxTemp:
            string += " %s *C above maximum temperature and"\
                        % round(rowMaxTemp - self.__maxTemp, 2)
        # Check min temperature, adding info if out of bounds
        if rowMinTemp < self.__minTemp:
            string += " %s *C below minimum temperature and"\
                        % round(self.__minTemp - rowMinTemp, 2)
        # Check max humidity, adding info if out of bounds
        if rowMaxHumid > self.__maxHumid:
            string += " %s%% above maximum humidity and"\
                        % round(rowMaxHumid - self.__maxHumid, 2)
        # Check min humidity, adding info if out of bounds
        if rowMinHumid < self.__minHumid:
            string += " %s%% below minimum humidity and"\
                        % round(self.__minHumid - rowMinHumid, 2)
        # If nothing has been added to string, change it to "OK"
        # Otherwise, add "BAD: " to the start of it and remove last "and"
        if not string:
            string = "OK"
        elif string:
            string = "BAD:" + string.rstrip(" and")
        # return built string
        return string

    def makeReport(self, csvname):
        # Setup database
        cur = self.__database.cursor()
        cur.execute("SELECT strftime('%d-%m-%Y', time),\
                    MAX(temperature), \
                    MIN(temperature), \
                    MAX(humidity), \
                    MIN(humidity) \
                    FROM ClimateData \
                    GROUP BY strftime('%d-%m-%Y', time);")
        # setup tuple with all results
        rows = cur.fetchall()

        # Setup csv writing
        with open(csvname, 'w') as report:
            rwriter = csv.writer(report,
                                 delimiter=',',
                                 quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
            rwriter.writerow(['Date', 'Status'])

            # Parse tuple into variables and write row into file
            for row in rows:
                date = row[0]
                maxTempRes = row[1]
                minTempRes = row[2]
                maxHumidRes = row[3]
                minHumidRes = row[4]

                # Build row string and write the row to file
                status = self.__buildStatusRec(maxTempRes,
                                               minTempRes,
                                               maxHumidRes,
                                               minHumidRes)
                rwriter.writerow([date, status])

# Main method
if __name__ == '__main__':
    # Initialize database name and report name
    databaseName = "climate_data.db"
    csvName = "report.csv"

    # Initialize report creator for specified climate database
    reportMaker = ReportCreator(databaseName)

    # Create report for climate database
    reportMaker.makeReport(csvName)
