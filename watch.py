import time
import sys
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
    #if event.src_path == '.\\.json':'
        time.sleep(3)
        with open('.\\db.json') as f:
                data = json.load(f)
                reports = data['report']
        if len(reports) <= 0:
            sys.exit('error')
        else:
    
    
            conn = sqlite3.connect('.\\locations.db')

            cursor = conn.cursor()

            print('connected')


            with open('.\\db.json') as f:
                data = json.load(f)
                reports = data['report']

            for x in reports:
                
                if len(x) > 3:
                    if 'wtst' in x:
                        cursor.execute("insert into transition values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        [x['id'], x['desc'], x["event"], x["lat"], x["lon"], x["t"], x["acc"], x["tid"], datetime.utcfromtimestamp(x["wtst"]).strftime('%Y-%m-%d %H:%M:%S'), datetime.utcfromtimestamp(x["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
                        conn.commit()
                        time.sleep(5)
                        with open('.\\db.json', 'w') as f:
                            f.write('''{
"report": [
        
]
}''')
                            f.close()
                    if 'batt' in x:
                        cursor.execute("insert into locations values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        [x['id'], x['lat'], x["lon"], x["t"], x["acc"], x["tid"], x["alt"], x["batt"], datetime.utcfromtimestamp(x["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
                        conn.commit()
                        time.sleep(5)
                        with open('.\\db.json', 'w') as f:
                            f.write('''{
"report": [
        
]
}''')
                            f.close()
                    
                    
                    
                    if 'rad' in x:
                        cursor.execute("insert into waypoints values (?, ?, ?, ?, ?, ?)",
                        [x['id'], x['desc'], x["rad"], x["lat"], x["lon"], datetime.utcfromtimestamp(x["tst"]).strftime('%Y-%m-%d %H:%M:%S')])    
                        conn.commit()
                        time.sleep(5)
                        with open('.\\db.json', 'w') as f:
                            f.write('''{
"report": [
        
]
}''')
                            f.close()
                    else:
                        print('error')


        



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

