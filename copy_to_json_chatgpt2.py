# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 22:32:58 2023

@author: gowrishankar.p
"""

from pycobol import CobolCopybook

copybook_path = 'D:\gowrishankar.p\Python Script\py_input\cobol_layout.txt'

with open(copybook_path,'r') as f:
    copybook_content = f.read()
    
cobol_copybook = CobolCopybook(copybook_content)


def cobol_field_to_dict(field):
    
    return{
        'name': field.name,
        'level':field.level,
        'pic': field.pic,
        'usage': field.usage,
        'occurs': field.occurs,
        'children':[cobol_field_to_dict(child) for child in field.children]
        }

json_structure = cobol_field_to_dict(cobol_copybook.root)

import json

json_output_path = 'D:\gowrishankar.p\Python Script\py_output\output.json'
with open(json_output_path,'w') as j:
    json.dump(json_structure,j,index=2)
    
