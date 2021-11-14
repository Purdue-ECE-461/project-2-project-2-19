# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 01:24:05 2021

@author: garvi
"""


from Project2 import app
from dotenv import load_dotenv
load_dotenv()

app.add_api('swagger.yaml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
