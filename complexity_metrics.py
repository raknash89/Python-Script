# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:19:14 2022

@author: gowrishankar.p
"""
import pandas as pd
import psycopg2,json,openpyxl
from operator import itemgetter
from statistics import mean, median
# import numpy as np



class database:
    def __init__(self,db_name, schema, user, password, host, port) -> None:
        
            self.db_name = db_name
            self.schema = schema
            self.user = user
            self.password = password
            self.host = host
            self.port = port
            
            self.conn = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port,
            options='-c search_path='+schema)
            self.table1 = '.program'
            self.table2 = '.program_metrics'
            self.table3 = '.program_node_hierarchy'
            self.table4 = '.sql_table_details'
            self.table5 = '.file_definition'
            self.table6 = '.mq_master'
            self.table7 = '.program_node'
            self.table8 = '.condition_node'

            # self.db_version()
            # self.program()
            # self.lloc()
            # self.sub_routine()
            # self.sql_table()
            # self.file_definition()
            # self.mq_master()
            # self.nested_para()
            # self.condparse()
            # self.count_verbs()
            # print(f"Connected to {db_name}.")
            #self.db_version()

    def db_version(self):
        try:
            print('PostgreSQL database version:')
            self.cur = self.conn.cursor()
            self.cur.execute('SELECT version()')
            fetch = self.cur.fetchall()
            self.cur.close()
            # self.printresult(fetch)
            return fetch
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            print("DB Connection Failed.")
            raise e
        
    def program(self):
        try:
            print('Fetching program realted data from program table')
            
            self.cur = self.conn.cursor()
            query = "SELECT id,name,program_type FROM " + self.schema + self.table1 \
                + " WHERE program_type IN ('cobol','pl1','cbl') ORDER BY id"
            self.cur.execute(query)
            
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            # self.printresult(fetch)
            return fetch
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()

    def lloc(self):
        try:
            print("To get the LLOC realted information for each programs")
            
            self.cur = self.conn.cursor()
            query = "SELECT program_id,original_loc,expanded_loc,status,proc_div_cnt,executable_loc " \
                + "FROM "+ self.schema + self.table2 + " WHERE program_id IN " \
                + " (SELECT id FROM " + self.schema + self.table1 + " WHERE program_type IN ('cobol','pl1','cbl') )"
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            # self.printresult(fetch)
            return fetch
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
            
    def sub_routine(self):
        try:
            print("Program cross-reference or sub-module call information")
            
            self.cur = self.conn.cursor()
            # query = "SELECT program_id,node_id,child_node_id,child_type,child_node_name " \
            #     + "FROM "+ self.db_name + self.table3 + " WHERE child_type IN ('D','C') AND program_id IN " \
            #     + " (SELECT id FROM " + self.db_name + self.table1 + " WHERE program_type IN ('cobol','pl1','cbl') )"
            
            # query = "SELECT program_id,count(*) FROM "+ self.db_name + self.table3 + " WHERE child_type IN ('D','C') " \
            query = "SELECT program_id,child_node_id,child_node_name FROM "+ self.schema + self.table3 + " WHERE child_type IN ('C','D') " \
                " AND program_id IN (SELECT id FROM " + self.schema + self.table1 + " WHERE program_type IN ('cobol','pl1','cbl') )" \
                " GROUP BY program_id,child_node_id,child_node_name ORDER BY program_id "
                #" ORDER BY program_id "
                
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            # self.printresult(fetch)
            return fetch
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
    
    def sql_table(self):
        try:
            print("List of tables used in program")
            # print("program_id, Sum of table")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT program_id,count(distinct(table_id)) FROM "+ self.schema + self.table4 + \
                    " GROUP BY program_id ORDER BY program_id "
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            # self.printresult(fetch)
            return fetch
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
    
    def file_definition(self):
        try:
            print("To Get files are used in the programs")
            # print("program_id,count of file_id")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT program_id,count(file_id) FROM "+ self.schema + self.table5 + \
                    " GROUP BY program_id ORDER BY program_id "
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            return fetch
            # self.printresult(fetch)
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()

    def mq_master(self):
        try:
            print("List of MQ's used in program")
            # print("Program_id,count of mq_id")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT program_id,count(mq_id) FROM "+ self.db_name + self.table6 + \
                    " GROUP BY program_id ORDER BY program_id "
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            return fetch
            # self.printresult(fetch)
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()

    def nested_para(self):
        try:
            print("Count of Nested paragraph calls used in program")
            # print("Program_id,node_id,para_name,count of para triggered")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT a.program_id,a.node_id,a.name,count(DISTINCT(b.child_node_id)) FROM " \
                    + self.db_name + self.table7 + " as a INNER JOIN " + self.db_name + self.table3  \
                    + " as b ON a.program_id = b.program_id AND a.node_id = b.node_id AND a.name not like '%DUMMY%' " \
                    + " AND child_type = 'P' " \
                    " GROUP BY a.node_id,a.program_id,a.name ORDER BY a.program_id,a.node_id"
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            return fetch
            # self.printresult(fetch)
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
    
    def condparse(self):
        try:
            print("Count of conditional nodes present in program")
            # print("Program_id,cond type,count of type")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT program_id,type,count(type) FROM " \
                    + self.db_name + self.table8 \
                    + " GROUP BY program_id,type ORDER BY program_id"
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            return fetch
            # self.printresult(fetch)
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
            
    def count_verbs(self):
        try:
            print("Count of VERBS are used in program")
            # print("Program_id,name ,count of type'A'")
            
            self.cur = self.conn.cursor()
            
            query = "SELECT program_id,name,count(type) FROM " \
                    + self.db_name + self.table7 + " WHERE type = 'A' AND name NOT IN " \
                    + "('READ','WRITE','PERFORM','CALL', 'PROCEDURE DIVISION') GROUP BY program_id,name,type ORDER BY program_id"
            self.cur.execute(query)
            fetch = self.cur.fetchall()
            self.cur.close()
            print(" >> ",len(fetch))
            return fetch
            # self.printresult(fetch)
        except psycopg2.DatabaseError as e:
            print("DB Connection Failed.")
            raise e
        finally:
            self.cur.close()
            
    def printresult(self,result):
        
        if len(result) > 0:
            for each in result:
                print(each)
        else:
            print("Result empty")

def process():
        pgm_id,pgm_name,pgm_type = '','',''
        data = []
        header = ["Program_id","Program_name","Program_type","Category","type","weightage", \
                  "Count","Result"]
        data.append(header)
        
        verb_incr = ['ALSO','ALTER','AND','DEPENDING','END-OF-PAGE','ENTRY','EOP',
                     'EXCEPTION','EXIT','GOBACK','IF','INVALID','OR','OVERFLOW',
                     'SIZE','STOP','TIMES','UNTIL','USE','VARYING','WHEN','WHILE',
                     'GOTO', 'GO TO','SEARCH']
        
        for each in program:   
            # Initialize 
            calc = 0
            sub_cnt = 0
            para_cnt = 0
            nes_para_cnt = 0
            res = ''
            
            # Want to change the weightage for each category.. check in db_config.json file
           
            
            # print(each)
            pgm_id = each[0]
            pgm_name = each[1]
            pgm_type = each[2].strip()
            
                     

            for a in lloc:
                
                #LLOC calculation
                if a[0] == each[0]:
                    if a[5] >= 1000:
                        calc = round(a[5]/1000 *lloc_wht,2)
                    res = [pgm_id,pgm_name,pgm_type,"LLOC","Exeuctable Code",lloc_wht,a[5],calc]
                    data.append(res)
                    
            for idx,b in enumerate(sub_routine):
                
                
                if b[0] == each[0]:
                    # print(b)
                    sub_cnt = sub_cnt + 1
                 
                #Calculation
                if len(sub_routine) == idx+1:
                    calc = sub_cnt * sub_wht
                    res = [pgm_id,pgm_name,pgm_type,"Program Cross-ref","Sub Module Call",sub_wht,sub_cnt,calc]
                    data.append(res)

                
            for c in sql_table:
                
                #Calculation
                if c[0] == each[0]:
                    # print(c)
                    calc = c[1] * sql_wht
                    res = [pgm_id,pgm_name,pgm_type,"No.of Tables ","DB2/SQL",sql_wht,c[1],calc]
                    data.append(res)
                    
            for d in file_def:
                
                #Calculation
                if d[0] == each[0]:
                    # print(d)
                    calc = d[1] * file_wht
                    res = [pgm_id,pgm_name,pgm_type,"No.of Files ","VSAM/PS/RPT",file_wht,d[1],calc]
            
            for e in mq:
                
                #Calculation
                if e[0] == each[0]:
                    # print(e)
                    calc = e[1] * mq_wht
                    res = [pgm_id,pgm_name,pgm_type,"No.of MQ ","PUT/GET",mq_wht,e[1],calc]
            
            # for idx,f in enumerate(nested_para):
                
            #     #Calculation
            #     if f[0] == each[0]:
            #         # print(f)
            #         para_cnt = para_cnt + 1
            #         nes_para_cnt = nes_para_cnt + f[3]
                
            #     if len(nested_para) == idx+1:
            #         calc = nes_para_cnt * para_wht
            #         res = [pgm_id,pgm_name,pgm_type,"Paragrah Cross-ref","Nested paragraph calls",para_wht,nes_para_cnt,calc]
            #         data.append(res)
                    
            for g in condparse:
                
                #Calculation
                if g[0] == each[0]:
                    # print(g)
                    
                    if g[1] == 'I':
                        calc = round(g[2] * cond_wht,2)
                        res = [pgm_id,pgm_name,pgm_type,"Condition Statement","If",cond_wht,g[2],calc]
                        data.append(res)
                        
                    elif g[1] == 'E':
                        calc = round(g[2] * cond_wht,2)
                        res = [pgm_id,pgm_name,pgm_type,"Condition Statement","Else",cond_wht,g[2],calc]
                        data.append(res)
                        
                    elif g[1] == 'E':
                        calc = round(g[2] * cond_wht,2)
                        res = [pgm_id,pgm_name,pgm_type,"Condition Statement","Evaluate",cond_wht,g[2],calc]
                        data.append(res)
                        
                    elif g[1] == 'W':
                        calc = round(g[2] * cond_wht,2)
                        res = [pgm_id,pgm_name,pgm_type,"Condition Statement","When",cond_wht,g[2],calc]
                        data.append(res)
                    else:
                        continue
                
            for h in verbs:
                
                # print(h)
                if h[0] == each[0]:
                    if h[1].upper() in verb_incr:
                        calc = round(h[2] * verb_wht,2)
                        res = [pgm_id,pgm_name,pgm_type,"Verb Statement",h[1].capitalize(),verb_wht,h[2],calc]
                        data.append(res)
                
        # print(data)
        # for each in data:
        #     print(each)
        return data     
    
def complexity_metrics(granular_data):
    
    prev_pgm_id = ''
    prev_pgm_name = ''
    prev_pgm_type = ''
    value = 0
    pgm_id = ''
    pgm_name = ''
    pgm_type = ''
    
    metrics = []
    
    metrics.append(['Program_id', 'Program_name', 'Program_type','Complexity_value','SMC'])
   
    # Calculating the Min, Max, Average based on the results
    last_items = set(map(itemgetter(-1), granular_data[1:len(granular_data)]))
    Min,Max = min(last_items),max(last_items)
    Avg = round(mean(last_items),1)
    Med = round((Avg+Max)/2,1)
    
    print('\nvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    print('     SMC Calulcation paramerets set based on overall value!!    ')
    print('     Min = %d : Avg = %d : Median = %d : Max = %d' % (Min, Avg , Med,Max))
    print('     Note: Above value considered dynaimcally based on the data')
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')      
    
    for each in range(1,len(granular_data)):
        # print(each[0])
            pgm_id = granular_data[each][0]
            pgm_name = granular_data[each][1]
            pgm_type = granular_data[each][2].strip()
            
            # value = value + int(each[-1])
            # print(granular_data[each])
            
            if prev_pgm_id != '':
                # print('prev_pgm_id',prev_pgm_id,pgm_id)
                
                if prev_pgm_id == pgm_id:
                    # print(pgm_id,value)
                    value = round(float(value) + float(granular_data[each][-1]),2)
                else:
                    # if value > 0 and value <=200:
                    if value > 0 and value <= Avg:
                        SMC = 'S'
                    # elif value > 200 and value <= 600:
                    elif value > Avg and value <= Med:
                        SMC = 'M'
                    # elif value > 600:
                    elif value > Med:
                        SMC = 'C'
                    else:
                        SMC = '--'
                    # print("Complexity Value >> ",prev_pgm_id,prev_pgm_name,prev_pgm_type,value,SMC)
                    metrics.append([prev_pgm_id,prev_pgm_name,prev_pgm_type,value,SMC])
                    value = 0
                    value = float(granular_data[each][-1])
                
            prev_pgm_id = pgm_id
            prev_pgm_name = pgm_name
            prev_pgm_type = pgm_type
            
    # if value > 0 and value <=200:
    if value > 0 and value <= Avg:
        SMC = 'S'
    # elif value > 200 and value <= 600:
    elif value > Avg and value <= Med:
        SMC = 'M'
    # elif value > 600:
    elif value > Med:
        SMC = 'C'
    else:
        SMC = '--'
                        
    # print("Complexity Value >> ",prev_pgm_id,prev_pgm_name,prev_pgm_type,value)
    metrics.append([prev_pgm_id,prev_pgm_name,prev_pgm_type,value,SMC])
    return metrics

def excel(granular_data,highlevel_data):
    df = pd.DataFrame(highlevel_data)
    df1 = pd.DataFrame(granular_data)
    # print(df1)
    
    pivot = df1.pivot_table(index=[3],
                            columns=1,
                            values=[7],
                            aggfunc='sum',fill_value=0)
    # print(pivot)
    
    # pd.concat([
    # y.append(y.sum().rename((x, 'Total')))
    # for x, y in pivot.groupby(level=0)]).append(pivot.sum().rename(('Result', 'Total')))
    
    # print(pivot)
    
    path = 'D:\gowrishankar.p\Accelerate Task\Cyclometric complexity/Complexity_Metrics_report.xlsx'

    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name='Summary',index=False, header=False)
        df1.to_excel(writer, sheet_name='Detail',index=False, header=False)
        pivot.to_excel(writer, sheet_name='Pivot')
        
        
    
def main():
    try:
        config_file = "db_config.json"
        # config_file = 'db_config_amtrack.json'
        path = 'D:\gowrishankar.p\Accelerate Task\Cyclometric complexity/'
        # with open('D:\gowrishankar.p\Python Script/'+config_file) as json_file:
        global lloc_wht,sub_wht,sql_wht,file_wht,mq_wht,para_wht,cond_wht,verb_wht
                                
        with open(path+config_file) as json_file:
            json_data = json.load(json_file)
            json_file.close()
            #Reading DB Connection parameters
            master_host = json_data['db-config']['master_host']
            master_user = json_data['db-config']['master_user']
            master_pwd = "postgres"
            master_port = json_data['db-config']['master_port']
            master_dbname = json_data['db-config']['master_db_name']
            master_schema_name = json_data['db-config']['master_schema_name']
            master_table = json_data['db-config']['master_table']
            
            #Reading Weightage values
            lloc_wht = float(json_data["weightage"]['lloc_'])
            sub_wht = float(json_data["weightage"]['sub_pgm'])
            sql_wht = float(json_data["weightage"]['sql_'])
            file_wht = float(json_data["weightage"]['file_'])
            mq_wht = float(json_data["weightage"]['mq_'])
            para_wht = float(json_data["weightage"]['para_'])
            cond_wht = float(json_data["weightage"]['cond_'])
            #if_wht = float(json_data["weightage"]['if_'])
            #else_wht = float(json_data["weightage"]['else_'])
            #when_wht = float(json_data["weightage"]['when_'])
            #eval_wht = float(json_data["weightage"]['eval_'])
            verb_wht = float(json_data["weightage"]['verb_'])
            
    except BaseException as e:
        print("File open error %s" %config_file )
    finally:
        connect = database(master_dbname, master_schema_name, master_user, \
                           master_pwd, master_host, master_port)
        
        global program, lloc, sub_routine, sql_table, file_def, mq, nested_para, condparse, \
            verbs
        # version = connect.db_version()
        program = connect.program()
        lloc = connect.lloc()
        sub_routine = connect.sub_routine()
        sql_table = connect.sql_table()
        file_def = connect.file_definition()
        mq = connect.mq_master()
        # nested_para = connect.nested_para()
        condparse = connect.condparse()
        verbs = connect.count_verbs()
        
        granular_data = process()
        highlevel_data = complexity_metrics(granular_data)
        
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Kinldy refer the Summary & Details in the Complexity_Metrics_report.xlsx")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        excel(granular_data,highlevel_data)
        
if __name__ == '__main__':
    main()
       
        