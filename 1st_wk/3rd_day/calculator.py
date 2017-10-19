#!/usr/bin/env python3
import sys
import os
import csv

class Config(object):
    def __init__(self,configfile):
        self.config = {}
        with open(configfile,'r') as file:
            for line in file:
                tmp = line.split('=')
                self.config[tmp[0].strip()] = tmp[1].strip()
    def get_config(self,key):
        value = self.config[key]
        return value

    def get_total_rate(self):
        rate_category=['YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']
        rate = 0
        for i in rate_category:
            rate = float(self.get_config(i)) + float(rate)          
        return rate



class DataProcess(object):
    def __init__(self,userfile):
        self.userdata = {}
        with open(userfile,'r') as file:
            for line in file:
                tmp = line.split(',')
                self.userdata[tmp[0].strip()] = tmp[1].strip()
            
##    def get_userdata(self,key):
##        value = self.userdata[key]
##        print(value)
##        return value
    
  
    def output(self,confile,result):
        config_data = Config(confile)
        rate = config_data.get_total_rate()
        for key,value in self.userdata.items():
            if float(value) < float(config_data.get_config('JiShuL')):
                value = config_data.get_config('JiShuL')
            elif float(value) > float(config_data.get_config('JiShuH')):                
                value = config_data.get_config('JiShuH')            
            pure_income = self.calculate(value,rate)
            final_result = [key,self.userdata[key],format(pure_income[0],'.2f'),format(pure_income[1],'.2f'),format(pure_income[2],'.2f')]
            
            with open(result,'a') as file:
                writer = csv.writer(file)
                writer.writerow(final_result)
                          
#            print(final_result)
                        

    def calculate(self,salary,rate):        
        insurance = float(salary)*rate
        before_tax = float(salary)-float(insurance)
        a = before_tax - 3500                
                
        tmp = float(salary)-float(insurance)
        if a <= 0:
            revenue = before_tax
            tax = 0
        elif a<= 1500:
            revenue = tmp-a*0.03
            tax = a*0.03
        elif a<= 4500:
            revenue = tmp-a*0.1+105
            tax = a*0.1-105
        elif a<= 9000:
            revenue = tmp-a*0.2+555
            tax = a*0.2-555
        elif a<= 35000:
            revenue = tmp-a*0.25+1005
            tax = a*0.25-1005
        elif a<= 55000:
            revenue = tmp-a*0.3+2755
            tax = a*0.3-2755
        elif a<= 80000:
            revenue = tmp-a*0.35+5505
            tax = a*0.35-5505
        else:
            revenue = tmp-a*0.45+13505
            tax = a*0.45-13505
        return insurance,tax,revenue



if __name__=="__main__":    
    args = sys.argv[1:]
    index_config = args.index('-d')+1
    index_user = args.index('-c')+1
    index_output = args.index('-o')+1
    user = args[index_config]
    confile = args[index_user]
    result = args[index_output]
    t = [user,confile,result,'-c','-d','-o']
    for i in t:
        if os.path.exists(i):
            pass
        else:
            print('file did not exist or parameter incorrect')
            os._exit(0)
    userdata = DataProcess(user)
    userdata.output(confile,result)
    with open(result) as file:
        for line in file:
            print(line)
