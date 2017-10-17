#!/usr/bin/env python3
import sys


def raw_data(salary_dic,*data):
    list_employee=data[0]
    del list_employee[0]
    for i in list_employee:
        tmp = i.split(':')
        try:
            salary_dic[tmp[0]] =int(tmp[1])
        except:
            print('Parameter Error')
    return salary_dic   

def insurance(salary):
    insurance =int(salary)*0.165
    #print('insurance:',insurance)
    return insurance


def revenue(salary,insurance):
    before_tax = salary-insurance
    a = before_tax - 3500
    if a <= 0:
        revenue = before_tax
    elif a<= 1500:
        revenue = salary-insurance-a*0.03
    elif a<= 4500:
        revenue = salary-insurance-a*0.1+105
    elif a<= 9000:
        revenue = salary-insurance-a*0.2+555
    elif a<= 35000:
        revenue = salary-insurance-a*0.25+1005
    elif a<= 55000:
        revenue = salary-insurance-a*0.3+2755
    elif a<= 80000:
        revenue = salary-insurance-a*0.35+5505
    else:
        revenue = salary-insurance-a*0.45+13505
    return revenue

def caculate():
    salary_dic1 = raw_data(salary_dic,sys.argv)
    for id,salary in salary_dic1.items():
        insurance_dic[id] = insurance(salary)
        pure_income_dic[id] = format(revenue(salary,insurance_dic[id]),'.2f')   
#print(pure_income_dic)
    for i,n in pure_income_dic.items():
        print(i,':',n)
if __name__=="__main__":
    salary_dic={}
    insurance_dic={}
    pure_income_dic={}
    caculate()

