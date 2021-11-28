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
print(flask_app.config)
db = SQLAlchemy(flask_app)


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


# User ORM for SQLAlchemy
class Projects(db.Model):
    print(db)
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    name = db.Column(db.String(50), nullable = False, unique = False)
    version = db.Column(db.String(50), nullable = False, unique = False)
    
    # 1 row of metrics, forward link
    project_metrics = db.relationship("Metrics", back_populates="project_owner")    

    
    def __repr__(self):
        return f'\n========\nID: {self.id}\nName: {self.name}\nVersion: {self.version}\nMetrics: {self.project_metrics}\n=======\n'


class Metrics(db.Model):
    mid = db.Column(db.Integer, 
                    primary_key=True, nullable = False, unique = True)
    
    BusFactor = db.Column(db.Float, 
                         index=True)
    Correctness = db.Column(db.Float, index = True)
    GoodPinningPractice = db.Column(db.Float, index = True)
    LicenseScore = db.Column(db.Float, index = True)
    RampUp = db.Column(db.Float, index = True)
    ResponsiveMaintainer = db.Column(db.Float, index=True)

    
    # Back link to the project that can have 1 row of metrics.
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))


    # There is no reason to set this.
    project_owner = db.relationship("Projects", back_populates="project_metrics")
    
    
    def ingestible(self):
        return (self.BusFactor >= 0.5 and 
                self.Correctness >= 0.5 and
                self.GoodPinningPractice >= 0.5 and
                self.LicenseScore >= 0.5 and
                self.RampUp >= 0.5 and
                self.ResponsiveMaintainer >= 0.5)


    
    def __repr__(self):
        return '\n<METRICS \nBus: {} \
            \nCorrec: {}\nPins {}\nID: {}>'.format(self.BusFactor, 
                                                self.Correctness, 
                                                self.GoodPinningPractice,
                                                self.mid)



def add_project_db(name, version):
    project = Projects.query.filter_by(name = name).first()
    
#    db.session.merge()
#    db.create_all()
        
    print ("\n====================\n")
    for prj in Projects.query.all():
        print (prj)
    print ("\n====================\n\n")

    for metr in Metrics.query.all():
        print (metr)
        
    print ("\n====================\n\n")

    # This project is new.
    if not project:
        try:
            print ("adding new project")
            new_project = Projects(
                        name = name,
                        version = version
                )
            db.session.add(new_project)
            db.session.commit()
            
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
    db.session.query(Metrics).delete()
    db.session.query(Projects).delete()
    db.session.commit()
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
    return Metrics(BusFactor = 1.0,
                   Correctness = 1.0,
                   GoodPinningPractice = new_metric_value,
                   LicenseScore = 1.0,
                   RampUp = 1.0,
                   ResponsiveMaintainer = 1.0)

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
    
    response_code = add_project_db(name, version)
    
    if (response_code != 200):
        return response_code
    
    temp_location = 'output_file.zip'

    with open(temp_location, 'wb') as f:
        f.write(base64.b64decode(byteStream))
            
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
    
    
    # find the project that was recently created again.
            # since version and name both have to be the same find that.
    new_created_project = Projects.query.filter(Projects.name == name 
                                                and Projects.version == version).first()
    
    
    print ("Will link this: {}".format(new_created_project.name))
    
    # --------------------- QUESTION 2 IN DOCS TODO --------------- #
    metrics_class = get_metrics(repo_url_for_github, new_metric_val)
    
    
    print (new_metric_val)
    print (metrics_class)
    
    if (metrics_class.ingestible() == False):
        db.session.delete(new_created_project)
        db.session.commit()
        
        print ("Ingestion failed.")
        return -1
    
    print ("\n Ingestion Success.. \n")
    
    # Add the metric class to SQL instance, 
    # .. link with the new project, upload to the bucket.
    db.session.add(metrics_class)
    db.session.commit()
    
    # Link these two together.
    new_created_project.project_metrics = [metrics_class]
    metrics_class.project_id = new_created_project.id
    
    db.session.commit()
    
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
    print(blob.public_url)
    
    # No use for the zip anymore.
    os.remove(temp_location)

    return repo_url_for_github


def find_metrics_by_project(proj):
    mid = proj.project_metrics[0].mid
    return Metrics.query.filter(Metrics.mid == mid).first()

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
    return 200
    pass
 