# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:22:59 2021

@author: garvi
"""

#File imports
from Project2 import app
from Project2 import util
from Project2 import macros

#Library imports
import os
from flask import render_template, flash, request
from google.cloud import storage

@app.route("/")
@app.route("/home")
def homepage():
    if (macros.first_load == True):
        flash('Welcome back!')
        macros.first_load = False
    return render_template("index.html", title="NPM-Registry Group 19")

@app.route("/docs")
def docs():
    return render_template("index.html", title="docs page")

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    '''
    Code borrowed from google-docs.
        https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage
    '''
    if request.method == 'POST':
                
        f = request.files['file']
        
        if not f:
            return 'No file uploaded.', 400
        
        name = request.form.get('name')
        
        if not name:
            return 'No Name mentioned', 400
        
        version = request.form.get("version")
        
        if not version:
            return 'No Version mentioned', 400
        
        
        # Lazy-load the libraries.
        import requests
        from requests.structures import CaseInsensitiveDict
        import base64
        
        data = f.read()
        encoded_data = base64.b64encode(data)
        
        url = "http://localhost:5000/package"
        
        headers = CaseInsensitiveDict()
        headers["X_Authorization"] = "fdsfdsfds"
        headers["Content-Type"] = "application/json"
        
        s_name = '"' + name + '"'
        s_version = '"' + version + '"'
        s_content = '"' + str(encoded_data) + '"'
        
        data = """
        {
          "data": {
            "Content": %s,
            "JSProgram": "JSProgram",
            "URL": "URL"
          },
          "metadata": {
            "ID": "ID",
            "Name": %s,
            "Version": %s
          }
        }
        """ % (s_content, s_name, s_version)
                        
        resp = requests.post(url, headers=headers, data=data)
        
        print(resp.status_code)
        
        if (resp.status_code == 200):
            flash("File added to the Cloud.")
        
    return render_template("index.html", title="docs page")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/view")
def view():
    import requests

    headers = {
        'X_Authorization': 'fsafsa',
    }
    
    params = (
        ('offset', '1'),
    )
    
    response = requests.post('http://localhost:5000/packages', headers=headers, params=params)
    
    names_array = []
    id_array = []
    size_array = []
    
    for item in response.json():
        names_array.append(item['name'].partition(':')[0])
        id_array.append(item['id'])
        size_array.append(item['size'])
        
    return render_template("view.html", result=zip(names_array, id_array, size_array))

if __name__ == "__main__":
    app.run(debug=True)
