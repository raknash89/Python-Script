# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 10:27:35 2022

@author: gowrishankar.p
"""
import ebcdic,binascii,os
import codecs,difflib

# ascii_path = 'D:\gowrishankar.p\Python Script\TEST.DATA.CON.ASCII.txt'
bin_path = 'D:\gowrishankar.p\Python Script\Inp_script\BFTP.TEST.DATA2.EBCID.txt'
wr = 'D:\gowrishankar.p\Python Script'

fromfile =  'D:\gowrishankar.p\Python Script\Inp_script\BFTP.TEST.DATA.EBCID.txt'
tofile =  'D:\gowrishankar.p\Python Script\Inp_script\BFTP.TEST.DATA2.EBCID.txt'
#fromfile = 'D:/gowrishankar.p/Python Script/BFTP.TEST.DATA.EBCID.txt.DAT'
#tofile = 'D:/gowrishankar.p/Python Script/BFTP.TEST.DATA2.EBCID.txt.DAT'

## *** Binary converson method       ****     ##
# def string2bits(s=''):
#     return [bin(ord(x))[2:].zfill(8) for x in s]

# def bits2string(b=None):
#     return ''.join([chr(int(x, 2)) for x in b])

# Support decode : 'cp1140','cp500' , 'cp037' , 'cp273' ,
# support encode : 'cp1252','latin1',' cp875 ' 

en_code = ['cp1252','latin1',' cp875 ']
de_code = ['cp1140','cp500' , 'cp037' , 'cp273' ]

##  Option using ebcdic package  ##
def option1(bread):
    for lines in bread:
        # import ebcdic,binascii,codecs
        for i in en_code:
            print('encode ',i,"\n")
            # print(bread.encode('cp1252'))
            # print(bread.encode('cp1252'))
            latinread = lines.encode(i,errors='ignore')
            print(latinread,'\n')
            for j in de_code:
                print('decode ',j,"\n")
                dcode = latinread.decode(j,errors='ignore')
                print(dcode)
        # for each in bread:
        #     print(each)
    
##  Option using Codecs package  ##
def option2(bread,fname):
    arr = []
    print(arr)
    for lines in bread:
        print('Before : ',lines)
        bread_lines=codecs.decode(lines.rstrip(), encoding="IBM037")
        print('After : ',bread_lines)
        arr.append(bread_lines)
        pdsout=codecs.open(wr+'/'+fname+'.DAT',"w+","utf-8")
        pdsout.write(bread_lines)
        pdsout.close()
        
        # print(arr)
    return arr
        
        
def comp():
    
    # with open(fromfile,'rb') as f:
    #     fromline = f.readlines()
    #     fname = (os.path.basename(fromfile))
    #     # print('Before ',fromline)
    #     fromlines = option2(fromline,fname)
    #     f.close()
    #     # print('After ',fromlines)
        
    # with open(tofile,'rb') as f:
    #     toline = f.readlines()
    #     fname = (os.path.basename(tofile))
    #     tolines = option2(toline,fname)
    #     f.close()
    
    with open(fromfile) as f:
        fromlines = f.readlines()
        f.close()
    
    with open(tofile) as f:
        tolines = f.readlines()
        f.close()
        
    repfile = "D:\gowrishankar.p\Python Script\ebcidout.txt"+".html"
    
    diff_html = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile, tofile)
    s = difflib.SequenceMatcher(None, fromlines, tolines)
    # print(s)
    with open(repfile, "a") as f:
        f.write(diff_html)
        f.close()
        
def main():

    ## *** EBCDIC to ASCII Conversion    ****    ##
    # aopen = open(ascii_path,'rb')
    # aread = aopen.read()
    # aopen.close()
    # print(aread,'\n')
    
    # bopen = open(bin_path,'rb')
    # bread = bopen.readlines()
    # bopen.close()
    
    # option1(bread)
    # option2(bread)
    comp()
    # print(bread,'\n')

if __name__ == "__main__":
    main()