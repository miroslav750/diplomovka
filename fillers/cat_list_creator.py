# -*- coding: utf-8 -*-

import psycopg2, time, json, re
from googletrans import Translator



# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"


# cursor creation
cur = conn.cursor()

# creation of dictionary for categorization
f = open('categories.txt','w')
cur.execute(""" SELECT distinct(product_en) FROM stat.products""")
rows = cur.fetchall()
for row in rows:
    if row[0] is not None:
        f.write(row[0] + "\n")
f.close()