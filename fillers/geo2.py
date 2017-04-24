import psycopg2
import time

start_time = time.time()
from resources import loading, select, update, edit

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()

# update basic, add GPS coordinates of patient
cur.execute("""
                SELECT basic.postal_code, geo.postal_code, geo.latitude, geo.longitude, basic.latitude
                FROM stat.basic, stat.geo
                WHERE (basic.postal_code = geo.postal_code)
                AND (basic.latitude =0)
                AND (geo.latitude <> 0)
                GROUP BY basic.postal_code, geo.postal_code, geo.latitude, geo.longitude, basic.latitude
            """)
rows = cur.fetchall()
print "\n1. UPDATE stat.basic, adding coordinates"

for i, item in enumerate(rows):
    postal1 = edit(item[0])
    print  postal1
    x = item[2]
    y = item[3]
    update(cur, 'stat.basic', 'latitude', x, 'postal_code', "'" + postal1 + "'")
    update(cur, 'stat.basic', 'longitude', y, 'postal_code', "'" + postal1 + "'")
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
    conn.commit()
