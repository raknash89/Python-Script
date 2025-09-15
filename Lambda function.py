# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 12:26:40 2022

@author: gowrishankar.p
"""

from operator import itemgetter

lst = [(10, [('Clark', 10, 2450), ('Miller', 10, 1300), ('Alex', 10, 9000)]),
(20, [('Smith', 20, 800), ('Jones', 20, 2975), ('Scott', 20, 3000)]),
(30, [('John', 30, 2850), ('Ward', 30, 1000), ('Kent', 30, 8000), ('James', 30, 2000)])]

ls = [('Data',0,[8, 4, 6],22),('Data',1,[8, 4, 6],22),('check',[8, 4, 6],50)]




#Using itemgetter
for i in lst:
    a = max(i[1], key=itemgetter(2))
    # print(i[0],a)
    
#using lamda fucntion : Max
for i in lst:
    a = max(i[1], key=lambda item:item[2])
    # print(i[0],a)
    
#using lamda fucntion : SORT
for i in lst:
    s = sorted(i[1],key = lambda x:x[2],reverse=True)
    # print(s)
    
#using lamda fucntion : Filter
f = list(filter(lambda x:x[0]=='Data',ls))
print(f)