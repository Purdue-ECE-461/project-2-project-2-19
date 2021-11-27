# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:24:05 2021

@author: garvi
"""

#Libraries
import os
from dotenv import load_dotenv
load_dotenv()

#Packages
from Project2 import app

flask_app = app.app
app.add_api('swagger.yaml')

PASSWORD=os.getenv("DB_PASS")
PUBLIC_IP_ADDRESS =os.getenv("DB_IP")
DBNAME ="projects"
PROJECT_ID ="purdue-project-2"
INSTANCE_NAME ="project-db"
 
# configuration
flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
flask_app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
