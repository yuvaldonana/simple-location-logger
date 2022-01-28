import json
import sqlite3
import os
import pprint
from datetime import datetime
conn = sqlite3.connect('C:\\Users\yuval\Desktop\Projects\gps\jsonserver\locations.db')

cursor = conn.cursor()


with open('C:\\Users\yuval\Desktop\Projects\gps\jsonserver\db.json') as f:
    data = json.load(f)

cursor.executescript('''

DROP TABLE IF EXISTS transition;

DROP TABLE IF EXISTS locations;

DROP TABLE IF EXISTS waypoints;

CREATE TABLE transition (ID, Location, Event, Latitude, Longitude, Trigger, Accuracy, Device, ModTime, Time);

CREATE TABLE locations (ID, Latitude, Longitude, Trigger, Accuracy, Device, Altitude, Battery, Time);

CREATE TABLE waypoints (ID, Location, Radius, Latitude, Longitude, Time);

''')

for entrey in data['employees']:
    if len(entrey) > 3:
        if entrey['_type'] == 'transition':
            cursor.execute("insert into transition values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [entrey['id'], entrey['desc'], entrey["event"], entrey["lat"], entrey["lon"], entrey["t"], entrey["acc"], entrey["tid"], datetime.utcfromtimestamp(entrey["wtst"]).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(entrey["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
            conn.commit()
        if entrey['_type'] == 'location':
            cursor.execute("insert into locations values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [entrey['id'], entrey['lat'], entrey["lon"], entrey["t"], entrey["acc"], entrey["tid"], entrey["alt"], entrey["batt"], datetime.utcfromtimestamp(entrey["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
            conn.commit()
            
        if entrey['_type'] == 'waypoint':
            cursor.execute("insert into waypoints values (?, ?, ?, ?, ?, ?)",
            [entrey['id'], entrey['desc'], entrey["rad"], entrey["lat"], entrey["lon"], datetime.utcfromtimestamp(entrey["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
            conn.commit()
        
    




