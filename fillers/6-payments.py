import psycopg2
from resources import select, update, loading
import time

start_time = time.time()

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# cursor creation
cur = conn.cursor()
cur.execute("""DROP TABLE stat.payments;""")
cur.execute("""CREATE TABLE stat.payments (
                    patient_id integer,
                    invoice_id integer,
                    consultation_id integer,
                    created_date timestamp without time zone,
                    doctor_id integer,
                    invoice_author character varying(64),
                    payment_method integer,
                    price numeric(12,2) DEFAULT 0,
                    paid numeric(12,2) DEFAULT 0,
                    to_pay numeric(12,2) DEFAULT 0
                    )
            """)

# naplnenie tabulky, udaje z invoices_consultations
rows = select(cur,
              'invoices_consultations.invoice_id, invoices_consultations.consultation_id,invoices_consultations.created_date',
              'invoices_consultations limit 10000 offset 0')
print "\nCREATE stat.payments: \n"

for i, item in enumerate(rows):
    invoice_id = item[0]
    consultation_id = item[1]
    created_date = item[2]
    if item[2] is not None:
        invoice_date = item[2]
    else:
        invoice_date = 'now()'
    if invoice_id or consultation_id is not None:
        cur.execute("""
                        INSERT INTO stat.payments (invoice_id, consultation_id, created_date)
                        VALUES ({0}, '{1}', '{2}')
                    """.format(invoice_id, consultation_id, created_date))

    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

conn.commit()

# update tabulky payments o patient_id
cur.execute("""
                SELECT invoices.invoice_id, invoices.patient_id, stat.payments.invoice_id, invoices.payment_method
                FROM invoices, stat.payments
                WHERE invoices.invoice_id = stat.payments.invoice_id
            """)
rows = cur.fetchall()
print "\n1. UPDATE add patient_id and invoice_date: \n"

for i, item in enumerate(rows):
    invoices_invoice_id = item[0]
    patient_id = item[1]
    payments_invoice_id = item[2]
    if item[1] is not None:
        update(cur, 'stat.payments', 'patient_id', patient_id, 'stat.payments.invoice_id',
               invoices_invoice_id)
    payment_method = item[3]
    if payment_method is not None:
        update(cur, 'stat.payments', 'payment_method', payment_method, 'stat.payments.invoice_id',
               invoices_invoice_id)
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

conn.commit()

# update tabulky payments o invoice_author
cur.execute("""
                SELECT invoices.invoice_author, invoices.invoice_id, osteopaths.osteopath_id, osteopaths.forename, osteopaths.surname
                FROM invoices, anonymized.osteopaths, stat.payments
                WHERE (invoices.invoice_id = payments.invoice_id)
                AND (invoices.invoice_author = osteopaths.osteopath_id)
            """)
rows = cur.fetchall()
print "\n2. UPDATE add invoice_author: \n"

for i, item in enumerate(rows):
    invoice_author = item[0]
    invoices_invoice_id = item[1]
    osteopath_id = item[2]
    if item[2] is not None:
        update(cur, 'stat.payments', 'doctor_id', osteopath_id, 'stat.payments.invoice_id', invoices_invoice_id)
    name = "'" + item[3] + ' ' + item[4] + "'"
    if item[3] is not None:
        update(cur, 'stat.payments', 'invoice_author', name, 'stat.payments.invoice_id', invoices_invoice_id)
    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
conn.commit()

# update payment o paid
cur.execute(""" SELECT patients_consultation_payments.paid, patients_consultation_payments.consultation_id
                FROM patients_consultation_payments, stat.payments
                WHERE payments.consultation_id = patients_consultation_payments.consultation_id""")
rows = cur.fetchall()
print "\n3. UPDATE add paid"

for i, item in enumerate(rows):
    paid_temp = item[0]
    consultation_id = item[1]
    if consultation_id is not None:
        cur.execute(
            """update stat.payments SET paid = paid + {0} where consultation_id = {1}""".format(paid_temp,
                                                                                                consultation_id))

    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

conn.commit()

# update payments o plnu sumu
# 1st step
cur.execute(""" SELECT patients_consultation_treatments.consultation_id, patients_consultation_treatments.price
                FROM patients_consultation_treatments, stat.payments
                WHERE patients_consultation_treatments.consultation_id = payments.consultation_id """)
rows = cur.fetchall()
print "\n4. UPDATE add price (1st step)"

for i, item in enumerate(rows):
    consultation_id = item[0]
    price = item[1]
    if price is None:
        price = 0
    if consultation_id is not None:
        cur.execute("""update stat.payments SET price = price + {0} where consultation_id = {1}""".format(price,
                                                                                                          consultation_id))

    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)
conn.commit()

# 2nd step   -- IF Zaporna suma -> predpoklad ze chybaju data v DB
cur.execute("""SELECT patient_consultation_kineo.consultation_id, patient_consultation_kineo.calculated_honorarium
               FROM patient_consultation_kineo, stat.payments
               WHERE patient_consultation_kineo.consultation_id = payments.consultation_id""")
rows = cur.fetchall()
print "\n5. UPDATE add price (2nd step)"

for i, item in enumerate(rows):
    consultation_id = item[0]
    price = item[1]
    if price is None:
        price = 0
    if consultation_id is not None:
        cur.execute("""update stat.payments SET price = price + {0} where consultation_id = {1}""".format(price,
                                                                                                          consultation_id))

    # nepotrebne ale len pre moje info ako ide vkladanie
    loading((len(rows)), i)

# update payments o to_pay
cur.execute("""update stat.payments SET to_pay = price - paid """)

# set patient_id to NOT NULL
cur.execute("ALTER TABLE stat.payments ALTER COLUMN patient_id SET NOT NULL ")

conn.commit()
print("\n\n\n--- %s seconds ---" % (time.time() - start_time))
