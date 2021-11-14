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

from google.cloud import storage


# Package imports
from project_2 import util
from project_2 import macros


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


#https://stackoverflow.com/questions/54747460/how-to-decode-an-encoded-zipfile-using-python
def convert_and_upload_zip(byteStream):
    '''
    Params
        byteStream: the base64 encoded zip file.
    '''
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
 