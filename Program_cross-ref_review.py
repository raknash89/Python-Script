# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 16:02:46 2022

@author: gowrishankar.p
"""

import pandas as pd

cnt = 0
xls = pd.ExcelFile('D:\gowrishankar.p\SEG Reports\SEGReports20221124154209\IMMP reports\Program Cross-ref_Consolidated_v1.xlsx')
df1 = pd.read_excel(xls,'IMMP')
df2 = pd.read_excel(xls,'EA_ pgm vs copy')
df1 = df1.sort_values(by=['Calling','Calling Type'])
df2 = df2.sort_values(by=['Referred by','Referring Object Type'])
pgm_vs_copy = open('D:\gowrishankar.p\SEG Reports\SEGReports20221124154209\pgm_vs_copy_error.txt','w')
# calling,caling_type = df1['Calling'].tolist(),df1['Calling Type'].tolist()
# called,called_type = df1['Called'].tolist(),df1['Called Type'].tolist()
# merge = [calling]
for each_2 in df2.index:
    # calling _EA = df2['Referring Object Type'][each_2]
    calling_ea = df2['Referred by'][each_2]
    calling_type_ea  = df2['Referring Object Type'][each_2]
    called_ea = df2['Object Name'][each_2]
    called_type_ea = df2['Object Type'][each_2]
    
    print('Calling_ea ',calling_ea,called_ea,called_type_ea)
    cnt = cnt + 1
    if cnt == 3:
        break
    match = False
    prev = ''
    pgm_match = False
    for each in df1.index:
        calling = df1['Calling'][each]
        calling_type = df1['Calling Type'][each]
        called = df1['Called'][each]
        called_type = df1['Called Type'][each]
        print('For each',calling,called,called_type)
        if pgm_match == True and prev != calling:
            print('match ',match , 'prev ',prev )
            pgm_match = False
            if match == False:
                print('Copybook not found',calling_ea,'>',called_ea)
                pgm_vs_copy.write('Copybook/Include not found '+calling_ea+' > '+called_ea+'\n')
            break
        
        
        if calling_ea == calling:
            pgm_match = True
            print('TRUE ',calling,called,called_type)
            if called_ea == called and called_type == called_type_ea:
                match = True
                print('SET MATCH')
                break
            if called_ea == called and calling_type == 'Include':
                match = True
                print('SET MATCH INC')
                break
            
        
        prev = calling
        
    

pgm_vs_copy.close()
            
    # break