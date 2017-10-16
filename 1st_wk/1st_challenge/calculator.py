#!/usr/bin/env python3
import sys
import os
try:
    salary = int(sys.argv[1])
    if type(salary) == int:
        if salary <0:
            print('Please enter postive value!')          
            os._exit(0) 
        #salary = format(salary,'.2f')
except:
    print('Parameter Error')
    os._exit(0)

#print(type(salary))
a = salary - 3500
if a <= 1500:
    tax = a*0.03
elif a<= 4500:
    tax = a*0.1-105
elif a<= 9000:
    tax = a*0.2-555
elif a<= 35000:
    tax = a*0.25-1005
elif a<= 55000:
    tax = a*0.3-2755
elif a<= 80000:
    tax = a*0.35-5505
else:
    tax = a*0.45-13505

print(format(tax,'.2f'))
