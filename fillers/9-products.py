# -*- coding: utf-8 -*-

import psycopg2, time, json, re
from resources import loading, select, update, delete_apostrophe, diacritics, delete_apostrophe
from googletrans import Translator

translator = Translator()
start_time = time.time()

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()

# CATEGORIZATION
json_data = open('categories.json').read()
dictionary = json.loads(json_data)
cur.execute(""" SELECT distinct(product_en) FROM stat.products""")
rows = cur.fetchall()
for row in rows:
    product_en = delete_apostrophe(row[0])
    category = [cat for cat in dictionary if
                any(marker in re.findall(r'[a-z0-9]+', product_en) for marker in dictionary[cat])]
    if category == []:
        category = 'uncategorized'
        cur.execute(
            """update stat.products SET category = '{0}' where product_en = '{1}'""".format(category, product_en))
    else:
        category = category[0]
        cur.execute(
            """update stat.products SET category = '{0}' where product_en = '{1}'""".format(category, product_en))

conn.commit()
print("\n\n\n--- %s seconds ---" % (time.time() - start_time))
