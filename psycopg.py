# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 18:15:30 2022

@author: gowrishankar.p
"""
import traceback
import psycopg2, json

f = open('readme.txt', 'w')

def __create_connection(db_name, schema, user, password, host, port,query_str) -> None:
    try:
            conn = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port,
            options='-c search_path='+schema)
            # print(f"Connected to {db_name}.")
            
            cur = conn.cursor()
            # print('PostgreSQL database version:')
            # cur.execute('SELECT version()')

            cur.execute(query_str)
            
            db_version = cur.fetchall()
        
            cur.close()
            
            return db_version
    except psycopg2.DatabaseError as e:
        # logger.error('DB Connection Failed.')
        print("DB Connection Failed.")
        raise e

def file_list(dataset_name):
    global i , tab
    tab = '\t'
    i = 0
    # To get list of rows for the files
    query_str = "select * from database86.jcl_dsn_hierarchy where dataset_name \
        ='%s'"% dataset_name
    # print(query_str)
    conn_1 = __create_connection(master_dbname, master_schema_name, master_user, \
                           master_pwd, master_host, master_port,query_str)
    for each1 in  conn_1:
        # id_ = each1[0]
        jcl_id = each1[1]
        # node_id = each1[2]
        step_map = each1[3]
        # dataset_name1 = each1[6]
        # recfm = each1[8]
        disp = each1[7].strip()
        
        if disp == 'OLD' or disp == 'SHR':
            print('Level-1 ',tab,jcl_id,step_map,disp)
            i = i +1
            tab = tab*i
            # f.write("-----------------------------------------\n")
            f.write(tab + str(jcl_id) + step_map  + disp + '\n')
            # f.write("-----------------------------------------\n")
            call_chain(each1,dataset_name)
                        
def call_chain(each1,dataset_name):
    global i, tab
    jcl_id = each1[1]
    # node_id = each1[2]
    step_map = each1[3]
    
    query_str = "select * from database86.jcl_dsn_hierarchy where jcl_id \
        ='%s'"% jcl_id + "and step_map = '%s'"%step_map
     
    conn_2 = __create_connection(master_dbname, master_schema_name, master_user, \
                    master_pwd, master_host, master_port,query_str)
        
    for each2 in conn_2:
        if each2[6] != dataset_name:
            if each2[7].rstrip() == 'NEW':
                # i = i + 1
                tab = tab+tab
                print('level-2',tab,each2[6])
                f.write(tab + str(each2[6]) +'\n')
                # i = i + 1
                tab = tab+tab
                print(tab,each2[1],each2[3],each2[7])
                f.write(tab + str(each2[1]) + each2[3] + each2[7] +"\n")

                file_list(each2[6])
    
                
def main():
    global master_host,master_user,master_pwd,master_port,master_dbname
    global master_schema_name,master_table
    try:
        with open('D:\gowrishankar.p\Python Script\py_input/db_config.json') as json_file:
            json_data = json.load(json_file)
            master_host = json_data['master_host']
            master_user = json_data['master_user']
            #master_pwd = "kSs@2807"
            master_pwd = "postgres"
            master_port = json_data['master_port']
            master_dbname = json_data['master_db_name']
            master_schema_name = json_data['master_schema_name']
            master_table = json_data['master_table']
            
            # To find the list of duplicate file entries
            query_str = "select dataset_name, count(dataset_name) from database86.jcl_dsn_hierarchy \
                group by dataset_name having count(dataset_name) > 1 order by dataset_name"
                
            conn = __create_connection(master_dbname, master_schema_name, master_user, \
                                       master_pwd, master_host, master_port,query_str)
                
            # query_show = "SHOW search_path"
            
            # conn2 = __create_connection(master_dbname, master_schema_name, master_user, \
            #                            master_pwd, master_host, master_port,query_show)
                
            # print(conn2)
            
            for each in conn:
                print("\nfile : ",each[0],"\n")
                dataset_name = each[0]
                f.write(each[0] + "\n")
                # f.write("\n")
                # f.write("-----------------------------------------\n")
                file_list(dataset_name)
                f.write("-----------------------------------------\n")
   
            
    except (psycopg2.Error, IOError) as e:
        traceback.print_exc()
        
    f.close()
if __name__ == '__main__':
    main()

