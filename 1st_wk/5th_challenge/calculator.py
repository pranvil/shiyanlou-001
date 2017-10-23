#!/usr/bin/env python3
import sys,os
import csv
import getopt,configparser,datetime
from multiprocessing import Process, Queue

q_userdata = Queue()
q_result = Queue()

class config(object):
    def __init__(self,cfgfile,city):
        self.config = {}
        config = configparser.ConfigParser()
        config.read(cfgfile)
        try:
            for key in config[city]:
                value = config.get(city,key)
                self.config[key] = float(value.strip())

        except:
            print('Config file parameter Error,please check you config file')
            sys.exit(1)
            
    def get_config(self,key):
        value = self.config[key]
        return value

    def get_total_rate(self):
        rate_category=['YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']
        rate = 0
        for i in rate_category:
            rate += self.get_config(i)
            rate = float(rate)    
        return rate


class userdata(Process):
    def run(self,userfile):
        self.userdata = {}
        try:
            with open(userfile,'r') as file:
                for line in file:
                    tmp = line.split(',')
                    self.userdata[tmp[0].strip()] = float(tmp[1].strip())
        except:
            print('userdata Parameter Error')
            sys.exit(1)
        q_userdata.put(self.userdata)
    

class calculate(Process):
    def __init__(self,cfgfile):
        self.JiShuL = config(cfgfile).get_config('JiShuL')
        self.JiShuH = config(cfgfile).get_config('JiShuH')
        self.rate = config(cfgfile).get_total_rate()
        
    def tax(self,salary,tax_rate,quick_deduction):
#        print('salary:',salary,'tax_rate:',tax_rate,'deduction:',quick_deduction)
        insurance = self.insurance(salary)
        tax_part = float(salary) - insurance - 3500
        if tax_part <= 0:
            tax = 0
        else:
            tax = tax_part * tax_rate - quick_deduction
#        print('Need tax:',tax_part)
        return tax
        

    def insurance(self,salary):
        if float(salary) < self.JiShuL:
            insurance_part = self.JiShuL
        elif float(salary) > self.JiShuH:
            insurance_part = self.JiShuH
        else:
            insurance_part = salary
        insurance = float(insurance_part)*self.rate
        return insurance

    def run(self):
        user_info=[]
        userdata=q_userdata.get()
        for key,salary in userdata.items():
            insurance = self.insurance(salary)
            a = float(salary) - insurance -3500
            if a <=0:
                tax_rate = float(0)
                quick_deduction = 0
                tax = self.tax(salary,tax_rate,quick_deduction)
            elif a <=1500:
                tax_rate = float(0.03)
                quick_deduction = 0
# print(tax_rate,salary)
                tax = self.tax(salary,tax_rate,quick_deduction)            
            elif a <=4500:
                tax_rate = float(0.1)
                quick_deduction = 105
                tax = self.tax(salary,tax_rate,quick_deduction)
            elif a <=9000:
                tax_rate = float(0.2)
                quick_deduction = 555
                tax = self.tax(salary,tax_rate,quick_deduction)
            elif a <=35000:
                tax_rate = float(0.25)
                quick_deduction = 1005
                tax = self.tax(salary,tax_rate,quick_deduction)
            elif a <=55000:
                tax_rate = float(0.3)
                quick_deduction = 2755
                tax = self.tax(salary,tax_rate,quick_deduction)
            elif a <=80000:
                tax_rate = float(0.35)
                quick_deduction = 5505
                tax = self.tax(salary,tax_rate,quick_deduction)
            else:
                tax_rate = float(0.45)
                quick_deduction = 13505
                tax = self.tax(salary,tax_rate,quick_deduction)            
            #ID,salary,insurance,tax,income             
            pure_income = float(salary) - insurance - tax
            insurance = format(insurance,'.2f')           
            tax = format(tax,'.2f')           
            pure_income = format(pure_income,'.2f')           
            salary = format(salary,'.2f')           
            tmp=[key,salary,insurance,tax,pure_income]
            user_info.append(tmp)
#       print('line115-userinfo:',user_info[2])
        q_result.put(user_info)        
class write_data(Process):
    def run(result):
        final_result = q_result.get(timeout=1)
        with open(result,'w') as file:
            writer = csv.writer(file)
            writer.writerows(final_result)
if __name__ =='__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hC:c:d:o:", ["help"])
    except getopt.GetoptError as err:        
        print("option does not recognized")          
        sys.exit(1)
    for m, n in opts:
        if "-h" or '--help' in m:
            print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')
            sys.exit(1)
        if '-C' in m:
            index_city = args.index('-C')+1
            config_city = args[index_city].upper()
        else:
            config_city = 'DEFAULT'

    index_user = args.index('-d')+1
    index_config = args.index('-c')+1
    index_output = args.index('-o')+1

    cfgfile = args[index_config]
    userfile = args[index_user]
    result = args[index_output]
    t = [userfile,cfgfile]
    for i in t:
        if os.path.exists(i):
            pass
        else:
            print('file does not exist')
            sys.exit(1)

    userdata().run(userfile)
    calculate(cfgfile).run()
    write_data.run(result)
    with open(result,'r') as file:
        for line in file:
            print(line)
