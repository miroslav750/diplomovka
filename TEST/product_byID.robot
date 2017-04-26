*** Settings ***
Documentation     Automaticky test pre ziskanie zaznamu produktu podla ID

Resource          resource.robot
Suite Teardown    Close All Browsers

*** Test Cases ***

Otvorenie prehliadaca a vykon
    make request    productById

test na result code 200
    response status code should equal   200

test na bad result code 400
    response status code should not equal   400


test na spravnu odpoved v tele a validny JSON
	${body}=    get response body
	should be valid json  ${body}
	json value should equal     ${body}    /product/0/product ID    14869
	json value should equal     ${body}    /product/0/product    "Supp. Accomodatie Tennisdel"
	json value should equal     ${body}    /product/0/product (EN)    "Supp. "