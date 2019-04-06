#!/usr/bin/env python3
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sqlite3
from sqlite3 import Error

# https://plot.ly/python/
# https://matplotlib.org/examples/api/barchart_demo.html


class GraphCreator:
    def __init__(self, databaseName):
        # Load JSON config variables (potential limits in graph)
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
    def __buildGraph(self):
        # TODO: Code for actually building the graph to a png
        return

    def queryTMP(self):
        # Setup database
        cur = self.__database.cursor()
        # Output average temperature and humidity of each day
        cur.execute("select strftime('%d-%m-%Y', time),\
                    AVG(temperature) \
                    FROM ClimateData \
                    GROUP BY strftime('%d-%m-%Y', time);")
        # convert turples to DataFrame (easier plotting to plotly)
        # put all data into rows tuple
        print("Fetching Rows")
        rows = cur.fetchall()
        print("Loading into DataFrame")
        # for each row, go through everything and add to equivilent dataframe.
        df = pd.DataFrame([[ij for ij in i] for i in rows])
        # Draw plot
        ax = plt.gca()
        df.rename(columns={0: 'Date', 1: 'Temperature (c)'}, inplace=True)
        print(df)
        df.plot(kind='line', x='Date', y='Temperature (c)', ax=ax)
        plt.savefig('fig1.png')


# Main method
if __name__ == '__main__':
    # Initialize database name and report name
    databaseName = "climate_data.db"

    # Initialize report creator for specified climate database
    gc = GraphCreator(databaseName)

    # Create report for climate database
    gc.queryTMP()
