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
                    "patient_id": row[0],
                    "forename": row[1],
                    "surname": row[2]
                }
            )

        return output
    except:
        return HTTPResponse(status=400, body=def_error)

# vrati zakladne udaje o pacientovi podla jeho ID
@route("/patient/<patient_id>", method='POST')
def get_users(patient_id):
    cur = conn.cursor()
    try:
        cur.execute("""SELECT patient_id, forename, surname, city, street, postal_code, latitude, longitude 
                       FROM stat.basic WHERE patient_id = {} """.format(patient_id))
        rows = cur.fetchall()

        output = {"patients": []}

        for row in rows:
            output['patients'].append(
                {
                    "patient_id": int(row[0]),
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