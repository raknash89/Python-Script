# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:33:49 2022

@author: gowrishankar.p
"""

import sys
import re,csv

readfile = False
scriptPath = 'D:\gowrishankar.p\Python Script\output.txt'

try:
    read = open('D:\gowrishankar.p\Python Script\input.csv','r')
    readfile = True
except ValueError as e:
    print("Open unsupported file read error: %s") %e
    sys.exit()
    
if readfile == True: 
    reader = csv.reader(read, delimiter=',')
    headers_ = next(reader)
    data_ = list(reader)
    read.close()

prevcalled = []
prevcalled_1 = []
load = []
data = []
temp = []
# multi = []
# bkp = []

def output(load):
    global scriptPath
    # string = ",".join(load)
    # print('Result',string)
    scriptPath = 'D:\gowrishankar.p\Python Script\output.txt'
    with open(scriptPath, "a+") as script:
        string = ",".join(load)
        # data.append(string)
        print('Result',string)
        script.write(string)
        script.write("\n")
        script.close()
        
def call_chain(called,data):
    global load
    global prevcalled
    global prevcalled_1
    global temp
    # global multi
    # global bkp
    
    add = False
    # To store the multi called modules 
    print('called',called)
    # if j not in prevcalled:
    for j in data:
        if called == j[0]:
            temp.append(j[1])
            add = True
    if add == True:
        temp = [called] + temp
        
    # Rest the temp if it's singleton
    if len(temp) <= 2:
        temp=[]

        
    for j in data:
        if called == j[0]:
            if called not in prevcalled:
                print('Sucs  ',j[1])
                print("temp",temp)
                called = j[1]
                load.append(called)
                if len(temp) > 2:
                    if temp[0] == j[0]:
                        for t in temp[2:len(temp)]:
                            if t not in prevcalled_1:
                                print("Temp-0",load,t)
                                # prevcalled_1.append(t)
                                # call_chain(t,data)
                # if len(temp) > 1:
                #     if temp not in multi:
                #         multi.append(temp)
                temp = []
                call_chain(called,data)
                prevcalled.append(j[0])
            else:
                print('skip ',called)
    
    
    if len(load) > 0:
        output(load)
        print("temp-2",temp)
        # strings = ",".join(load)
        # data.append(strings)
        load =[]
        temp = []
        # for m in multi:
        #     for i in m[1:len(m)]:
        #         if i not in bkp and i not in prevcalled:
        #             print('calling from multi',i)
        #             bkp.append(i)
        #             load.append(i)
        #             call_chain(i, data)
        # print(multi)
        # multi = []
        # bkp = []
        # load =[]
        # prevcalled = []
        
    # print(data)
    # return(multi)
        
for i in data_:
    calling = i[0]
    called = i[1]
    if i[0] not in prevcalled:
        print("start ", calling,called)
        load.append(calling)
        load.append(called)
        call_chain(called,data_)
        # multi = call_chain(called,data_)
        # print(multi)
    # break
    

        

    