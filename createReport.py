#!/usr/bin/env python3
 import requests
import json
import os
import sqlite3
from sqlite3 import Error
import time

 
 
def create_connection(dbfile):
    ## Connect to database, error if doesn't exist
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except Error as e:
        print(e)
 
    return None


def querydb(conn):
    # Setup database
    cur = conn.cursor()
    cur.execute("SELECT strftime('%d-%m-%Y', time), MAX(temperature), MIN(temperature), MAX(humidity), MIN(humidity) FROM ClimateData GROUP BY strftime('%d-%m-%Y', time);")
 
    rows = cur.fetchall()
 
    for row in rows:
        # Split results into individual variables, comma delimiter (up to 5)
        date, maxtemp, mintemp, maxhumidity, minhumidity = row.split(',',5)
        # temp print for debugging
        print("Date: ")
        print(date)
        print("\nMax Temperature: ")
        print(maxtemp)
        print("\nMin Temperature: ")
        print(mintemp)
        print("\nMax Humidity: ")
        print(maxhumidity)
        print("\nMin Humidity: ")
        print(minhumidity)
 
 
def main():
    database = "climate_data.db"
 
    # Create database connection, pass conn to querydb.
    conn = create_connection(database)
    with conn:
        querydb(conn)
 
if __name__ == '__main__':
    main()