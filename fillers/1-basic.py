import psycopg2
from resources import select, loading, edit
import time

start_time = time.time()

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()

# cur.execute("""DROP TABLE stat.basic;""")
cur.execute("""CREATE TABLE stat.basic (
                    patient_id integer NOT NULL UNIQUE,
                    forename character varying(64),
                    surname character varying(64),
                    city character varying(64),
                    street character varying(64),
                    postal_code character varying(32),
                    latitude numeric NOT NULL DEFAULT 0,
                    longitude numeric NOT NULL DEFAULT 0
                    )
            """)

# naplnenie tabulky, udaje o pacientovi z PATIENTS
rows = select(cur, 'patient_id, forename, surname, address_city, address_street, address_postalcode',
              'anonymized.patients')
print "CREATE basic: \n"

for i, item in enumerate(rows):
    patient_id = item[0]
    forename = edit(item[1])
    surname = edit(item[2])
    city = edit(item[3])
    if city is None or city == 'None':
        city = ""
    street = edit(item[4])
    if street is None or street == 'None':
        street = ""
    postal_code = edit(item[5])
    if postal_code is None or postal_code == 'None':
        postal_code = ""
    cur.execute("""
                    INSERT INTO stat.basic (patient_id, forename, surname, city, street, postal_code)
                    VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}')
                """.format(patient_id, forename, surname, city, street, postal_code))
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

conn.commit()
print("\n\n\n--- %s seconds ---" % (time.time() - start_time))
