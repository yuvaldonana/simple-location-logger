import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import json
import sqlite3
from datetime import datetime

if __name__ == "__main__":
    patterns = ["*.json"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)



def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
    if event.src_path == '.\\db.json':
        conn = sqlite3.connect('.\\locations.db')

        cursor = conn.cursor()


        with open('.\\db.json') as f:
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
        



my_event_handler.on_modified = on_modified


path = '.'
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()


try:
    while True:
            time.sleep(1)
except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

