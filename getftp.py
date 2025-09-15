import sys, re, shutil
import os, time
from datetime import datetime

# userName = input("Enter the user name:")
# password = input("Enter the password:")
# url = input("Enter the IP address:")
# certificate = input("Enter the certificate:")
# sourceFilePath = input("Enter the source file path:")
# targetFolderPath = input("Enter the target folder path:")
# logFolderPath = input("Enter the log folder path:")
# scriptPath = input("Enter scriptPath:")

userName = 'G176281'
password = 'newpass1'
url = '10.123.79.234'
certificate = '0f:e3:7c:9b:c8:45:54:c5:cc:63:82:21:ae:25:32:ad:73:40:20:54'
#sourceFilePath = 'G176281.FTP.JCLLIB'
# sourceFilePath ='G176281.DB.BANKTAB.UNLOAD'
# sourceFilePath = 'G176281.COBOL.LIST.DCOMMINS'
sourceFilePath = 'G176281.TEST.DATA2.ASCII'
# targetFolderPath = 'D:\gowrishankar.p\GET'
targetFolderPath = 'D:\gowrishankar.p\Python Script\Inp_script'
logFolderPath = 'D:\gowrishankar.p'
scriptPath = 'D:\gowrishankar.p\SubmitJobScript.txt'


sourceFolder, separator, sourceFile = sourceFilePath.partition(".")
print(sourceFilePath)
print(sourceFolder)
print(sourceFile)
transferStatus = ""

ftpCommand = "open ftpes://" + userName + ":" + password + "@" + url + "/"
if certificate != None and not certificate.isspace() and len(certificate) != 0:
    ftpCommand = ftpCommand + ' -certificate="' + certificate + '"'
        
# Generate WinSCP script file
with open(scriptPath, "w") as script:
    script.write(ftpCommand)
    script.write("\n")
    # Transfer file from remote to local
    script.write('lcd "{}"\n'.format(targetFolderPath))
    script.write("cd '{}.'\n".format(sourceFolder))
    script.write('get -transfer=binary "{}"\n'.format(sourceFile))
    # script.write('get -transfer=binary "{}"\n'.format(sourceFile))
    #script.write('get "{}"\n'.format(sourceFile))
    script.write("exit")

# Getting Current Date & time to create Log file
now = datetime.now()
today = now.strftime("%m-%d-%Y-%H-%M-%S")
logFilePath = logFolderPath + "\\GetFileUsingFtp_" + str(today) + ".log"
logPath = os.path.abspath(logFilePath)
command = '"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /log="{}" /ini=nul /script="{}"'.format(logPath,scriptPath)
# Executing the WinSCP script
winscp = os.popen(command)
# Wait for process to complete
winscp.close()
# Read transfer status from logfile
#transferStatus = getStatus(logPath, userName)
transferStatus = "Get file successfull"
if transferStatus == "Get file successfull":
    # Rename output file to .txt
    print(sourceFile)
    print(targetFolderPath)
    targetFile = os.path.abspath(targetFolderPath + "\\" + sourceFile)
    textFile = targetFile + ".txt"
    os.replace(targetFile, textFile)
print(transferStatus)
print(logFilePath)
print(targetFile)

def getStatus(logPath, userName):
    T = 0
    loginSuccess = userName + " is logged on"
    passwordError = "530 PASS command failed"
    ipError = "Timeout detected. (control connection)"
    certificateError = "Peer certificate rejected"
    successStatus = "Script: Exit code: 0"
    result = "Get file failed"
    success = False
    while (not success and T < 5):
        time.sleep(2)
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
                result = "Get file successfull"
                success = True
        T += 1
    return result
