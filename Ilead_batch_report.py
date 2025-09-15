# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 17:14:47 2022

@author: gowrishankar.p
"""
import json,os,psycopg2
import pandas as pd

class database:
    def __init__(self):
        try:
            # print(os.getcwd())
            config_file = 'db_config_report.json'
            with open(config_file) as json_file:
                json_data = json.load(json_file)
                json_file.close()
            # print(json_data)
            #Reading DB Connection parameters
            self.host = json_data['db_conn']['master_host']
            self.user = json_data['db_conn']['master_user']
            self.pwd = json_data['db_conn']['master_password']
            self.port = json_data['db_conn']['master_port']
            self.dbname = json_data['db_conn']['master_db_name']
            self.schema_name = json_data['db_conn']['master_schema_name']
            # self.table = json_data['db_conn']['master_table']
            
            self.input_path = json_data['path_']['query_excel']
            self.sheet_name = json_data['path_']['sheet_name']
            self.output_path = json_data['path_']['output']
            
            print("Configuration parameters passed :\n",self.host,self.user,self.pwd,self.port,\
                  self.dbname,self.schema_name,"\n")
            self.db_connect()
            self.read_input_excel()
            
        except BaseException as e:
            print("File open error %s" %os.getcwd()+"-> "+ config_file )
    
    def db_connect(self):
        try:
            self.conn = psycopg2.connect(
            database=self.dbname,
            user=self.user,
            password=self.pwd,
            host=self.host,
            port=self.port,
            options='-c search_path='+self.schema_name)
            print("DB Connection sucessfull !!")
        except psycopg2.DatabaseError as e:
            print("DB connection error",e)
            raise e
    
    def read_input_excel(self):
        try:
            df = pd.read_excel(self.input_path, sheet_name=self.sheet_name,\
                               keep_default_na=False)
            df = df.replace('nan','')
            
            # self.pandas_list = self.excel_data_df.tolist()
            # print(df)
            for idx,i in  df.iterrows():
                self.report_name = i[1]
                self.header = i[4].split(',')
                if i[2] != '':
                    self.query = i[2].replace('SCHEMAXX',self.schema_name)
                    result = self.db_run()
                    result.insert(0,self.header)
                    self.writecsv(result)
                else:
                    print("*** Warning *** \nEmpty Query for the report '%s'\n"\
                          %self.report_name.upper())
                    
                
                
            
        except BaseException as e:
            print("Input query excel open error %s" %self.input_path )

    def db_run(self):
        try:
            print('Running the "%s" query in PostgreSQL table'%self.report_name.upper())
            self.cur = self.conn.cursor()
            self.cur.execute(self.query)
            fetch = self.cur.fetchall()
            self.cur.close()
            # self.printresult(fetch)
            print("No of rows extracted ",len(fetch))
            return fetch
            
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            print("   >> Query exectuon failed for the report%s"%self.report_name)
            raise e
        finally:
            self.cur.close()
            print("   >> Query executed sucessfully\n")
            
    def writecsv(self,result):
        try:
            df1 = pd.DataFrame(result)
            # print(len(df1.index()))
            df1.to_csv(self.output_path+"/"+self.report_name+".csv",sep=',',encoding='utf-8',\
                   header=None,columns=None,index=None)
        except BaseException as e:
            print("Error writing into csv '%s'" %self.report_name.upper() )
    # def printresult(self,result):
        
    #     if len(result) > 0:
    #         for each in result:
    #             print(each)
    #     else:
    #         print("Result empty")
            
if __name__ == '__main__':
    # config()
    connect = database()
    # connect.db_connect()
    # connect.read_query()