# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:01:10 2022

@author: gowrishankar.p
"""
import shutil

class copy_:
    
    def __init__(self) -> None:
        # self.from_path = 'D:\gowrishankar.p\IMMP-ILead\Amtrack_inventory/user - Copy/'
        self.from_path = 'D:\gowrishankar.p\sample_dump\AMTRAK20221028155013\Source\Source/MISC/'
        self.to_path = 'D:\gowrishankar.p\IMMP-ILead\Amtrackfew_inventory/user - Copy/'
        self.file_list = 'D:\gowrishankar.p\IMMP-ILead\Amtrackfew_inventory/List.txt'
        self.ext_list = ['.cpy','.CPY','.cbl','.CBL','']
        
        self.read_list()
        self.copy_dest()
        
    def read_list(self):
        with open(self.file_list,'r') as f:
            self.line = f.readlines()
    
    def copy_dest(self):
        for i in self.line:   
            copied = False
            for ext in self.ext_list:
                try:
                    print(self.from_path+i.strip()+ext)
                    shutil.copy(self.from_path+i.strip()+ext,self.to_path)
                    copied = True
                    break
                except:
                    try:
                        shutil.copy(self.from_path+i.strip(),self.to_path)
                        copied = True
                        break
                    except:
                        copied = False
            
            if copied == False:
                print('copy failed %s'%i.strip())

def main():
    a = copy_()
    # data = 'a'
    #a.__inti__()
    
if __name__ == '__main__':
    main()
    

