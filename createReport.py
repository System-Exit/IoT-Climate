#!/usr/bin/env python3
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
        date = row[0]
        maxtemp = row[1]
        mintemp = row[2]
        maxhumid = row[3]
        minhumid = row[4]
        
        #date, maxtemp, mintemp, maxhumid, minhumid = row.split(',',5)
        # temp print for debugging
        print("Date: ")
        print(date)
        print("\nMax Temperature: ")
        print(maxtemp)
        print("\nMin Temperature: ")
        print(mintemp)
        print("\nMax Humidity: ")
        print(maxhumid)
        print("\nMin Humidity: ")
        print(minhumid)
 
 
def main():
    database = "climate_data.db"
 
    # Create database connection, pass conn to querydb.
    conn = create_connection(database)
    with conn:
        querydb(conn)
 
if __name__ == '__main__':
    main()