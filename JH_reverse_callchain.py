import pandas as pd
import json
import numpy as np

def read_input_csv(input_csv,crossref_csv):
    
    try:
        df = pd.read_csv(input_csv)
        df1 = pd.read_csv(crossref_csv)
        
        #Initialize 
        df['Calling'] =         df['Calling'].str.strip().str.upper()
        df['Calling_type']  =   df['Calling_type'].str.strip().str.upper()
        df['Application']   =   df['Application'].str.strip().str.upper()
        df['Application'] =     df['Application'].fillna('')
        df1['Referred by']  =       df1['Referred by'].str.strip().str.upper()
        df1['Referring Object Type'] =   df1['Referring Object Type'].str.strip().str.upper()
        df1['Referred by App name'] =   df1['Referred by App name'].str.strip().str.upper()
        df1['Object Name']   =       df1['Object Name'].str.strip().str.upper()
        df1['Object Type'] =    df1['Object Type'].str.strip().str.upper()
        df1['Ref Object App Name'] =    df1['Ref Object App Name'].str.strip().str.upper()
        
        return df,df1
    except BaseException as e:
        print("File open error %s" %input_csv )


def write(data_final,output_path):
    # print(data_final)
    filename = output_path + "/reverse_call_chain.xlsx"
    df_2 = pd.DataFrame(data_final,columns=['Level-1','Level-2','Level-3','Level-4','Level-5'])
    # Pandas Color background
    df_2 = df_2.style.applymap(lambda x:'background-color: %s' % 'yellow' if x in ("['FLXDXP61', 'SHARED', 'ASSEMBLER']",'XX') else '')
    
    # (lambda v: 'background-color: %s' % 'yellow' if v in ('TESTJCL.JCL','TESTCOP3.COPYBOOK') else ''))
    df_2.to_excel(filename,engine='openpyxl')
    
def loop(called,called_app,called_type):
    
    #DataFrame Filter
    val = df1[(df1['Object Name'] == called) &  (df1['Ref Object App Name'] == called_app)]
    # val = df1[(df1['Object Name'] == called)]
    
    count = 0
    
    # print('val',val)
    for idx,row in val.iterrows():
        # print('Level-',level,row['Called'],row['Called_type'],application)
        calling = row['Referred by']
        calling_type = row['Referring Object Type']
        calling_app = row['Referred by App name']
        # print('Level',calling,calling_app,calling_type)
        key_ = [calling,calling_app]
        find = list(filter(lambda x: x[:2] ==key_[:2] , data_temp))

        if len(find) == 0:
            count += 1

            data_temp.append([calling,calling_app,calling_type])
            # print('second',data_temp)
            loop(calling,calling_app,calling_type)
            
    if count == 0 and (data_temp not in data_final):
        data_final.append(data_temp.copy())
        # print("data_final",data_final)
    data_temp.pop()

def main():
    try:
        global df, df1,data_temp,data_final
        data_temp = []
        data_final = []
        config_file = "D:\gowrishankar.p\Python Script\Inp_script\JH_Config.json"
        
        with open(config_file) as json_file:
            json_data = json.load(json_file)
            json_file.close()
        
            input_csv = json_data['starting-module']
            crossref_csv = json_data['cross-ref']
            output_path= json_data['output-path']
            
        df,df1 = read_input_csv(input_csv,crossref_csv)
        # print(df,df1)
        for idx,row in df.iterrows():
            called = row['Calling']
            called_type = row['Calling_type']
            called_app = row['Application']
            print(called,called_type,called_app)
            # key = [calling,calling_type,application]
            key = [called,called_app]
            find = list(filter(lambda x: x[:2] ==key[:2] , data_temp))
            # print('find',find)
            if len(find) == 0:
                data_temp.append([called,called_app,called_type])
                # print('first',data_temp)
                # print('loop')
                loop(called,called_app,called_type)

        write(data_final,output_path)
            
        
        # print(df,df1)
    except BaseException as e:
        print("Process error %s" %e )
    finally:
        print("process completed kindly refer the ouput %s" %output_path)
        
        
if __name__ == '__main__':
    main()