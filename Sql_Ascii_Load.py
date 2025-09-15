# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:27:34 2022

@author: gowrishankar.p
"""
import psycopg2,csv


def main():
    # query = 'Select * from process_fix.testing'
    # source_file = open("D:\gowrishankar.p\Python Script\Inp_script\sql_ascii.csv","r",\
                       # encoding='utf8')
    with open("D:\gowrishankar.p\Python Script\Inp_script\sql_ascii.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print(row)
    
    query = '''COPY process_fix.testing (id,name) FROM 'D:\gowrishankar.p\Python Script\Inp_script\sql_ascii.csv'
                DELIMITER ',' CSV HEADER ENCODING 'SQL_ASCII';'''
    try:
            conn = psycopg2.connect(
            database='process_fix',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432,
            options='-c search_path='+'process_fix')
            # print(f"Connected to {db_name}.")
            
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            # db_data = cur.fetchall()
            # return db_data
            # print(db_data)
    except UnicodeError:
            cur.rollback()
            print("unicode error")
            #logging.error(f'{query} - Query throws error')
            #logging.error('Unicode error raised loading Program Source Table ',exc_info=True)
    except psycopg2.DatabaseError as e:
        # logger.error('DB Connection Failed.')
        print("DB Connection Failed.")
        raise e
    finally:
        cur.close()
        print('sucessfully')

if __name__ == '__main__':
    main()
