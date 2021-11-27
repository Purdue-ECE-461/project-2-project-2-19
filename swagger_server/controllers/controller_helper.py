# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 00:59:53 2021

@author: garvi
"""

# Library imports
import zipfile
import base64
import os
import glob
import json
from flask_sqlalchemy import SQLAlchemy
from google.cloud import storage


# Package imports
from Project2 import util
from Project2 import macros
from Project2 import app

flask_app = app.app
db = SQLAlchemy(flask_app)

def child_dirs(path):
     cd = os.getcwd()        
     os.chdir(path)          
     dirs = glob.glob("*/")  
     os.chdir(cd)            
     return dirs

def get_package_json(temp_location_of_zip):
    with zipfile.ZipFile(temp_location_of_zip, 'r') as f:
        f.extractall('unzipped')    
    
    repo_name = child_dirs('unzipped')[0]
    
    print(repo_name)
    
    f = open('unzipped/' + repo_name + '/package.json', 'r')
    
    data = json.load(f)['repository']
    print(data)
    f.close()
    
    import shutil
    shutil.rmtree('unzipped')


# User ORM for SQLAlchemy
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    version = db.Column(db.String(50), nullable = False, unique = True)


def add_project_db(name, vs):
    project = Projects.query.filter(version == vs).first()

    # This project is new.
    if not project:
        try:
            project = Projects(
                        name = name,
                        version = version
                )
            db.session.add(project)
            db.session.commit()
            return 200
        except:
            return 404
    else:
        return 403

    # it should not get here
    return -1

#https://stackoverflow.com/questions/54747460/how-to-decode-an-encoded-zipfile-using-python
def convert_and_upload_zip(byteStream, name, version, uid):
    '''
    Params
        byteStream: the base64 encoded zip file.
                
    1. Check the name, version.
            If new, assign a UID in the SQL database.
            If not, delete the query.
    2. Find the metrics, upload to another SQL db with the UID.
    3. Delete all breadtrails upload to the bucket and make it available for download in bucket.
    '''
    
    
    response_code = add_project_db(name, version)
    
    if (response_code != 200):
        return -1
    
    temp_location = 'output_file.zip'

    with open(temp_location, 'wb') as f:
        f.write(base64.b64decode(byteStream))
            
    #Verify the auth works.
    util.implicit()
    
    if not f:
        return 'No file uploaded.', 400

    gcs = storage.Client()
    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)


    # Create a new blob and upload the file's content.
    blob = bucket.blob('tmp_file.zip')

    blob.upload_from_filename(temp_location)

    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    print(blob.public_url)
    
    # Get the JSON file inside this dir.
    repo_url_for_github = get_package_json(temp_location)
    
    print(repo_url_for_github)
    
    # No use for the zip anymore.
    os.remove(temp_location)

    return repo_url_for_github
 