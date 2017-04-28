# -*- coding: utf-8 -*-

import psycopg2, time, json, re
from resources import loading, select, update, edit, diacritics, delete_apostrophe
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
cur.execute("DROP TABLE stat.products")  # uncomment to drop DB before creating
cur.execute("""CREATE TABLE stat.products
                            (consultation_id integer NOT NULL,
                            product_id integer,
                            product character varying(225),
                            product_en character varying(225),
                            category character varying(64)
                            )
            """)

# naplnenie tabulky, udaje z patients_consultation_treatments
rows = select(cur, 'consultation_id, product_id', 'patients_consultation_treatments')
print "\nCREATE stat.products: \n"

for i, item in enumerate(rows):
    consultation_id = item[0]
    product_id = item[1]
    if product_id is not None:
        cur.execute("""
                        INSERT INTO stat.products (consultation_id, product_id)
                        VALUES ({0}, '{1}')
                    """.format(consultation_id, product_id))

    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
conn.commit()

# update tabulky products o product
rows = select(cur, 'product_id, product_name', 'shop_product')
print "\n1. UPDATE stat.products: \n"
for i, item in enumerate(rows):
    product_id = item[0]
    product = edit(item[1])
    if product_id is not None:
        cur.execute("""update stat.products SET product = '{0}' where product_id = {1}""".format(product, product_id))
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
conn.commit()

# update tabulky o produkty z nomenclature tabulky
cur.execute("""SELECT nomenclature_pathologies.pathology_title, nomenclature_pathologies.pathology_id, nomenclatures.pathology_id, nomenclatures.nomenclature_id,
                    patients_consultation_nomenclature.nomenclature_id, patients_consultation_nomenclature.consultation_id
                FROM nomenclature_pathologies, nomenclatures,patients_consultation_nomenclature
                WHERE (nomenclature_pathologies.pathology_id = nomenclatures.pathology_id)
                AND (nomenclatures.nomenclature_id = patients_consultation_nomenclature.nomenclature_id)
                GROUP BY nomenclature_pathologies.pathology_title, nomenclature_pathologies.pathology_id, nomenclatures.pathology_id, nomenclatures.nomenclature_id,
                    patients_consultation_nomenclature.nomenclature_id, patients_consultation_nomenclature.consultation_id
                ORDER BY consultation_id
            """)
rows = cur.fetchall()
print "\n2. UPDATE stat.products: \n"
for i, item in enumerate(rows):
    consultation_id = item[5]
    product = edit(item[0])
    if product_id is not None:
        cur.execute(
            """update stat.products SET product = CONCAT(product,', {0}') where consultation_id = {1}""".format(product,
                                                                                                                consultation_id))
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

# update tabulky products o product_en
rows = select(cur, 'distinct(product)', 'stat.products')
print "\n3. UPDATE stat.products: \n"
for i, item in enumerate(rows):
    try:
        product = delete_apostrophe(item[0])
        bez_dia = str(diacritics(product))
        translation = translator.translate(bez_dia, dest='en')
        product_en = translation.text.encode('UTF-8')
        product_en = delete_apostrophe(product_en)
        if product_en is not None:
            cur.execute(
                """update stat.products SET product_en = '{0}' where product = '{1}'""".format(product_en, product))
    except UnicodeEncodeError:
        print " - - ERROR - -"
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
conn.commit()

conn.commit()
print("\n\n\n--- %s seconds ---" % (time.time() - start_time))
