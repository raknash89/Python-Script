import sys, re, shutil
import os, time
from datetime import datetime  

#Inputs from user
##userName = input("Enter the user name:")
##password = input("Enter the password:")
##url = input("Enter the IP address:")
##certificate = input("Enter the certificate:")
##sourceFilePath = input("Enter the source file path:")
##targetFolderPath = input("Enter the target folder path:")
##logFolderPath = input("Enter the log folder path:")
##scriptPath = input("Enter scriptPath:")

def getStatus(logPath, userName):
    T = 0
    loginSuccess = userName + " is logged on"
    passwordError = "530 PASS command failed"
    ipError = "Timeout detected. (control connection)"
    certificateError = "Peer certificate rejected"
    successStatus = "Script: Exit code: 0"
    result = "Submit job failed"
    success = False
    while (not success and T < 5):
        time.sleep(2)
        file = open(logPath, 'r')
        print(logPath)
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


userName = 'G176281'
password = 'newpass3'
url = '10.123.79.234'
certificate = '0f:e3:7c:9b:c8:45:54:c5:cc:63:82:21:ae:25:32:ad:73:40:20:54'
# sourceFilePath = r'D:\gowrishankar.p\JCL\UNLOAD3'
sourceFilePath = r'D:\gowrishankar.p\Python Script\jcl'
targetFolderPath = 'G176281.FTP.JCLLIB.UNLOAD'
logFolderPath = 'D:\gowrishankar.p\Python Script\log'
scriptPath = 'D:\gowrishankar.p\SubmitJobScript.txt'

print( ' user: ', userName,'\n','password: ',password,'\n','url: ',url,'\n','sourceFilePath: ',sourceFilePath,'\n','targetFolderPath: ',targetFolderPath,'\n','logFolderPath: ',logFolderPath,'\n','scriptPath: ',scriptPath,'\n')


transferStatus = ""
# sourceFolder = os.path.dirname(sourceFilePath)
# # sourceFile = os.path.basename(sourceFilePath)
sourceFile = os.listdir(sourceFilePath)
# sourceFolder, separator, file = sourceFile.partition(".")
#arr = os.listdir(sourceFilePath)
#sourceFile = 'XXXXX1.txt'
#print('sourceFile : ',sourceFile.replace(".txt",""))
print('file ',sourceFile)
ftpCommand = "open ftpes://" + userName + ":" + password + "@" + url + "/"
if certificate != None and not certificate.isspace() and len(certificate) != 0:
    ftpCommand = ftpCommand + ' -certificate="' + certificate + '"'

if scriptPath == None or scriptPath.isspace() or len(scriptPath) == 0 or scriptPath.lower() == "na":
    scriptPath = "D:\gowrishankar.p\SubmitJobScript.txt"
elif not os.path.isdir(os.path.dirname(scriptPath)):
##    scriptPath = "C:\Users\soundharya.murugan\Python FTP\SubmitJobScript.txt"
    scriptPath = "D:\gowrishankar.p\SubmitJobScript.txt"

# Generate WinSCP script file
with open(scriptPath, "w") as script:
    script.write(ftpCommand)
    script.write("\n")
    # Transfer file from remote to local
    # script.write('lcd "{}"\n'.format(sourceFolder))
    script.write('lcd "{}"\n'.format(sourceFilePath))
    # if targetFolderPath != None and len(targetFolderPath) != 0 and targetFolderPath.lower() != "na":
    #     if not targetFolderPath.endswith("."):
            # targetFolderPath = targetFolderPath + "."
          # print("targetFolderPath : ",targetFolderPath)
    script.write("cd '{}'\n".format(targetFolderPath))
    # script.write("call site filetype=jes JESJOBNAME=*\n")
    loop = 0
    for mem in sourceFile:
        if loop == 0:
            script.write('put -transfer=ascii "{}"\n'.format(mem))
        else:
            script.write("call site filetype=jes JESJOBNAME=*\n")
            script.write('put -transfer=ascii "{}"\n'.format(mem))
        loop = loop+1
    # mem = 'PNTDBHIS'
    # script.write('put -transfer=ascii "{}"\n'.format(mem))
    script.write("call site filetype=jes JESJOBNAME=*\n")
    script.write("exit")

# Getting Current Date & time to create Log file
now = datetime.now()
today = now.strftime("%m-%d-%Y-%H-%M-%S")
logFilePath = logFolderPath + "\\SubmitJobUsingFtp_" + str(today) + ".log"
logPath = os.path.abspath(logFilePath)
print("log path : ",logPath)
command = '"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /log="{}" /ini=nul /script="{}"'.format(logPath, scriptPath)
# logger.info(command)
# Executing the WinSCP script
winscp = os.popen(command)

winscp.close()

getStatus(logPath, userName)

