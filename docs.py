# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 02:29:57 2021

@author: garvi
"""

'''
Baseline requirement
    You must support, via a REST-ful API:
    -	Upload, update, rate, and download individual packages, including the new metric
    -	Ingestion of a public npm package as described
    -	Paginated list of all packages
    -	Reset to default system state

Progress:
    [Note to self: Dont change file location]
        file:///C:/Users/garvi/Downloads/P2M1n%20(3).pdf

Todos:
    Storage Phase:
        1. Change the "tmp_file" destination to cloud with the NAME and ID identifiers.
            It's overwriting right now.
            
        2. Metric calculations, DB storage, uploading the latter.
        
    
    Fetching Phase:
        1. Everything else really. EZ-PZ if storage is good.
    

    Other Crap:
        1. Set up CI/CD.

        2. Convert package_create to /tmp/ for GCloud.
            https://stackoverflow.com/questions/61762429/how-to-upload-an-image-to-google-cloud-storage-from-app-engine

        3. (XAUTH) Piazza @153 talks more about, XAUTH... When I get to it lol.
        
        4. About page.
            Credit anyone who needs it/clear cache/instructions (how-to).
            
        5. Deploy and see if changes mitigate properly.
'''