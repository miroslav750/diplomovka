from bottle import route, run, request, HTTPResponse
import psycopg2
from fillers.resources import delete_apostrophe, edit

# connection to database
try:
    conn = psycopg2.connect("dbname='diplomovka' user='bart' host='localhost' password='miro'")
except:
    print "Unable to connect to the database"

# defininicia chybovych hlasok
def_error = "ospravedlnujeme sa nastala chyba"

# - - - BASIC REQUESTY - - -

# vrati yakladne udaje o pacientovi po [offset] zaznamov
@route("/patients", method='POST')
def get_users():
    try:
        offset = request.query.offset
        offset = int(offset)
    except :
        return HTTPResponse(status=400, body="nespravne zadany OFFSET, zadajte cislo")

    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT patient_id, forename, surname from stat.basic ORDER BY patient_id ASC LIMIT 100 OFFSET {}""".format(
                offset))
        rows = cur.fetchall()

        output = {"patients": []}

        for row in rows:
            output['patients'].append(
                {
                    "patient ID": row[0],
                    "forename": row[1],
                    "surname": row[2]
                }
            )

        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# vrati zakladne udaje o pacientovi podla jeho ID
@route("/patient/<patient_id>", method='POST')
def get_user(patient_id):
    cur = conn.cursor()
    try:
        cur.execute("""SELECT patient_id, forename, surname, city, street, postal_code, latitude, longitude 
                       FROM stat.basic WHERE patient_id = {} """.format(patient_id))
        rows = cur.fetchall()

        output = {"patient": []}

        for row in rows:
            output['patient'].append(
                {
                    "patient ID": int(row[0]),
                    "forename": edit(row[1]),
                    "surname": edit(row[2]),
                    "city":edit(row[3]),
                    "street":edit(row[4]),
                    "postal_code":edit(row[5]),
                    "latitude":float(row[6]),
                    "longitude":float(row[7])
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# vrati zakladne udaje o doktorovi podla jeho ID
@route("/doctor/<doctor_id>", method='POST')
def get_doctors(doctor_id):
    cur = conn.cursor()
    try:
        cur.execute("""SELECT doctor_id, doctor_name, postal_code, latitude, longitude 
                       FROM stat.doctors WHERE doctor_id = {} """.format(doctor_id))
        rows = cur.fetchall()

        output = {"doctor": []}

        for row in rows:
            output['doctor'].append(
                {
                    "doctor ID": int(row[0]),
                    "doctor name": edit(row[1]),
                    "postal_code": edit(row[2]),
                    "latitude": float(row[3]),
                    "longitude": float(row[4])
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# vrati pacientove konzultacie, faktury, platby podla jeho ID
@route("/payments/<patient_id>", method='POST')
def get_payments(patient_id):
    cur = conn.cursor()
    try:
        cur.execute("""SELECT patient_id, invoice_id, consultation_id, created_date, doctor_id, invoice_author, payment_method, price, paid, to_pay
                       FROM stat.payments
                       WHERE patient_id = {} """.format(patient_id))
        rows = cur.fetchall()

        output = {"payments": []}

        for row in rows:
            output['payments'].append(
                {
                    "patient ID": int(row[0]),
                    "invoice ID": int(row[1]),
                    "consultation ID": int(row[2]),
                    "created date": str(row[3]),
                    "doctorID": int(row[4]),
                    "invoice author": str(row[5]),
                    "payment method": str(row[6]),
                    "PRICE": float(row[7]),
                    "paid": float(row[8]),
                    "to pay": float(row[9])
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# vrati produkt podla jeho ID
@route("/product/<product_id>", method='POST')
def get_products(product_id):
    cur = conn.cursor()
    try:
        cur.execute("""SELECT distinct(product_id), product, product_en, category
                       FROM stat.products 
                       WHERE product_id = {} """.format(product_id))
        rows = cur.fetchall()

        output = {"product": []}

        for row in rows:
            output['product'].append(
                {
                    "product ID": int(row[0]),
                    "product": edit(row[1]),
                    "product (EN)": edit(row[2]),
                    "category": edit(row[3])
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# - - - SPECIAL REQUESTY - - -

# vrati pocet pacientov pre jednotlive mesta
@route("/most_patients", method='POST')
def get_most_patients():
    cur = conn.cursor()
    try:
        cur.execute("""SELECT city, count(*)
                       FROM stat.basic
                       GROUP BY city
                       ORDER BY count(*) desc
                       LIMIT 10""")
        rows = cur.fetchall()

        output = {"number of patients": []}

        for row in rows:
            output['number of patients'].append(
                {
                    "CITY": edit(row[0]),
                    "number of patients": int(row[1])
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)


# komplet request vrati vsetko potrebne pre katarininu cast DP
# KATARINA
@route("/all", method='POST')
def all():
    cur = conn.cursor()
    try:
        cur.execute(""" SELECT  basic.patient_id, basic.forename, basic.surname, basic.city, basic.latitude, basic.longitude,
                                doctors.doctor_id, doctors.doctor_name, doctors.latitude, doctors.longitude,
                                payments.consultation_id, payments.created_date, payments.price, payments.paid, payments.to_pay,
                                products.product_id, products.product_en, products.category
                        FROM stat.basic, stat.doctors, stat.payments, stat.products
                        WHERE basic.patient_id = payments.patient_id
                        AND doctors.doctor_id = payments.doctor_id
                        AND products.consultation_id = payments.consultation_id
                        limit 1000""")
        rows = cur.fetchall()

        output = {"data":[]}
        for row in rows:
            consultation_gps_lat = row[8]
            consultation_gps_lon = row[9]
            patient_id = row[0]
            patient_forename = row[1]
            patient_surname = row[2]
            patient_address = row[3]
            patient_gps_lat = row[4]
            patient_gps_lon = row[5]
            consultation_datetime = row[11]
            consultation_author = row[6]
            doctor_name = delete_apostrophe(row[7])
            product_id = row[15]
            nomenclature = row[16]
            nomenclature_category = row[17]
            consultation_id = row[10]
            price = row[12]
            paid = row[13]
            to_pay = row[14]
            output["data"].append(
                {
                    "consultation_location": "None",
                    "consultation_gps_lat": float(consultation_gps_lat),
                    "consultation_gps_lon": float(consultation_gps_lon),
                    "patient_id": int(patient_id),
                    "patient_forename": patient_forename,
                    "patient_surname": patient_surname,
                    "patient_address": patient_address,
                    "patient_gps_lat": float(patient_gps_lat),
                    "patient_gps_lon": float(patient_gps_lon),
                    "consultation_datetime": str(consultation_datetime),
                    "consultation_author": int(consultation_author),
                    "doctor_name": doctor_name,
                    "nomenclature_id": int(product_id),
                    "nomenclature": nomenclature,
                    "nomenclature_category": str(nomenclature_category),
                    "consultation_id": int(consultation_id),
                    "price": float(price),
                    "paid": float(paid),
                    "to_pay": float(to_pay)
                }
            )
        return output
    except:
        return HTTPResponse(status=400, body=def_error)


run(host='localhost', port=8080, debug=True, reloader=True)
