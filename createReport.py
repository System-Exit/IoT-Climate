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

    def __connectToDatabase(dbfile):
        # Connect to database, error if doesn't exist
        try:
            self.__database = sqlite3.connect(databaseName)
        except Error as e:
            print(e)

    # Builds status record depending on parameters
    def __buildStatusRec(rowMaxTemp, rowMinTemp, rowMaxHumid, rowMinHumid):
        # Initialize record string
        string = ""
        # Check max temperature
        if rowMaxTemp > self.__maxTemp:
            string += ""
        # Check min temperature
        if rowMinTemp > self.__minTemp:
            string += ""
        # Check max humidity
        if rowMaxHumid > self.__maxHumid:
            string += ""
        # Check min humidity
        if rowMinHumid > self.__minHumid:
            string += ""
        # If nothing has been added to string, change it to "OK"
        # Otherwise, add "BAD: " to the start of it
        if not string:
            string = "OK"
        elif string:
            string = "BAD:" + string
        #

    # Validation for Max Temp
    def validatetmp_max(self, lim_tmp_max, maxtemp):
        if maxtemp > lim_tmp_max:
            # Calculate Difference (converting to string (Rounded))
            tmpdiff_max = maxtemp-lim_tmp_max
            return("BAD: "+str(round(tmpdiff_max, 2)) +
                "°c above maximum temperature")
        else:
            return("Max Temp: OK ")

    # Validation for Min Temp
    def validatetmp_min(self, lim_tmp_min, mintemp):
        if mintemp < lim_tmp_min:
            # Calculate Difference (convert to string (Rounded))
            tmpdiff_min = lim_tmp_min-mintemp
            return("BAD: "+str(round(tmpdiff_min, 2)) +
                "°c below minimum temperature")
        else:
            return("Min Temp: OK ")

    # Validation for Max Humidity
    def validatehumid_max(self, lim_hmd_max, maxhumid):
        if maxhumid > lim_hmd_max:
            # Calculate Difference (converting to string from int (raw percentage))
            hmddiff_max = max-lim_hmd_max
            return("BAD: "+str(int(hmddiff_max, 2))+"% above maximum Humidity")
        else:
            return("Max Humidity: OK ")

    # Validation for Min Humidity
    def validatehumid_min(self, lim_hmd_min, minhumid):
        if minhumid < lim_hmd_min:
            # Calculate Difference (converting to string from int (raw percentage))
            hmddiff_min = lim_hmd_min-minhumid
            return("BAD: "+str(round(hmddiff_min, 2)) +
                "°c below minimum Humidity")
        else:
            return("Min Temp: OK ")

    def querydb_and_write(self, lim_tmp_min, lim_tmp_max, lim_hmd_min, 
                          lim_hmd_max, conn, csvname):
        # Setup database
        cur = conn.cursor()
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
            rwriter.writerow(['Date',
                            'Temperature Status: Maximum',
                            'Temperature Status: Minumum',
                            'Humidity Status: Maximum',
                            'Humidity Status: Minumum'])

            # parse tuple into variables (all writing is in this loop too.)
            for row in rows:
                date = row[0]
                maxtemp = row[1]
                mintemp = row[2]
                maxhumid = row[3]
                minhumid = row[4]

                # Call validations, giving them max,mins and the limits
                # TODO: This isnt pretty, it will write a whole new column for each
                # validation (instead of just an OK), possible but time consuming
                # to redo. (possibly move the return parts to here.)
                rwriter.writerow([date,
                                validatetmp_max(lim_tmp_max, maxtemp),
                                validatetmp_min(lim_tmp_min, mintemp),
                                validatehumid_max(lim_hmd_max, maxhumid),
                                validatehumid_min(lim_hmd_min, minhumid)])


def main():
    database = "climate_data.db"
    csvname = "report.csv"

    with open("config.json", "r") as jsonFile:
        config = json.load(jsonFile)
        lim_tmp_min = float(config["min_temperature"])
        lim_tmp_max = float(config["max_temperature"])
        lim_hmd_min = float(config["min_humidity"])
        lim_hmd_max = float(config["max_humidity"])

    # Create database connection, pass conn to querydb.
    conn = create_connection(database)
    with conn:
        querydb_and_write(lim_tmp_min,
                          lim_tmp_max,
                          lim_hmd_min,
                          lim_hmd_max,
                          conn,
                          csvname)

if __name__ == '__main__':
    main()
