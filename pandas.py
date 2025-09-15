# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 15:51:32 2022

@author: gowrishankar.p
"""

import pandas as pd
import openpyxl

def read_reference_file():
    
    # Read the xlsx file with sorting order
   data_test = pd.read_excel('D:\gowrishankar.p\Python Script\py_input\Program_Chain.xlsx',engine = 'openpyxl')
   df = pd.DataFrame(data_test)
   df_1 = df.sort_values('Program',ascending=True)
   # print(df_1)
   return df_1

# #*** To write the file in sort order with same sheet
# writer =  pd.ExcelWriter('Program_Chain.xlsx')
# df_1.to_excel(writer,sheet_name = 'Program Call Chain_sort',index=False)
# writer.save()

def read_error_file():
    # Read the xlsx error file
    # error_data = pd.read_excel(open('Error.xlsx','rb'))
    error_data = pd.read_excel('D:\gowrishankar.p\Python Script\py_input\Error.xlsx',engine = 'openpyxl')
    ef_1 = pd.DataFrame(error_data)
    ef_1 = ef_1.reset_index()

    return(ef_1)

def sub_process(line_item,call_typ):
    
    if len(line_item.index) > 0:
            count_1 = 1
            for e in line_item.itertuples(index=False):
                error_line = e[2]
                error_msg = e[4].rstrip()
                if count_1 == 1:
                    if call_typ == 'main':
                        data.append([pgm,'',error_line,error_msg])
                    else:
                        data.append([pgm,sub_pgm,error_line,error_msg])
                else:
                        data.append(['','',error_line,error_msg])
                    
                count_1 = count_1 + 1
    return(data)

def process(df_1,ef_1):
    
    global pgm,sub_pgm,data
    data = []
    prev = ''
    for row in df_1.itertuples(index=False):

        pgm = row[0]
        sub_pgm = row[1]
        
        ## ** To skip the second time processing the main program
        if pgm != prev:
            # Main program error/warning validation
            main = ef_1.loc[ef_1['Program Name'].isin([pgm+'.pli',pgm+'.cbl'])]
            call_typ = 'main'
            data = sub_process(main,call_typ)
                
        # Sub program error/warning validation
        sub = ef_1.loc[ef_1['Program Name'].isin([sub_pgm+'.pli',sub_pgm+'.cbl'])]
        if len(sub.index) > 0:
            call_typ = 'sub'
            data = sub_process(sub,call_typ)
        else:
            data.append([pgm,sub_pgm,'','Sucessful Compilation'])
        prev = pgm
    return(data)

def write(data):
    df_2 = pd.DataFrame(data,columns=['Main Program','Sub Program','Error Line','Error/Warning Message'])
    # df_2.style.applymap(lambda x: "background-color: red" if x== 'COMPJCL' else "background-color: white")
    df_2.style.applymap('background-color: yellow',subset=['Error/Warning Message'])
    df_2.to_excel('D:\gowrishankar.p\Python Script\py_output\compilation_result.xlsx',index= False)
    
def main():
    df_1 = read_reference_file()
    ef_1 = read_error_file()
    data = process(df_1,ef_1)
    write(data)

if __name__ == "__main__":
    main()