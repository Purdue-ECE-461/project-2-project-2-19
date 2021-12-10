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
  s_encoded = str(encoded)[2:]
  
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

  print (request_exist.content)
  print (request_exist.status_code)
  print ("\nPost works with existing package.")
  assert(request_exist.status_code == 403)


def test_post_package_2():
  requestUrl = "https://purde-final-project.appspot.com/package"
  
  data = open ("react-main.zip", "rb").read()
  encoded = base64.b64encode(data)
  s_encoded = str(encoded)[2:]
  
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
  print (request.content)
  print (request.status_code)
 # print (request.status_code)
  assert(request.status_code == 201)

def test_post_package_url():
    pass

def test_post_package_user_id():
    print ("Testing custom user ID schema for POST")
    requestUrl = "https://purde-final-project.appspot.com/package"

    data = open ("react-main.zip", "rb").read()
    encoded = base64.b64encode(data)
    s_encoded = str(encoded)[2:]
    
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
  
  
def test_get_package_false():
  requestUrl = "https://purde-final-project.appspot.com/package/1"
  print ("GET a package that doesnt exist...")
  requestHeaders = {
    "X-Authorization": "",
    "Accept": "application/json"
  }

  request = requests.get(requestUrl, headers=requestHeaders)

  assert (request.status_code == 400)
  
def test_get_package_true():
  requestUrl = "https://purde-final-project.appspot.com/package/69696969"
  print ("GET a package that exists..")
  requestHeaders = {
    "X-Authorization": "gsg",
    "Accept": "application/json"
  }

  request = requests.get(requestUrl, headers=requestHeaders)

  assert (request.status_code == 200)    



def test_package_delete_false():
    print ("Testing delete on false project...")
    requestUrl = "https://purde-final-project.appspot.com/package/66"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.delete(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 400)
    

def test_package_delete_true():
    print ("Testing delete on true project...")
    requestUrl = "https://purde-final-project.appspot.com/package/69"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.delete(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 200)
    

def test_get_by_name_false():
    print ("Get by name false package")
    requestUrl = "https://purde-final-project.appspot.com/package/byName/something fake"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.get(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 400)
    
def test_get_by_name_true():
    print ("Get by name real package")
    requestUrl = "https://purde-final-project.appspot.com/package/byName/shrek%20lol"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.get(requestUrl, headers=requestHeaders)

    assert (request.status_code == 200)
    assert (json.loads(request.content)[0]["name"] == "shrek lol")
    

def test_put_no_package():
      data = open ("express-master.zip", "rb").read()
      print ("Testing update on package that doesnt exist")
      encoded = base64.b64encode(data)
      s_encoded = str(encoded)[2:]
        
      requestUrl = "https://purde-final-project.appspot.com/package/1"
      requestBody = {
        "metadata": {
          "Name": 255,
          "Version": 9,
          "ID": 699010020520535
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
    
      request = requests.put(requestUrl, headers=requestHeaders, json=requestBody)
      
      assert (request.status_code == 400)

def test_put_yes_package():
      data = open ("express-master.zip", "rb").read()
      print ("Testing update on package that does exist")
      encoded = base64.b64encode(data)
      s_encoded = str(encoded)[2:]
        
      requestUrl = "https://purde-final-project.appspot.com/package/1"
      requestBody = {
        "metadata": {
          "Name": 255,
          "Version": 9,
          "ID": 69696969
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
    
      request = requests.put(requestUrl, headers=requestHeaders, json=requestBody)
      
      assert (request.status_code == 200)
    

def test_get_by_name_more_versions():
    print ("\n Testing get by name by adding a new version for a package")
    requestUrl = "https://purde-final-project.appspot.com/package"
    
    data = open ("react-main.zip", "rb").read()
    encoded = base64.b64encode(data)
    s_encoded = str(encoded)[2:]
    
    requestBody = {
      "metadata": {
        "Name": "shrek lol",
        "Version": "1.2.4",
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
    
    _ = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
    requestUrl = "https://purde-final-project.appspot.com/package/byName/shrek%20lol"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.get(requestUrl, headers=requestHeaders)

    assert (request.status_code == 200)
    print (request.content)
    

def test_delete_by_name_false():
    print ("Delete by name false package")
    requestUrl = "https://purde-final-project.appspot.com/package/byName/something fake"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.delete(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 400)


def test_delete_by_name_true_all_versions():
    print ("Delete by name all version for this package")
    requestUrl = "https://purde-final-project.appspot.com/package/byName/shrek%20lol"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.delete(requestUrl, headers=requestHeaders)

    assert (request.status_code == 200)

def test_delete_by_name_singular():
    print ("Delete by name real package")
    requestUrl = "https://purde-final-project.appspot.com/package/byName/shrek23"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.delete(requestUrl, headers=requestHeaders)

    assert (request.status_code == 200)
    
    
def get_pages_empty():
    print ("\n Testing empty pages..")
    requestUrl = "https://purde-final-project.appspot.com/packages"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.post(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 200)
    assert (["No such page exists"] == json.loads(request.content))


def post_random_packages(number):
    requestUrl = "https://purde-final-project.appspot.com/package"
    
    data = open ("react-main.zip", "rb").read()
    encoded = base64.b64encode(data)
    s_encoded = str(encoded)[2:]
    
    s_num = str(number)
    
    requestBody = {
      "metadata": {
        "Name": s_num,
        "Version": s_num,
        "ID": number
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
    
    r = requests.post(requestUrl, headers=requestHeaders, json=requestBody)
    return r.status_code
    
def get_some_pages():
    print ("\n Testing full pages... [Adding 2 random packages]")

    post_random_packages("1")
    post_random_packages("2")

    requestUrl = "https://purde-final-project.appspot.com/packages"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.post(requestUrl, headers=requestHeaders)
    
    assert (request.status_code == 200)
    assert (["No such page exists"] != json.loads(request.content))


def get_some_pages_with_offset():
    print ("\n Testing offset... first adding 15 random projects.")
    for i in range(0, 19):
        print ("\n\t@ Package {}".format(i))
        post_random_packages(str(i + 3))
    
    requestUrl = "https://purde-final-project.appspot.com/packages?offset=2"
    requestHeaders = {
      "Accept": "application/json"
    }
    
    request = requests.post(requestUrl, headers=requestHeaders)
    a = json.loads(request.content)
    
    requestUrl = "https://purde-final-project.appspot.com/packages?offset=1"
    
    request_2 = requests.post(requestUrl, headers=requestHeaders)
    
    b = json.loads(request_2.content)

    assert (a != b)


def test_ece_461_failed_1():
    print ("\n Testing ECE-461 failed case 1")
    r = post_random_packages("underscore")     
    assert (r == 201)


if __name__ == "__main__":
  test_ece_461_failed_1()
    
  print ("\nRunning Auth tests..")  
  test_auth_none_user()
  test_auth_exist_user()
  
  test_reset()
  test_reset()
  test_reset()
  
  # post package but first reset so I can actually test shit
  test_post_package_1()
  test_post_package_2()
  
  test_post_package_user_id()
  
  test_get_package_false()
  test_get_package_true()
  
  
  test_package_delete_false()
  test_package_delete_true()
  
  
  test_put_no_package()
  test_put_yes_package()
  
    # GET /package/byName/{name}
  test_get_by_name_false()
  test_get_by_name_true()
  test_get_by_name_more_versions()
  
      #DELETE /package/byName/{name}
  test_delete_by_name_false()
  test_delete_by_name_true_all_versions()
  test_delete_by_name_singular()
  
      #POST /packages
  get_pages_empty()
  get_some_pages()
  get_some_pages_with_offset()
  
  test_ece_461_failed_1()
