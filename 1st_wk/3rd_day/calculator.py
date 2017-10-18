#!/usr/bin/env python3
import sys
import os
import json

class Config(object):
    def __init__(self,configfile):
        self.config = {}
        with open(configfile,'r') as file:
            for line in file:
                tmp = line.split('=')
                self.config[tmp[0].strip()] = tmp[1].strip()
        print(self.config)
    def get_config(self,key):
        value = self.config[key]
        print(value)
        return value

class DataProcess(object):
    def __init__(self,userfile):
        self.userdata = {}
        with open(userfile,'r') as file:
            for line in file:
                tmp = line.split(',')
                self.userdata[tmp[0].strip()] = tmp[1].strip()
            print(self.userdata)
    def get_userdata(self, key):
        value = self.userdata[key]
        print(value)
        return value
    
    def get_userdata(self):
        pass
    def calculate(self):
        pass


    def dumptofile(self,outputfile):
       pass



if __name__=="__main__":
    test = Config('test.cfg')
    test.get_config('YiLiao')
    userdata = DataProcess('user.csv')
    userdata.get_userdata('203')
