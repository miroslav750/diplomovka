import psycopg2
import time
from resources import select, update, edit
from geopy.geocoders import ArcGIS


start_time = time.time()
from resources import loading

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()
# cur.execute("DROP TABLE stat.doctors")
cur.execute("""CREATE TABLE stat.doctors
                            (doctor_id integer,
                            doctor_name character varying(64),
                            postal_code character varying(32),
                            latitude numeric NOT NULL DEFAULT 0,
                            longitude numeric NOT NULL DEFAULT 0,
                            found boolean DEFAULT FALSE)
            """)
# naplnenie tabulky doctors z tabulky osteopaths
rows = select(cur, 'osteopath_id, forename, surname, address_postalcode', 'anonymized.osteopaths')
print "\nCREATE stat.doctors: \n"

for i, item in enumerate(rows):
    doctor_id = item[0]
    name = "'" + item[1] + ' ' + item[2] + "'"
    name =  edit(name)
    postal_code = item[3]
    if postal_code is not None:
        cur.execute("INSERT INTO stat.doctors (doctor_id, doctor_name, postal_code) VALUES ('{0}','{1}','{2}')".format(doctor_id,name,postal_code))
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

# UPDATE doctors o GPS suradnice
# pocet neprevedenych suradnic
count = cur.execute("select count(*) from stat.doctors where found = False")
count = cur.fetchall()
count = count[0][0] - 1

rows = select(cur, 'postal_code, found', 'stat.doctors where found = False')
print "\n UPDATE stat.doctors, adding GPS from postal codes. . . "
geolocator = ArcGIS()
i = 0
maximum = 200

if count < maximum:
    maximum = count

while i <= maximum:
    found = rows[count][1]
    if found is False:
        time.sleep(1.1)
        postal_code = rows[count][0]
        location = geolocator.geocode(postal_code)
        if location is not None:
            latitude = location.latitude
            longitude = location.longitude
            update(cur, 'stat.doctors', 'latitude', latitude, 'postal_code', "'" + postal_code + "'")
            update(cur, 'stat.doctors', 'longitude', longitude, 'postal_code', "'" + postal_code + "'")
            update(cur, 'stat.doctors', 'found', True, 'postal_code', "'" + postal_code + "'")
            i += 1
            print "vkladam zaznam cislo: %s " % i
        else:
            update(cur, 'stat.doctors', 'found', True, 'postal_code', "'" + postal_code + "'")
            i += 1
            print "CHYBA pri zazname cislo: %s " % i
        count -= 1

conn.commit()
print("\n\n\n--- %s seconds ---" % (time.time() - start_time))

