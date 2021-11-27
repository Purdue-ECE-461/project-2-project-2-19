# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:24:05 2021

@author: garvi
"""


from Project2 import app
from dotenv import load_dotenv
import os

load_dotenv()

app.add_api('swagger.yaml')
flask_app = app.app
flask_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
