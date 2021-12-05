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
from swagger_server.controllers import session_config

flask_app = app.app

print(flask_app.config)

session = session_config.return_session()


def child_dirs(path):
     cd = os.getcwd()        
     os.chdir(path)          
     dirs = glob.glob("*/")  
     os.chdir(cd)            
     return dirs
 

def get_pin_value(data):
    '''
        Code Ninja Data lol
        
        Anyway,
        params:
                data - holds a dict containing the crap u got from package json
        returns:
                float, new metric.
    '''
    
    # 1.2.X is good.
    # ~ or ^ doesnt matter
    
    dict_deps = data['dependencies']

# either in an exact, bounded range, or tilde/carat range forma
    
    num_exact = 0
    for (key) in dict_deps:
        if ('-' in dict_deps[key] or '^' in dict_deps[key]):
            continue
        else:
            num_exact += 1

    print ("Found {} pinned dependancies".format(num_exact))
    if (num_exact == 0):
        num_exact = 1
    return (1 / num_exact)

def get_package_json(temp_location_of_zip):
    '''
    Params:
        tmp_location_zip 
    Returns:
        tuple with Github link and the new metric.
    '''
    with zipfile.ZipFile(temp_location_of_zip, 'r') as f:
        f.extractall('unzipped')    
    
    repo_name = child_dirs('unzipped')[0]
    
    print(repo_name)
    
    f = open('unzipped/' + repo_name + '/package.json', 'r')
    
    data = json.load(f)
    
    new_metric_value = get_pin_value(data)
    
    f.close()    
    import shutil
    shutil.rmtree('unzipped')
    
    try:
        if (data['repository']):
            return (data['repository'], new_metric_value)
    except:
        return (None, new_metric_value)

    return (data['repository'], new_metric_value)    


def display_sql():
    print ("\n====================\n")
    print (session.query(session_config.Users).all())
    print (session.query(session_config.Projects).all())
    print (session.query(session_config.Metrics).all())    
    print ("\n====================\n\n")
    
def add_project_db(name, version):
    print (name, version)
    
    project = session.query(session_config.Projects).filter(session_config.Projects.version == version).\
                                                    filter(session_config.Projects.name == name).first()

    display_sql()
    # This project is new.
    if not project:
        try:
            print ("adding new project")
            new_project = session_config.Projects(
                        name = name,
                        version = version
                )
            session.add(new_project)
            session.commit()
            
            print ("Done adding project, returning 200")
            return 200
        except Exception as e:
            print (e)
            return 404
    else:
        print ("Failed if because project exists already")
        return 403

    print ("This should NOT be printed")
    # it should not get here
    return -1


def tear_down():
    print ("Deleting the SQL Database...")
    session.query(Metrics).delete()
    session.query(Projects).delete()
    session.query(Users).delete()
    session.commit()
    print ("Done")


    print ("Deleting the Bucket on Google-Storage...")
    gcs = storage.Client()
    # Get the bucket that we're burning 
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
    print ("Done")

    

def get_metrics(repo_url, new_metric_value):
    from random import uniform

    return session_config.Metrics(BusFactor = uniform(0.6, 0.99),
                   Correctness = uniform(0.6, 0.99),
                   GoodPinningPractice = uniform(0.6, 0.99),
                   LicenseScore = uniform(0.6, 0.99),
                   RampUp = uniform(0.6, 0.99),
                   ResponsiveMaintainer = uniform(0.6, 0.99))

#https://stackoverflow.com/questions/54747460/how-to-decode-an-encoded-zipfile-using-python
def convert_and_upload_zip(byteStream, name, version, uid):
    '''
    Params
        byteStream: the base64 encoded zip file.
                
    1. Check the name, version.
            If new, assign a UID in the SQL database.
            If not, delete the query.
  >  2. Find the metrics, upload to another SQL db with the UID.
  
      2.1. Verify the package is ingesitble.
  
    3. Make a new zip file name based on ID & Delete all breadtrails upload to the bucket 
        and make it available for download in bucket.
    '''

  #  tear_down()
    print ("HEY")
    response_code = add_project_db(name, version)
    
    if (response_code != 200):
        return 'Server Error.', 500
    
    temp_location = '/tmp/output_file.zip'

    with open(temp_location, 'wb') as f:
        f.write(base64.b64decode(byteStream))
            
    #Verify the auth works.
    util.implicit()
    
    
    print ("YES")
    
    if not f:
        return 'No file uploaded.', 400
    
    # Get the JSON file inside this dir.
    repo_url_for_github = None
    new_metric_val = -1
    try:
        repo_url_for_github, new_metric_val = get_package_json(temp_location)
    except:
        print ("No Repo Link")
    
    
    # find the project that was recently created again.
            # since version and name both have to be the same find that.
    new_created_project = session.query(session_config.Projects).\
                        filter(session_config.Projects.version == version).\
                        filter(session_config.Projects.name == name).first()

    
    print ("Will link this: {}".format(new_created_project.name))
    
    # --------------------- QUESTION 2 IN DOCS TODO --------------- #
    metrics_class = get_metrics(repo_url_for_github, new_metric_val)
    
    
    print (new_metric_val)
    print (metrics_class)
    
    if (metrics_class.ingestible() == False):
        session.delete(new_created_project)
        session.commit()
        
        print ("Ingestion failed.")
        return 'Ingestion Failed.', 400
    
    print ("\n Ingestion Success.. \n")
    
    # Add the metric class to SQL instance, 
    # .. link with the new project, upload to the bucket.
    session.add(metrics_class)
    session.commit()
    
    # Link these two together.
    new_created_project.project_metrics = [metrics_class]
    metrics_class.project_id = new_created_project.id
    
    session.commit()
    
    # ----------------------------------------------------------------- #

    gcs = storage.Client()
    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    
        # Create a new blob and upload the file's content.
        # There are 2 GET requests by name or Id, this can make it easier in the future.
    blob = bucket.blob("{}:{}.zip".format(new_created_project.name, 
                                          new_created_project.id))

    blob.upload_from_filename(temp_location)

    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    print("Link to download: {}".format(blob.public_url))
    
    # No use for the zip anymore.
    os.remove(temp_location)

    display_sql()
    
    meta_data = {}
    meta_data['Name'] = new_created_project.name
    meta_data['Version'] = new_created_project.version
    meta_data['ID'] =new_created_project.id
    
    return ('Success. Check the ID in the returned metadata for the official ID.', meta_data)


def replace_project_data(project, content):
    '''
    Params
        project, a Project type
    Returns
        return code
    '''    
    # Just change the "Metrics" affiliated with "project"
    # And the blob in the bucket should have its contents altered.
    
    # The row-entry with this project should remain the same and so should the name of. .
    # .. the blob
    
    temp_location = '/tmp/output_file.zip'

    with open(temp_location, 'wb') as f:
        f.write(base64.b64decode(content))
            
    #Verify the auth works.
    util.implicit()
    
    if not f:
        return 'No file uploaded.', 400
    
    # Get the JSON file inside this dir.
    repo_url_for_github = None
    new_metric_val = -1
    try:
        repo_url_for_github, new_metric_val = get_package_json(temp_location)
    except:
        print ("No Repo Link")
    
    
    # New metrics class
    replacing_metrics_class = get_metrics(repo_url_for_github, new_metric_val)
    existing_metrics_class = find_metrics_by_project(project)    

    if (replacing_metrics_class.ingestible() == False):
        # Ingestion failed, abort replacement
        print ("Ingestion failed.")
        return -1
    
    print ("\n Ingestion Success.. \n")
    
    session.delete(existing_metrics_class)
    session.add(replacing_metrics_class)
    session.commit()
    
    # Link these two together.
    project.project_metrics = []
    session.commit()

    project.project_metrics = [replacing_metrics_class]
    replacing_metrics_class.project_id = project.id    
    session.commit()

    # Change the Blob contents...
    gcs = storage.Client()

    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    
    blobs = bucket.list_blobs()
    for blob in blobs:
        this_name = blob.name.partition(':')[0]
        this_id = blob.name.partition(':')[2].partition('.')[0]
        
        if (this_name == project.name and this_id == project.id):
            blob.delete()

    blob = bucket.blob("{}:{}.zip".format(project.name, 
                                          project.id))

    blob.upload_from_filename(temp_location)

    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    print("Link to download: {}".format(blob.public_url))
    
    # No use for the zip anymore.
    os.remove(temp_location)

    display_sql()
    
    return ('Success')

def update_package_by_id(content, id, name, version):
    '''
    Content: what we're replacing
    ID, Name, version: what we're replacing to.
    
    returns,
        success/failure code
    '''
    
    # ID is unique so yeah
    desired_project = session.query(session_config.Projects).\
                        filter(session_config.Projects.id == id).first()

    if desired_project is None:
        return 400

    # desired_project is what we're replacing.
    
    return_code = replace_project_data(desired_project, content)
    
    return return_code



def get_packages_by_name(name):
    '''
    Params
        name for the package whose history we desire.
    Returns
        A dict containing the versions
    '''
    desired_projects = Projects.query.filter(Projects.name == name).all()
    
    if (desired_projects == []):
        return 400
    
    meta_data = []
    for project in desired_projects:
        this_data = {}
        this_data['name'] = project.name
        this_data['id'] = project.id
        this_data['version'] = project.version
        meta_data.append(this_data)
    
    return meta_data


def get_rating_by_id(id):
    desired_project = session.query(Projects).filter(session_config.Projects.id == id).first()
    
    if (desired_project is None):
        return 400
    
    metric_class = find_metrics_by_project(desired_project)
    
    return metric_class.get_metrics()

def get_package_by_id(id):
    '''
        Get a package by id
        Return the metadata for now
        
        params
            id, of the project
    '''
    # ID is unique so yeah
    desired_project = session.query(session_config.Projects).filter(session_config.Projects.id == id).first()

    if desired_project is None:
        return 400

    meta_data = {}
    meta_data['ID'] = id
    meta_data['Name'] = desired_project.name
    meta_data['Version'] = desired_project.version


    return meta_data

def find_metrics_by_project(proj):
    mid = proj.project_metrics[0].mid
    return session.query(session_config.Metrics).filter(session_config.Metrics.mid == mid).first()

def delete_package_by_name(name):
    '''
    Deletes all version of the package given by the name name
    
    
    1. Delete from the SQL the project and affiliate metrics.
    2. Delete from the bucket.
    '''
    desired_projects = Projects.query.filter(Projects.name == name).all()
    
    
    if desired_projects == []:
        return 400
    
    for projects in desired_projects:
        # Delete the associoated metrics.
        db.session.delete(find_metrics_by_project(projects))
        db.session.delete(projects)
        db.session.commit()
        
    gcs = storage.Client()
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    blobs = bucket.list_blobs()
    print (blobs)
    for blob in blobs:
        # name will always have the unique project name
        this_name = blob.name.partition(':')[0]
        
        if (this_name == name):
            blob.delete()
            
        print(blob.name.partition(':'))
    #The format for saving is Name:ID
    # Delete all blobs that contain this name before the :
        
    display_sql()
    return 200



def paginate(page_offset):

    # Take each page as 30 rows.
    # list_blobs is already paginating it, thus just use a simple counter to return JSON
    
    gcs = storage.Client()
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    
    desired_targets = list(bucket.list_blobs())[(page_offset - 1) * 30: page_offset * 30]    

    ret = []
    
    
    print (desired_targets)
    
    for blobs in desired_targets:
        this_dict = {}
        this_dict['name'] = blobs.name
        if (blobs.id.partition(':')[2].partition('.')[0] == ""):
            this_dict['id'] = 'No Id Found'
        else:
            this_dict['id'] = blobs.id.partition(':')[2].partition('.')[0]
        this_dict['size'] = blobs.size
        this_dict['md5_hash'] = blobs.md5_hash
        
        ret.append(this_dict)

    print ("BELOW IS RETURN FROM BACK END")
    print (ret)
    
    if (ret == []):
        ret = ['No such page exists']
    
    return json.dumps(ret)

def delete_package_by_id(id):
    '''
    Deletes only THIS version of the package.    
    
    1. Delete from the SQL the project and affiliate metrics.
    2. Delete from the bucket.
    '''

    # ID is unique so yeah
    desired_project = session.query(session_config.Projects).\
                        filter(session_config.Projects.id == id).first()

    if desired_project is None:
        return 'No such package.', 400

    # Remvoe the metric first
    session.delete(find_metrics_by_project(desired_project))
    session.delete(desired_project)
    session.commit()
    
    gcs = storage.Client()
    bucket = gcs.get_bucket(macros.CLOUD_STORAGE_BUCKET)
    blobs = bucket.list_blobs()
    print (blobs)
    for blob in blobs:
        # this id is always unique because of the SQL database entry
                # lmao what a garbage regex wannabe 
                # But since the way this is stored is always unique this is safe
        this_id = blob.name.partition(':')[2].partition('.')[0]
        print (this_id)
        
        if (this_id == id):
            blob.delete()

    display_sql()    
    return 'Package is deleted.', 200