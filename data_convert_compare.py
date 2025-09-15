# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:01:13 2022

@author: gowrishankar.p
"""

import ebcdic,binascii,os
import codecs,difflib
from datetime import datetime

mf_folder_path = 'D:/gowrishankar.p/Python Script/mf_input/'
mfes_folder_path = 'D:/gowrishankar.p/Python Script/mfes_input/'

mf_convert_path = 'mf_convert'
mfes_convert_path  = 'mfes_convert'
mf_compare = 'Data_compare'
space = '                   '

# diff_out = 'D:/gowrishankar.p/Python Script/'

def curr():
    now = datetime.now()
    return(now.strftime("%m-%d-%Y-%H-%M-%S"))

def folder():
    # Check whether the specified path exists or not
    # print(os.getcwd())
    folder_name = [mf_convert_path,mfes_convert_path,mf_compare]
    for folder in folder_name:
        isExist = os.path.exists(folder)
        
        if not isExist:
          os.makedirs(folder)
          print("The new directory is created! ",folder)

          
def readfile(ls):
    # global mfread, mfesread
    
    for file in ls:
        # print('>>>> File ',file,'\n')
        print(space,'>> File MF  :' , file)
        with open(mf_folder_path + file,'rb') as f:
            mfread = f.readlines()
            f.close()
        
        ## >> Data conversion 
        convert(mfread,file,'MF')
    
        mfes_file = file.replace('MF.','MFES.')
        try:
            print(space,'>> File MFES:' , mfes_file)
            with open(mfes_folder_path + mfes_file,'rb') as f:
                mfesread = f.readlines()
                f.close()
                
                ## >> Data conversion 
                convert(mfesread,mfes_file,'MFES')
        
        except IOError:
            print('File not found in MFES folder ',mfes_file)
       
def convert(data,filename,path):    
    get = curr()
    if path == 'MF':
        pdsout=codecs.open(mf_convert_path+'/'+filename,"w+","utf-8")
    else:
        pdsout=codecs.open(mfes_convert_path+'/'+filename,"w+","utf-8")
        
    for line in data:
        # bread_lines=codecs.decode(line.rstrip(), encoding="IBM037")
        bread_lines=codecs.decode(line, encoding="IBM037")
        pdsout.write(bread_lines)
    pdsout.close()
    
def compare(ls):
    
    for file in ls:
        
        fromfile = file
        tofile = file.replace('MF.','MFES.')
        
        with open(mf_convert_path+'/'+fromfile) as f:
            fromlines = f.readlines()
            f.close()
    
        with open(mfes_convert_path+'/'+tofile) as f:
            tolines = f.readlines()
            f.close()
            
        # repfile = "D:\gowrishankar.p\Python Script\ebcidout.txt"+".html"
        repfile = mf_compare + '/' + file+'.html'
        
        diff_html = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile, tofile)
        s = difflib.SequenceMatcher(None, fromlines, tolines)
        
        with open(repfile, "a") as f:
            f.write(diff_html)
            f.close()
        
def main():
    
    get = curr()
    ## Create folder for output
    print(get,'>> Folder creation')
    folder()
    
    ## >> Read files from the path 
    ls = os.listdir(mf_folder_path)
    get = curr()
    print(get,'>> Read & convert the file')
    readfile(ls)
    
    ## >> Compare the converted files
    get = curr()
    print(get,'>> Compare the files')
    compare(ls)
    
    
    
if __name__ == "__main__":
    main()