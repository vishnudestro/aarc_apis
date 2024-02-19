AARC api wrappers
---

This project is an aggregation of all the supporting apis that are required for proper
 functioning of the Yekaliva. 
 
 Contains the following APIs. 
 
 TODO: Add the apis, their endpoints, their schemas
 

##### Initializing the project locally

1. We use pipenv to manage package dependencies. (Goodbye to virtualenvs and pip)
    - If you want to initalize a pipenv environment, (if there's no pipfile yet)
        `pipenv install --python /usr/local/bin/python3.6`
        - Make sure you have python3.6 installed in that location. ;) 
        
    - If you already have a pipfile in the project
        `pipenv install`
   
##### Steps to run locally.

1. You need to tell dynaconf where the configurations reside.
    `export ROOT_PATH_FOR_DYNACONF='aarc_apis/config'`
2. You also need to export FLASK_APP so dynaconf knows the application.
    ` export FLASK_APP='aarc_apis:create_app()' `
3. Activate the virtual env using pipenv
    `pipenv shell`
**Tip: Check if configurations are proper by running `flask routes`**
