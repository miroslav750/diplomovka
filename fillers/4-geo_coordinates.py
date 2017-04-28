import psycopg2
import time
from geopy.geocoders import ArcGIS
from geopy.exc import GeocoderTimedOut

start_time = time.time()
from resources import update, select, edit, delete_apostrophe

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()
while True:

    # update stat.basic o GPS suradnice
    # pocet neprevedenych suradnic
    count = cur.execute("select count(*) from stat.geo where found = False")
    count = cur.fetchall()
    count = count[0][0] - 1

    rows = select(cur, 'GEO.postal_code, GEO.found', 'stat.GEO  where found = False')
    print "\n UPDATE stat.GEO, adding GPS from postal codes. . . "
    geolocator = ArcGIS()
    i = 0
    maximum = 200

    if count < maximum:
        maximum = count

    while i <= maximum:
        found = rows[count][1]
        if found is False:
            # time.sleep(1.1)
            print rows[count]
            try:
                postal_code = rows[count][0]
                postal_code = edit(postal_code)
                location = geolocator.geocode(postal_code)
                if location is not None:
                    latitude = location.latitude
                    longitude = location.longitude
                    update(cur, 'stat.GEO', 'latitude', latitude, 'postal_code', "'" + postal_code + "'")
                    update(cur, 'stat.GEO', 'longitude', longitude, 'postal_code', "'" + postal_code + "'")
                    update(cur, 'stat.GEO', 'found', True, 'postal_code', "'" + postal_code + "'")
                    i += 1
                    conn.commit()
                    print "vkladam zaznam cislo: %s " % i
                else:
                    update(cur, 'stat.GEO', 'found', True, 'postal_code', "'" + postal_code + "'")
                    i += 1
                    print "CHYBA pri zazname cislo: %s " % i
                count -= 1
            except GeocoderTimedOut:
                print "- - ERROR - -"
    conn.commit()
    # print 'teraz pockajte 30 min'
    # time.sleep(600)
    # print 'este 20  min'
    # time.sleep(600)
    # print 'este 10 min'
    # time.sleep(600)
    time.sleep(30)
    print 'DALSIA ITERACIA'
