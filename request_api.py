# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 19:41:03 2022

@author: gowrishankar.p
"""

import requests,ssl,certifi

def get():
    # api_url = "https://jsonplaceholder.typicode.com/todos/1"
    api_url = "https://www.apartments.com/70-sherwood-st-providence-ri/gw1mknz/"
    ssl._create_default_https_context = ssl._create_unverified_context
    response = requests.get(api_url)
    return(response)
    # result = response.json()
    # status_code = response.status_code
    # char_typ = response.headers["Content-Type"]

    # print(result,status_code,char_typ)


def put():
    api_url = "https://jsonplaceholder.typicode.com/todos"
    todo = {"userId": 1, "title": "testing", "completed": False}
    response = requests.post(api_url, json=todo)
    return(response)

def final(response):
    result = response.json()
    status_code = response.status_code
    char_typ = response.headers["Content-Type"]
    print(result,status_code,char_typ)
    # response.json()
#{'userId': 1, 'title': 'Buy milk', 'completed': False, 'id': 201}

if __name__ == '__main__':
    response = get()
    final(response)
    # response = put()
    # final(response)

#{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}