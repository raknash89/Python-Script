# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 17:35:43 2022

@author: gowrishankar.p
"""

import csv,os
import requests
import xml.etree.ElementTree as ET

def parseXML(xmlfile):
  
    # create element tree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
    # root = ET.fromstring(country_data_as_string)
    # print(len(root.tag))
    data = root.split("<")
  
    # iterate news items
    # # for item in root.findall('Field name'):
    # for child in root:
    #     if 'oap/envelope' in 'oap/en
        # print(child.tag, child.attrib)
        # for child1 in child:
        #     print(child1.tag,child1.attrib)
        #     for child2 in child1:
        #         print(child2.tag,child2.attrib)
  
  
      
    # # return news items list
    # return newsitems

# with open('D:\gowrishankar.p\sample_dump\manifestid.xml', 'r') as f:

#     a = f.readline()
# print(os.getcwd())
path = 'D:\gowrishankar.p\sample_dump'
os.chdir(path)
print(os.getcwd())
# with open('test.xml', 'r') as f:
#     a = f.readlines()

# print(a)
# parseXML('test.xml')
parseXML('manifestid.xml')
        

  