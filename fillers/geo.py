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
# cur.execute("DROP TABLE stat.GEO")            # uncomment to drop DB before creating
cur.execute("""CREATE TABLE stat.GEO
                            (postal_code character varying(64),
                            latitude numeric NOT NULL DEFAULT 0,
                            longitude numeric NOT NULL DEFAULT 0,
                            found boolean DEFAULT FALSE)
            """)

cur.execute("select distinct postal_code from stat.basic")
rows = cur.fetchall()
for i, item in enumerate(rows):
    postal_code = edit(item[0])
    if postal_code is not None:
        cur.execute("INSERT INTO stat.GEO (postal_code) VALUES ('{0}')".format(postal_code))
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)


conn.commit()
