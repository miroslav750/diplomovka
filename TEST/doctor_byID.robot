*** Settings ***
Documentation     Automaticky test pre ziskanie zaznamu doktora podla ID

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Otvorenie prehliadaca a vykonanie requestu
    make request    doctorById

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400


test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /doctor/0/doctor ID    268
	json value should equal     ${body}    /doctor/0/postal_code    "1131"
	json value should equal     ${body}    /doctor/0/doctor name    "Forename268 Surname268"
	json value should equal     ${body}    /doctor/0/latitude    47.538700027
	json value should equal     ${body}    /doctor/0/longitude    19.093330434
