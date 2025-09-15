import os, time
import csv
#import array as arr
from getpass import getpass
#import sys, re, shutil
from datetime import datetime


global CURDIR
CURDIR = os.getcwd()


def get_def_configuration():
## READS CONFIG FILE TO CREATE A CONFIG DICTIONARY 
#    CURDIR = os.getcwd()
    conf  = "CONFIG.txt"
    global configd
    configd = {}
    proc_ok = False 
    try:
      config = open (conf,'r')
      proc_ok = True 
    except:
        print ("Confguration file CONFIG.txt is missing !! ")
        xc = input ("Enter any key to continue .....")
    if proc_ok:
        for line in config:
            keys,val = line.strip().split('<=>',1)
            configd.update(dict.fromkeys(keys.split('<=>'),val))
        config.close()
    return (configd)

def get_configuration():
## DEFAULT SETTING ARE SAVED ON A CONFIGURATION FILE .
## THIS SUBROUTINE IS TRIGGERED INITIALLY TO GET THE CONFIGURATION INFORMATION FROM
## FROM THE USER. THIS IS SAVED ON CONFIG FILE     
    configd = {}
#    CURDIR  = os.getcwd()
    conf  = "CONFIG.txt"
##    MFUSRID  = input ("Enter your Mainframe id : ").upper()
##    configd['MFUSRID'] =  MFUSRID

    JCLLIB = input ("Enter the local directory where you wish to save the JCLs:")
    if JCLLIB == '':
        JCLLIB = "JCLLIB"
    configd['JCLLIB'] = JCLLIB
    
    MFFTPIN  = input ("Enter the mainframe PDS where you want to FTP the Unload JCLS:").upper()
    configd['MFFTPIN']  = MFFTPIN
    if MFFTPIN == '':
        print("Error occur while executing FTP SEND")
        

    JCLLIB = input ("Enter the local directory where you wish to save the JCLs:")
    if JCLLIB == '':
        JCLLIB = "JCLLIB"
    configd['JCLLIB'] = JCLLIB
    
    MFFTPIN  = input ("Enter the mainframe PDS where you want to FTP the Unload JCLS:").upper()
    configd['MFFTPIN']  = MFFTPIN
    if MFFTPIN == '':
        print("Error occur while executing FTP SEND")

    GETLIB = input ("Enter the local directory where you wish to recieve the mainframe file:")
    if GETLIB == '':
        GETLIB = "GET"
    configd['GETLIB'] = GETLIB
    
        
    configd['VER']    = time.strftime("%m%d")
    configd['OPT']    = 'FL'
    configd['MAKERUN'] = 'YES'

    configd['SERVER'] = input ("Enter the Mainframe FTP Server Name:")
    configd['USER']   = input ("Enter the Mainframe Login ID :")
    password = getpass("Enter the password")
    configd['PASS']     = password
    configd['CERTI']   = input ("Enter the Winscp certificate No :")
    configd['LOG']   = input ("Enter the Log folder path :")

    update_configuration(configd)

    print ("Configuration complete, all entered information updated in %s , you may review and change the same if needed "  % conf )

def update_configuration(configd):
## UPDATES THE CONFIG FILE 
#    CURDIR = os.getcwd()
    #conf = CURDIR+"\\CONFIG.txt"
    conf = "CONFIG.txt"
    with open(conf,"w") as config:
        for key,value in configd.items():
            config.write('%s<=>%s\n' %(key,value))

def do_ftp(opt):
## FTPS THE JCL FILES CREATED TO MAINFRAME.
    SERVER = ' '
    USER  = ' '
    PASS = ' '
#    err = ' '
#    skel = ''
    MFSEND = ''

    configd = {}
    do_ask = False 
    configd = get_def_configuration()
    if opt == 'L':
        try:
            JCLLIB = configd['JCLLIB']
            do_ask = True
        except:
            JCLLIB =  print ("Enter the local Unload JCL Directory:")
            configd['JCLLIB'] = JCLLIB
            do_ask  = False 
        if do_ask:
            do_ask = False 
            chg = input ("The unload JCLs will be picked from %s ,Enter Y if you wish to change:" % JCLLIB).upper()
            if chg == 'Y':
                JCLLIB =  print ("Enter the local Unload JCL Directory:")
                configd['JCLLIB'] = JCLLIB
        try:
            MFFTPIN = configd['MFFTPIN']
            do_ask = True 
        except:
            MFFTPIN  = input ("Enter the Mainframe Directory you wish to FTP the JCLs:")
            configd['MFFTPIN'] = MFFTPIN 
            do_ask = False 
        if do_ask:
            chg = input ("The default FTP directory is set to % s ,enter Y to change:" % MFFTPIN)
            if chg == 'Y':
                MFFTPIN  = input ("Enter the Mainframe Directory you wish to FTP the JCLs:")
                configd['MFFTPIN'] = MFFTPIN

    if opt == 'G':
        try:
            GETLIB = configd['GETLIB']
            do_ask = True
        except:
            GETLIB =  print ("Enter the local directory where you wish to recieve the mainframe file::")
            configd['GETLIB'] = GETLIB
            do_ask  = False 
        if do_ask:
            do_ask = False 
            chg = input ("The MF files will be recieved to %s ,Enter Y if you wish to change:" % GETLIB).upper()
            if chg == 'Y':
                GETLIB =  print ("Enter the local directory where you wish to recieve the mainframe file::")
                configd['GETLIB'] = GETLIB
            
    if chg == 'Y':        
        update_configuration(configd)

    CERTI = configd['CERTI']
    USER = configd['USER']
    PASS = configd['PASS']
    LOG = configd['LOG']
    SERVER = configd['SERVER']
    GETLIB = configd['GETLIB']
##    SERVER , USER ,PASS = configure_ftp()

##  Re-direct from FTPLIB connect to WINSCP Connect    
    ftpCommand = "open ftpes://" + USER + ":" + PASS + "@" + SERVER + "/"
    if CERTI != None and not CERTI.isspace() and len(CERTI) != 0:
        ftpCommand = ftpCommand + ' -certificate="' + CERTI + '"'

    scriptPath = "SubmitJobScriptDB2.txt"
    
    with open(scriptPath, "w") as script:
        script.write(ftpCommand)
        script.write("\n")
        # Transfer file from local to remote
        if opt == 'T':
            Folder = os.listdir(JCLLIB)
            script.write('lcd "{}"\n'.format(JCLLIB))
            script.write("cd '{}'\n".format(MFFTPIN))
            for Member in Folder:
                script.write('put -transfer=ascii "{}"\n'.format(Member))
        # Recieve file from remote to local
        if opt == 'G':
            script.write('lcd "{}"\n'.format(GETLIB))
            MFSEND =  input("Enter the local directory where you wish to recieve the mainframe file:")
            configd['MFSEND'] = MFSEND
            sourceFolder, separator, sourceFile = MFSEND.partition(".")
            script.write("cd '{}'\n".format(sourceFolder))
            script.write('get -transfer=ascii "{}"\n'.format(sourceFile))
        script.write("exit")

    # Getting Current Date & time to create Log file
    now = datetime.now()
    today = now.strftime("%m-%d-%Y-%H-%M-%S")
    logFilePath = LOG + "\\SubmitJobUsingFtp_" + str(today) + ".log"
    logPath = os.path.abspath(logFilePath)
    print("log path: ", logPath)
    command = '"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /log="{}" /ini=nul /script="{}"'.format(logPath, scriptPath)
    # Executing the WinSCP script
    winscp = os.popen(command)
    winscp.close()

    transferStatus = getStatus(logPath, USER)
    print(transferStatus)
    
def getStatus(logPath, USER):
    T = 0
    loginSuccess = USER + " is logged on"
    passwordError = "530 PASS command failed"
    ipError = "Timeout detected. (control connection)"
    certificateError = "Peer certificate rejected"
    successStatus = "Script: Exit code: 0"
    result = "Submit job failed"
    success = False
    while (not success and T < 5):
        time.sleep(2)
        #print(logPath)
        #file = open(logPath, 'r')
        file = open(logPath, 'r')
        content = file.readlines()
        for line in content:
            if loginSuccess in line:
                result = "Login Successful"
            elif passwordError in line:
                result = "Incorrect MFID/Password"
            elif ipError in line:
                result = "Incorrect IP address"
            elif certificateError in line:
                result = "Certificate authentication error"
            elif successStatus in line:
                result = "Submit job successfull"
                success = True
        T += 1
    return result


######################################################## Added above #################

## To Process the Unload file
def processUnload(table,job,skeleton):
    global count
    global getload

#    start = "//"
    load=[]
    getload=[]
    count = 0
    step = 0
    idx = ''
    # ADD INX NUMBER 
    for idx, line in enumerate(skeleton):      
        if line[:10] == "//JOBNAMEX":
            job_name = "//" + job[0]
            line1 = job_name + line[10:]
            load.append(line1)
        elif 6 < idx < 10:
            # LOOP THE TABLE FOR SAME BATCH
            for tab in table:
                if len(tab) >= 9:
                    tab = tab[0:8]
                    
                # ADD DD NAME INCERMENTAL
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".UNLOAD,"
                    getload.append(configd['USER'] + ".DB." + tab + ".UNLOAD")
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SYSPUNCH,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                
##                    
        elif 11 <= idx <=28:
            if idx == 28:
                # LOOP THE TABLE FOR SAME BATCH
                for tab in table:
                    tablename = tab
                    if len(tab) >= 9:
                        tab = tab[0:8]
                    # REPEAT THE UNLOAD STEPS FOR GIVEN TABLE
                    for z, linex in enumerate(skeleton,start=11):
                        #print("line: ",skeleton[z])
                        if z == 28:
                            break
                        if ("//SYSREC   DD DSN=XXXXXX," in skeleton[z]):
                           # print("sysrec : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".UNLOAD,"
                            load.append(linex)
                        elif ("UNLOAD FROM TABLE DB.TABLE" in skeleton[z]):
                            #linex = skeleton[z].replace("DB.TABLE",tab)
                            linex = skeleton[z].replace("DB.TABLE",tablename)
                            #print("syspun : ", linex)
                            load.append(linex)
                        elif ("//SYSPUNCH DD DSN=XXXXXX," in skeleton[z]):
                           # print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSPUNCH,"
                            load.append(linex)
                        elif ("//STEPD" in skeleton[z]):
                            step = step + 1
                            linex = skeleton[z].replace("//STEPD","//STEPD"+str(step))
                            load.append(linex)
                        else:
                            load.append(skeleton[z])
        else:
            load.append(line)
               
    return(load)

## To Process the Load file Inprogress
def processLoad(table,job,skeleton):
    global count

 #   start = "//"
    load=[]
    count = 0
    idx = ''
    step = 0
    # ADD INX NUMBER 
    for idx, line in enumerate(skeleton):
        #print( " line: ", line,idx)
        if line[:10] == "//JOBNAMEX":
            job_name = "//" + job[0]
            line1 = job_name + line[10:]
            load.append(line1)
        elif 6 < idx < 10:
            #print(skeleton[idx])
            # LOOP THE TABLE FOR SAME BATCH
            for tab in table:
                if len(tab) >= 9:
                    tab = tab[0:8]            
                # ADD DD NAME INCERMENTAL
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SYSUT1,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SORTOUT,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SYSDISC,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SYSERR,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
                if("//DD    DD DSN=XXXXXX," in line):
                    count = count+1
                    inc = "//DD" + str(count)
                    line1 = line.replace("//DD",inc)
                    pos = line1.find("XXXXXX")
                    line1 = line1[:pos] + configd['USER'] + ".DB." + tab + ".SYSMAP,"
                    load.append(line1)
                    load.append(skeleton[idx+1])
                    load.append(skeleton[idx+2])
        elif 11 <= idx <=49:
            #print(skeleton[idx])
            if idx == 49:
                # LOOP THE TABLE FOR SAME BATCH
                for tab in table:
                    if len(tab) >= 9:
                        tab = tab[0:8]
                    # REPEAT THE UNLOAD STEPS FOR GIVEN TABLE
                    for z, linex in enumerate(skeleton,start=11):
                        #print("line inside: ",skeleton[z])
                        if z == 49:
                            break
                        if ("//SYSREC  DD DSN=XXXXXX," in skeleton[z]):
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".UNLOAD,"
                            load.append(linex)
                        elif ("//SYSUT1  DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSUT1,"
                            load.append(linex)
                        elif ("//SORTOUT DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SORTOUT,"
                            load.append(linex)
                        elif ("//SYSDISC DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSDISC,"
                            load.append(linex)
                        elif ("//SYSERR  DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSERR,"
                            load.append(linex)
                        elif ("//SYSMAP  DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSMAP,"
                            load.append(linex)
                        elif ("//SYSIN   DD DSN=XXXXXX," in skeleton[z]):
                            #print("syspun : ", skeleton[z])
                            pos = skeleton[z].find("XXXXXX")
                            linex = skeleton[z][:pos] + configd['USER'] + ".DB." + tab + ".SYSPUNCH,"
                            load.append(linex)
                        elif ("LOAD DB2 TABLE XXXXXXX" in skeleton[z]):
                            linex = skeleton[z].replace("XXXXXXX",tab)
                            load.append(linex)
                        elif ("//STEPD" in skeleton[z]):
                            step = step + 1
                            linex = skeleton[z].replace("//STEPD","//STEPD"+str(step))
                            load.append(linex)
                        else:
                            load.append(skeleton[z])
        else:
            load.append(line)
            
    return(load)


# WRTIE INTO THE OUTPUT FILES
def write(job,load,opt):
    global incrU
    global incrL

    if opt == 'U':
        incrU = incrU+1
        for k in getload:
            #print("write file get : ",configd['GETLIB']+"/recive")
            wr = open(configd['GETLIB']+"/recive", "a")
            wr.write(k+'\n')

    elif opt == 'L':
        incrL = incrL+1

    for l in load:
        if opt == 'U':
            if (len(job[0]) <= 7):
                jobname = job[0] + "U"
            else:
                jobname = job[0].replace(job[0][-1],"U")
        if opt == 'L':
            if (len(job[0]) <= 7):
                jobname = job[0] + "L"
            else:
                jobname = job[0].replace(job[0][-1],"L")
                
        #w = open("JCL/"+ jobname, "a")
        #print("write file name : ",configd['JCLLIB'])
        w = open(configd['JCLLIB']+"/"+ jobname, "a")
        w.write(l+'\n')
        #print(l)

# JCL SKELETON FOR UNLAOD READ
def JCLUNLOAD():
    with open("UNLOAD Skeleton.txt", "r") as f:
        data = f.read().splitlines(False)
        f.close()
        return data

# JCL SKELETON FOR LOAD READ
def JCLLOAD():
    with open("LOAD Skeleton.txt", "r") as f:
        data = f.read().splitlines(False)
        f.close()
        return data
    

# INPUT INVENTORY READ    
def Inventory(skeleton,opt):
    global data1
    with open("Inventory.csv", "r") as b:
        reader = csv.reader(b, delimiter=',')
        headers = next(reader)
        data1 = list(reader)
        #print(headers)
        b.close()

        #LOCAL VARIABLE INITIZ
        prevjob =""
        prev =""
        current = ""
        i = 0

        for k in data1:
            # SAME BATCH ACCUMULATION
            if k[3] == prevjob:
                table.append(k[0])
                job.append(k[3])
                #print(table)
                current = i+1
            else:
                # FIRST REC SKIP
                if prev == current:
                    table=[]
                    job=[]
                    table.append(k[0])
                    job.append(k[3])
                    #print("if",table,job)
                else:
                    if opt == 'U':
                        load = processUnload(table,job,skeleton)
                    if opt == 'L':
                        load = processLoad(table,job,skeleton)
                    #WRITE COMPLETE BATCH FINISH
                    write(job,load,opt)
                    table=[]
                    job=[]
                    table.append(k[0])
                    job.append(k[3])
                    #print("else",table,job)
                prev = i
                
            prevjob = k[3]
            
        # LAST BATCH INVENTORY RUN
        if opt == 'U':
            load = processUnload(table,job,skeleton)
            write(job,load,opt)
        if opt == 'L':
            load = processLoad(table,job,skeleton)
            write(job,load,opt)
def main():
    global opt
    cont = True
    quit = False
    print ("********************************************") 
    print ("** Welcome to DB2 Data Transfer Workbench **")
    print ("********************************************")

    configd = {}
    configd = get_def_configuration()

     
    validOPT = ['U','T','G','L']

    if not configd:
        print (" Before Starting its recommended to configure the defaults values ")
        cfg  = input (" Enter Y if you wish to configure now :").upper()
        if cfg == 'Y':
            get_configuration()
             
    while (cont):
        
        print ("-------------------------------------------")
        print ("***** IMS DB Migrator Function List *******")
        print ("-------------------------------------------")
        print ("To Create Unload Jcls                 :  U ")
        print ("To Create Load Jcls                   :  L ")
        print ("To TRASNFER JCL submit using FTP      :  T ")
        print ("To GET files from Mainframe to local  :  G ")
        opt = input ("Enter one of the options from above: ").upper()
        if opt in validOPT:
            if opt == 'U':
               skeleton = JCLUNLOAD()
               Inventory(skeleton,opt)
               print("Number of Unload JCl's created is", incrU)
            elif opt == 'T':
                do_ftp(opt)
            elif opt == 'L':
                skeleton = JCLLOAD()
                Inventory(skeleton,opt)
                print("Number of LOAD JCl's created is", incrL)
            elif opt == 'G':
                do_ftp(opt)
            inp = input ("Processing Complete ... Do you wish to do any other operation Y/N:" ).upper()
            if inp == 'Y':
                cont = True
            else:
                sys.exit()
                cont = False
        else:
            print ("Invalid Option Provided, please use one listed:")
            cont = True
                


incrL = 0
incrU = 0
main()

