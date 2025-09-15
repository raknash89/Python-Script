# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:40:14 2022

@author: gowrishankar.p
"""
import os

path = 'D:\gowrishankar.p\Airbus\Inventory/user - Copy'

# files = os.listdir(path)
files = ['TK13PROJ','TK13HTZX','TF13V01','MBBCHKP1']

i = 0
# print(files)
for file in files:
    print('Files=',file)
    # with open(path+'/'+file) as f:
    with open(path+'/'+file+'.cpy') as f:
        lines = f.readlines()
        # lines = lines.rstrip()
        for line in lines:
            if '%INCLUDE' in line and '/*' not in line:
                split = line.strip().split()
                # print(line.strip())
                for each,ind in enumerate(split):
                    if split[each] == '%INCLUDE':
                        calling = split[each+1]
                        calling = calling.replace(';','')
                        
                        print("calling",calling)
                        break
    i = i + 1
    # if i == 10:
    #     break
