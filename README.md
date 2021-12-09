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

DELETE requests:
1. Deleting a particular version of a package
2. Deleting all versions of a package
3. Resetting the entire registry to its default state.

The registry uses Google App Engine, Google Compute Engine, and a MySQL Database while exposing a single api instance to users. 

The webpage is ADA compliant as verified by Microsofts automated accessibility checks. 

The link to access the registry is:

    https://purde-final-project.appspot.com 

The directory structure for the frontend of our project is as follows:
    
    |   apiroutes.py
    |   macros.py
    |   routes.py
    |   swagger.yaml
    |   util.py
    |   __init__.py
    |
    +---static
    |       about.css
    |       ada_compliance.PNG
    |       index.css
    |       tutorial_pagination_front.PNG
    |       ui.css
    |       view.css
    |
    +---templates
    |       about.html
    |       index.html
    |       ui.html
    |       view.html
    |
    \---__pycache__
            apiroutes.cpython-39.pyc
            macros.cpython-37.pyc
            macros.cpython-39.pyc
            routes.cpython-37.pyc
            routes.cpython-39.pyc
            util.cpython-37.pyc
            util.cpython-39.pyc
            __init__.cpython-37.pyc
            __init__.cpython-39.pyc```

The directory structure for our swagger_server is as follows:
    
    |   encoder.py
    |   type_util.py
    |   util.py
    |   __init__.py
    |
    +---controllers
    |   |   authorization_controller.py
    |   |   controller_helper.py
    |   |   default_controller.py
    |   |   ranking_module.py
    |   |   session_config.py
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           controller_helper.cpython-37.pyc
    |           controller_helper.cpython-39.pyc
    |           default_controller.cpython-37.pyc
    |           default_controller.cpython-39.pyc
    |           ranking_module.cpython-37.pyc
    |           session_config.cpython-37.pyc
    |           session_config.cpython-39.pyc
    |           __init__.cpython-37.pyc
    |           __init__.cpython-39.pyc
    |
    +---models
    |   |   authentication_request.py
    |   |   authentication_token.py
    |   |   base_model_.py
    |   |   enumerate_offset.py
    |   |   error.py
    |   |   package.py
    |   |   package_data.py
    |   |   package_history_entry.py
    |   |   package_id.py
    |   |   package_metadata.py
    |   |   package_name.py
    |   |   package_query.py
    |   |   package_rating.py
    |   |   semver_range.py
    |   |   user.py
    |   |   user_authentication_info.py
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           authentication_request.cpython-37.pyc
    |           authentication_request.cpython-39.pyc
    |           authentication_token.cpython-37.pyc
    |           authentication_token.cpython-39.pyc
    |           base_model_.cpython-37.pyc
    |           base_model_.cpython-39.pyc
    |           enumerate_offset.cpython-37.pyc
    |           enumerate_offset.cpython-39.pyc
    |           error.cpython-37.pyc
    |           error.cpython-39.pyc
    |           package.cpython-37.pyc
    |           package.cpython-39.pyc
    |           package_data.cpython-37.pyc
    |           package_data.cpython-39.pyc
    |           package_history_entry.cpython-37.pyc
    |           package_history_entry.cpython-39.pyc
    |           package_id.cpython-37.pyc
    |           package_id.cpython-39.pyc
    |           package_metadata.cpython-37.pyc
    |           package_metadata.cpython-39.pyc
    |           package_name.cpython-37.pyc
    |           package_name.cpython-39.pyc
    |           package_query.cpython-37.pyc
    |           package_query.cpython-39.pyc
    |           package_rating.cpython-37.pyc
    |           package_rating.cpython-39.pyc
    |           semver_range.cpython-37.pyc
    |           semver_range.cpython-39.pyc
    |           user.cpython-37.pyc
    |           user.cpython-39.pyc
    |           user_authentication_info.cpython-37.pyc
    |           user_authentication_info.cpython-39.pyc
    |           __init__.cpython-37.pyc
    |           __init__.cpython-39.pyc
    |
    +---test
    |   |   test_default_controller.py
    |   |   __init__.py
    |   |
    |   \---__pycache__
    |           __init__.cpython-39.pyc
    |
    \---__pycache__
            encoder.cpython-37.pyc
            type_util.cpython-37.pyc
            type_util.cpython-39.pyc
            util.cpython-37.pyc
            util.cpython-39.pyc
            __init__.cpython-37.pyc
            __init__.cpython-39.pyc
            __main__.cpython-37.pyc
            __main__.cpython-39.pyc

The files for the project outside the server and frontend directories are:

    |   .env
    |   .gcloudignore
    |   API tests
    |   app.yaml
    |   correctapi.yaml
    |   docs.py
    |   express-master.zip
    |   main.py
    |   react-main.zip
    |   README.md
    |   requirements.txt
    |   test.py
    |   test_suite.py
    
 
Trustworthy Modules Registry by Group 19.
