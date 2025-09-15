import sys, getopt
import os
from datetime import datetime

mfid = 'G176281'
pwd = 'newpass'
ip = '10.123.79.234'
#certificate = '0f:e3:7c:9b:c8:45:54:c5:cc:63:82:21:ae:25:32:ad:73:40:20:54'
#sourceFilePath = 'D:\gowrishankar.p\JCL\XXXXX1'
#targetFolderPath = 'G176281.FTP.JCLLIB'
#logFolderPath = 'D:\gowrishankar.p'
#scriptPath = 'D:\gowrishankar.p\SubmitJobScript.txt'
# mf_file = 'G176281.FTP.JCLLIB.NEW'
mf_file = 'G176281.SPUNCH.D220622.TBL1.DAT'
mf_cd = 'D:\gowrishankar.p\DB2 to SQL Migrator tool\dataset'
# mf_cd = 'D:\gowrishankar.p\JCL'

#def main(mfid,pwd,ip,mf_cd,mf_file): 
print('argv:',mfid,pwd,ip,mf_file)
command='open ftpes://'+str(mfid)+':'+str(pwd)+'@'+str(ip)+'/ -certificate="0f:e3:7c:9b:c8:45:54:c5:cc:63:82:21:ae:25:32:ad:73:40:20:54"'
#Getting Current Date & time to create Log file
now = datetime.now()
today = now.strftime("%m-%d-%Y-%H-%M-%S")
logname="GET"+"@"+str(today)+".log"

#Generating the WinSCP script file
#with open("C:\\Users\\hamsappriya.vadivel\\PythonFTP\\script1.txt", "w") as textlog:
with open("D:\gowrishankar.p\script1.txt", "w") as textlog:
    textlog.write(command)
    textlog.write("\n")
    #textlog.write("lcd C:\\Users\\hamsappriya.vadivel\\PythonFTP")
    textlog.write("lcd D:\gowrishankar.p\JCL")
    textlog.write("\n")
    textlog.write("cd '"+str(mf_cd)+".'")
    textlog.write("\n")
    textlog.write("get -transfer=ascii "+str(mf_file)+"")
    # textlog.write("get -transfer=ascii XDC.TEST")
    textlog.write("\n")
    textlog.write("ls")
    textlog.write("\n")
    textlog.write("exit")
    #cmd2='"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /log="C:\\Users\\hamsappriya.vadivel\\PythonFTP\\'+logname+'" /ini=nul /script="C:\\Users\\hamsappriya.vadivel\\PythonFTP\\script1.txt"'
    cmd2='"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /log="D:\gowrishankar.p\JCL'+logname+'" /ini=nul /script="D:\gowrishankar.p\script1.txt"'
    #Executing the WinSCP script
    os.popen(cmd2)
    #return mf_file

