# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 23:04:33 2021

@author: garvi
"""

'''
    This file has all the config variables at the top level.
'''

#Library imports
import os



# I dont know why I need to do this, its stupid. but thats life.
GAC = "C:\\Users\\garvi\\Downloads\\purdue-project-2-c3aa3b050970.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GAC

CLOUD_STORAGE_BUCKET = os.getenv('CLOUD_STORAGE_BUCKET')

first_load = True