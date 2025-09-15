# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 12:09:08 2022

@author: gowrishankar.p
"""

import win32com.client as client

outlook = client.Dispatch("Outlook.Application")
message = outlook.CreateItem(0)
message.Display()
message.To = "gowrishankar.p@infosys.com"
message.CC = "raknash.shankar@gmail.com"
#message.BCC = "raknash.shankar@gmail.com"
message.Subject = "Hello World"
message.Body = "Hi mail sent through python script, did you receive it ?"
#message.SentOnBehalfOfName = "gowrishankar.p@infosys.com"
message.Send()