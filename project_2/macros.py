# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:04:33 2021

@author: garvi
"""
import os
# This file has all the config variables at the top level.

# Library imports

GAC = "C:\\Users\\garvi\\Downloads\\purdue-project-2-c3aa3b050970.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GAC

CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')

FIRST_LOAD = True
