*** Settings ***
Documentation     Resource file pre atutomatizovane testy mojej diplomovej prace
Library           Selenium2Library
Library           BuiltIn
Library           HttpLibrary.HTTP

*** Variables ***
${SERVER}         http://localhost:8080
${BROWSER}        Chrome
${DELAY}          0

${patientID}    550086
${limit}    10
${offset}    10
${doctorID}    268
${paymentID}    1367822
${productID}    14869

${patient_byID}      ${SERVER}/patient/${patientID}
${patients}      ${SERVER}/patients/${limit}/${offset}
${doctor_byID}      ${SERVER}/doctor/${doctorID}
${payments}      ${SERVER}/payments/${paymentID}
${product_byID}      ${SERVER}/product/${productID}
${most_patients}      ${SERVER}/most_patients



*** Keywords ***

make request
    [Arguments]    ${request_url}
    run keyword if    "${request_url}" == "patientById"     POST  ${patient_byID}
    run keyword if    "${request_url}" == "patients"    POST  ${patients}
    run keyword if    "${request_url}" == "doctorById"     POST  ${doctor_byID}
    run keyword if    "${request_url}" == "payments"     POST  ${payments}
    run keyword if    "${request_url}" == "productById"     POST  ${product_byID}
    run keyword if    "${request_url}" == "mostPatients"     POST  ${most_patients}






