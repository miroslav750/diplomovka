*** Settings ***
Documentation     Automaticky test pre ziskanie zaznamov platby podla ID

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Otvorenie prehliadaca a vykonanie requestupaymentspen
    make request    payments

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400


test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /payments/0/created date     "2013-12-20 11:52:53.023426"
	json value should equal     ${body}    /payments/0/consultation ID      4889605
	json value should equal     ${body}    /payments/0/doctorID        1025
	json value should equal     ${body}    /payments/0/paid     6.84
	json value should equal     ${body}    /payments/0/patient ID       1367822
	json value should equal     ${body}    /payments/0/PRICE       6.84
	json value should equal     ${body}    /payments/0/to pay       0.0
	json value should equal     ${body}    /payments/0/invoice ID       98034

