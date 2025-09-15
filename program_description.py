# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 19:13:23 2022

@author: gowrishankar.p
"""

import os

path = 'D:\gowrishankar.p\sample_dump\Sample'
sourceFile = os.listdir(path)
content_start = 'DESCRIPTION'
content_start1    ='PROGRAM OVERVIEW'
content_start2  = 'MODULE NAME    '
zero = 0
commented = '*'
i = 0

# w = open(path + '\getfilelist.bat','w')
global lastarr

for file in sourceFile:
    filename = os.path.join(path, file)
    # if (file == 'ILICBCRT.cbl'):
    print(file)
        # w.write(file+'\n')
    with open(filename) as f:
        read = f.readlines()
        # print(read)
        start, end = False, False
        # if file == 'PT432.cbl':
        lastarr = (str(read.pop()))
            
        for idx,line in enumerate(read):
            
            i = i + 1
            if not start:
                if (line.find(content_start) >= zero) | (line.find(content_start1) >= zero) \
                    | (line.find(content_start2) >= zero):
                    start = True

            if start == True:
                # if file == 'ILICBCRT.cbl':
                print(line[7:71])
                    # w.write(line[7:71]+'\n')
                # print(read[idx+1][8:17])
                # if ((read[idx+1].find('    -----') == zero) | (read[idx+1][8:17] == '         ')) \
                if (read[idx+1][8:17] != '         ') | (read[idx+1].find('  --') == zero):
                    #| (read[idx+1].find('PROGRAM CALLED') >= zero):

                # if read[idx+1].find('PROGRAM CALLED') != zero:
                    # if file == 'ILICBCRT.cbl':
                    print(read[idx+1][8:17])
                        
                # if (read[idx+1][8:17] != '         '):
                    end = True
            if end:
                break

# w.close()
            # if i == 5:
            #     break

    # break
        
