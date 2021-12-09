# project-2-project-2-19
<br>
This project is a NPM-registry with authentication. <br>

<br>
The registry supports the following operations:<br>
    GET requests:
    
1. Getting package history when package is requested by name. 
2. Getting package by package id. 
3. Rating uploaded packages on Ramp-up time, correctness, bus factor, maintainer responsivity, license compatibility, dependency pinning. 

POST requests:

1. Creating/uploading a new package
2. Ingestion of public npm packages when package is posted with URL field but without content field.
4. Ingestion of packages with at least a 0.5 rating on all relevant metrics. 
5. Gets paginated list of all packages currently in the registry

PUT requests:
1. Update the version of a package already in the registry using its name, id, and version.
2. Create auth token for a default user with the following credentials:


    Username: ece461defaultadmin<br>
    Password: correcthorsebatterystaple123(!__+@**(A

DELETE requests:
1. Deleting a particular version of a package
2. Deleting all versions of a package
3. Resetting the entire registry to its default state.

The registry uses Google App Engine, Google Compute Engine, and a MySQL Database while exposing a single api instance to users. 

The webpage is ADA compliant as verified by Microsofts automated accessibility checks. 

The link to access the registry is:

    https://purde-final-project.appspot.com 

Trustworthy Modules Registry by Group 19.
