*** Settings ***
Documentation     Automaticky test pre ziskanie zoznamu 100 miest s najvacsim poctom pacientov

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Vykonanie requestu
    make request    mostPatients

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400


test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /number of patients/0/CITY    "unidentified"
	json value should equal     ${body}    /number of patients/0/number of patients    249468
	json value should equal     ${body}    /number of patients/1/CITY    "Amsterdam"
	json value should equal     ${body}    /number of patients/1/number of patients    56394
