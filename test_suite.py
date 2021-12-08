# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 16:27:05 2021

@author: garvi
"""

import requests
import base64
import json

def make_user():
  requestUrl = "https://purde-final-project.appspot.com/user"
  requestBody = {
    "metadata": {
      "Name": "69",
      "Password": "69"
    }
  }
  requestHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }

  request = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
  

def test_auth_none_user():
  requestUrl = "https://purde-final-project.appspot.com/authenticate"
  requestBody = {
    "User": {
      "name": "hey",
      "isAdmin": False
    },
    "Secret": {
      "password": "yes"
    }
  }
  requestHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }

  request = requests.put(requestUrl, headers=requestHeaders, json=requestBody)
  
  assert (request.status_code == 501)
  assert(request.content == b"This system does not support authentication.")
  
  print ("Assertion passed for no user.")


def test_auth_exist_user():
    make_user()
    requestUrl = "https://purde-final-project.appspot.com/authenticate"
    requestBody = {
      "User": {
        "name": "69",
        "isAdmin": False
      },
      "Secret": {
        "password": "69"
      }
    }
    requestHeaders = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
      
    request = requests.put(requestUrl, headers=requestHeaders, json=requestBody)
    
    assert (request.status_code == 501)
    assert(request.content == b"This system does not support authentication.")
    
    print ("Assertion passed for existing user.")


def test_post_package_1():
  requestUrl = "https://purde-final-project.appspot.com/package"
  
  data = open ("react-main.zip", "rb").read()
  encoded = base64.b64encode(data)
  s_encoded = '"' + str(encoded) + '"'
  
  requestBody = {
    "metadata": {
      "Name": "test_post_package_1",
      "Version": "1.2.3",
      "ID": "69"
    },
    "data": {
      "Content": s_encoded,
      "JSProgram": "",
      "URL": ""
    }
  }
  requestHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }

    # This request posts the package.
  _ = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
  
      # This request is a duplicate. to ensure the existing package.
  request_exist = requests.post(requestUrl, headers=requestHeaders, json=requestBody)

  
  print ("\nPost works with existing package.")
  assert(request_exist.status_code == 403)


def test_post_package_2():
  requestUrl = "https://purde-final-project.appspot.com/package"
  
  data = open ("react-main.zip", "rb").read()
  encoded = base64.b64encode(data)
  s_encoded = '"' + str(encoded) + '"'
  
  requestBody = {
    "metadata": {
      "Name": "shrek lol",
      "Version": "1.2.3",
      "ID": "69"
    },
    "data": {
      "Content": s_encoded,
      "JSProgram": "",
      "URL": ""
    }
  }
  requestHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json"
  }

  request = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
 

  print ("\nPost works with new package.")
 # print (request.status_code)
  assert(request.status_code == 201)

def test_post_package_url():
    pass

def test_post_package_user_id():
    print ("Testing custom user ID schema for POST")
    requestUrl = "https://purde-final-project.appspot.com/package"

    data = open ("react-main.zip", "rb").read()
    encoded = base64.b64encode(data)
    s_encoded = '"' + str(encoded) + '"'
    
    requestBody = {
      "metadata": {
        "Name": "shrek23",
        "Version": "1.2.3",
        "ID": "69696969"
      },
      "data": {
        "Content": s_encoded,
        "JSProgram": "",
        "URL": ""
      }
    }
    requestHeaders = {
      "Content-Type": "application/json",
      "Accept": "application/json"
    }
      
    request = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
    print (request.content)
    assert(json.loads(request.content)["ID"] == 69696969)
     

def test_reset():
  requestUrl = "https://purde-final-project.appspot.com/reset"
  requestHeaders = {
    "X-Authorization": "gdsgds",
    "Accept": "application/json"
  }
  
  
  print ("\nTesting reset...")

  request = requests.delete(requestUrl, headers=requestHeaders)

  assert (request.status_code == 200)

if __name__ == "__main__":
  print ("\nRunning Auth tests..")  
  test_auth_none_user()
  test_auth_exist_user()
  
  test_reset()
  
  # post package but first reset so I can actually test shit
  test_post_package_1()
  test_post_package_2()
  
  test_post_package_user_id()
  
  
