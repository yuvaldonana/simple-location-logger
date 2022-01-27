import json
import sqlite3
from datetime import datetime
conn = sqlite3.connect('path\to\locations.db')

cursor = conn.cursor()


with open('path\to\entries.json') as f:
    data = json.load(f)


# for testing purposes delete table if exists
cursor.executescript('''

DROP TABLE IF EXISTS locations;

CREATE TABLE locations (id, lat, lon, time)
''')
# insert into locations table
for entrey in data['entries']:
    cursor.execute("insert into locations values (?, ?, ?, ?)",
                    [entrey['id'], entrey['lat'], entrey["lon"], datetime.utcfromtimestamp(entrey["tst"]).strftime('%Y-%m-%d %H:%M:%S')])
    conn.commit()


