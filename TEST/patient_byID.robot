*** Settings ***
Documentation     Automaticky test pre ziskanie pacienta podla ID

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Otvorenie prehliadaca a vykonanie requestu
    make request    patientById

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400

test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /patient/0/postal_code    "6523 KW"
	json value should equal     ${body}    /patient/0/city    "Nijmegen"
	json value should equal     ${body}    /patient/0/latitude    51.831229761
	json value should equal     ${body}    /patient/0/longitude    5.886055459