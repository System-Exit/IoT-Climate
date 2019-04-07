#!/usr/bin/env python3
import json
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
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
        # Check queryHMD for commenting, this is same but uses matplotlib
        # and graphs temperature.
        cur = self.__database.cursor()
        cur.execute("select strftime('%d-%m-%Y', time),\
                    AVG(temperature) \
                    FROM ClimateData \
                    GROUP BY strftime('%d-%m-%Y', time);")

        rows = cur.fetchall()
        dft = pd.DataFrame([[ij for ij in i] for i in rows])
        ax = plt.gca()

        dft.rename(columns={0: 'Date', 1: 'Temperature (c)'}, inplace=True)
        dft.plot(kind='line', x='Date', y='Temperature (c)', ax=ax)

        plt.savefig('fig1.png')
        plt.clf()
        plt.close()

    def queryHMD(self):
        # Initialize Database
        cur = self.__database.cursor()
        # Query Database to get avg humidity for each day
        cur.execute("select strftime('%d-%m-%Y', time),\
                    AVG(humidity) \
                    FROM ClimateData \
                    GROUP BY strftime('%d-%m-%Y', time);")
        # Place all results into a tuple that pandas can handle.
        rows = cur.fetchall()
        sns.set(style="darkgrid")
        # Convert from tuples to pandas dataframe.
        dfh = pd.DataFrame([[ij for ij in i] for i in rows])
        # Update dataframe with correct data
        dfh.rename(columns={0: 'Date', 1: 'Humidity'}, inplace=True)

        # Create the plot
        sns.lineplot(x="Date", y="Humidity", data=dfh)

        # Save the file
        plt.savefig("fig2.png")
        plt.clf()
        plt.close()

# Main method
if __name__ == '__main__':
    # Initialize database name and report name
    databaseName = "climate_data.db"

    # Initialize report creator for specified climate database
    gc = GraphCreator(databaseName)

    # Create report for climate database
    gc.queryTMP()
    gc.queryHMD()
