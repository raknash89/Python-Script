import os
#import ftplib
import ssl
#from ftplib import FTP
from ftplib import FTP_TLS
from getpass import getpass
import time
import subprocess
import request
from requests.auth import HTTPDigestAuth
import json


global USER
global PASS
global SERVER
global PORT
USER = 'g176281'
PASS = 'newpass2'
SERVER = '10.123.79.234'
PORT = 21

def ftp():
    try:
        print("server ->",SERVER, "port -->",PORT,"++ use -> ",USER,"++ pass->",PASS)
        ftp = FTP()
        ftp.connect('10.123.79.234')
        resp = (ftp.login(user=USER,passwd=PASS)).split(' ')[0]
        if resp == '230':
            connect_success = True
        ftp.quit()
    except ftplib.all_errors as e:
        print ('Error -->',e)
        print ('Error {}'.format(e.args[0][:3]))
        print("Error in FTP Connection ,Check Configuration ")
    except :
        print ("Some exception in FTP Connection ,wrong configuration ")
        close = input("Enter any key to Terminate ..")
        
def ftp_tls():
    try:
        print("TLS server ->",SERVER,"++ use -> ",USER,"++ pass->",PASS)
        print(ssl.OPENSSL_VERSION)
        ftp = FTP_TLS()
        ftp.connect(SERVER)
       # ftp.auth()
        #resp = (ftp.login(user=USER,passwd=PASS)).split(' ')[0]
        resp = ftp.login()
        ftp.prot_p()
        if resp == '230':
            connect_success = True
        ftp.quit()
    except ftplib.all_errors as e:
        print ('Error -->',e)
        print ('Error {}'.format(e.args[0][:3]))
        print("Error in FTP Connection ,Check Configuration ")
    except :
        print ("Some exception in FTP Connection ,wrong configuration ")
        close = input("Enter any key to Terminate ..")

def get_server_cert(hostname, port):
    conn = ssl.create_connection((hostname, port))
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sock = context.wrap_socket(conn, server_hostname=hostname)
    cert = sock.getpeercert(True)
    cert = ssl.DER_cert_to_PEM_cert(cert)
    return cerft

def api():

    # Replace with the correct URL
    url = "10.123.79.234"

    # It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
    myResponse = requests.get(url,auth=HTTPDigestAuth(raw_input("g176281"), raw_input("newpass2")), verify=True)
    #print (myResponse.status_code)

    # For successful API call, response code will be 200 (OK)
    if(myResponse.ok):

        # Loading the response data into a dict variable
        # json.loads takes in only binary or string variables so using content to fetch binary content
        # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
        jData = json.loads(myResponse.content)

        print("The response contains {0} properties".format(len(jData)))
        print("\n")
        for key in jData:
            print(key + " : " + jData[key])
    else:
      # If response code is not ok (200), print the resulting http error code with description
        myResponse.raise_for_status()
    
ftp()
#ftp_tls()
# api()

#resp = get_server_cert(SERVER, PORT)

