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
    print(db)
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    name = db.Column(db.String(50), nullable = False)
    version = db.Column(db.String(50), nullable = False, unique = False)
    
    # 1 row of metrics, forward link
    project_metrics = db.relationship("Metrics", back_populates="project_owner")    

    
    def __repr__(self):
        return f'\n========\nID: {self.id}\nName: {self.name}\nVersion: {self.version}\nMetrics: {self.project_metrics}\n=======\n'


class Metrics(db.Model):
    mid = db.Column(db.Integer, 
                    primary_key=True)
    
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


    
    def __repr__(self):
        return '<METRICS \nBus: {}\nID: {}>'.format(self.BusFactor, self.mid)



def add_project_db(name, version):
    project = Projects.query.filter_by(name = name).first()
    
    db.create_all()
        
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
            print ("HEY adding new")
            new_project = Projects(
                        name = name,
                        version = version
                )
            db.session.add(new_project)
            db.session.commit()
            
            print ("here")
            return 200
        except Exception as e:
            print (e)
            return 404
    else:
        print ("Failed if")
        return 403

    print ("NOT HERE")
    # it should not get here
    return -1


def tear_down():
    db.session.query(Metrics).delete()
    db.session.query(Projects).delete()
    db.session.commit()

def get_metrics(repo_url):
    return Metrics(BusFactor = 1.0,
                   Correctness = 1.0,
                   GoodPinningPractice = 1.0,
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
    try:
        repo_url_for_github = get_package_json(temp_location)
    except:
        print ("No Repo Link")
    
    
    # find the project that was recently created again.
    new_created_project = Projects.query.filter(Projects.name == name 
                                                and Projects.version == version).first()
    
    
    print ("Will link this: {}".format(new_created_project.name))
    
    # --------------------- QUESTION 2 IN DOCS TODO --------------- #
    metrics_class = get_metrics(repo_url_for_github)
    
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
 