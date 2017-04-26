@echo off
:: " call robot -d [mietso ulozenia vystupu] [nazov test suboru] "
:: POZOR nepouzivat DIAKRITIKU


call robot -d ../test_output/most_patients              most_patients.robot
call robot -d ../test_output/product_byID              product_byID.robot
call robot -d ../test_output/payment_byID              payment_byID.robot
call robot -d ../test_output/doctor_byID               doctor_byID.robot
call robot -d ../test_output/patients               patients.robot
call robot -d ../test_output/patient_byID               patient_byID.robot


pause