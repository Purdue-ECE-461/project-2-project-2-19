# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 02:29:57 2021

@author: garvi
"""

'''
                            These are just my notes. 
                            Dont look here.
                            Go away.


File/Structure Guide:
     /
         Top level main
    /Project2
        Contains all the webapp front-end.
        and routing.
    /swagger_server
        Back-end stuff.
    

Baseline requirement
    You must support, via a REST-ful API:
    -	Upload, update, rate, and download individual packages, including the new metric
    -	Ingestion of a public npm package as described
    -	Paginated list of all packages
    -	Reset to default system state
    
    
    Just add Front-end and Token thing on top of this, fuck the rest dont have time
    nor do I care enough to do that shit.

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
        2. Convert package_create to /tmp/ for GCloud.
            https://stackoverflow.com/questions/61762429/how-to-upload-an-image-to-google-cloud-storage-from-app-engine

        3. (XAUTH) Piazza @153 talks more about, XAUTH... When I get to it lol.
        
        4. About page.
            Credit anyone who needs it/clear cache/instructions (how-to).
            
        5. Deploy and see if changes mitigate properly.
        

Todo:
    1. Make a new database cos idk
    2. Update front-end to call API
    3. all the other endpoints
    
    4. Error checking, end to end tests good response codes and so forth.

Questions.
    1. When passing metrics, what package to compare to? Existing? How to find metrics?
         AS of now I'm using random repos to normalize data.
    2. The backend is not deploying.
    3. IS my new metric correct?
    
    4. Test cases for deleting wtih more than 1 package version.
    5. Divide by zero errors.
    
    6. Uploading packages with same name and same version, same name diff version, diff name
    .. same version.
    
'''