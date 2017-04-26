*** Settings ***
Documentation     Automaticky test pre ziskanie zaznamov 10-tich pacientov

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Otvorenie prehliadaca a vykonanie requestu
    make request    patients

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400


test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /patients/0/patient ID    25
	json value should equal     ${body}    /patients/9/patient ID    610
	json value should equal     ${body}    /patients/0/surname    "pSurname25"

