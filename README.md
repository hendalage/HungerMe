# PWP SPRING 2021
# HungerMe
# Group information
* Student 1. Ashan Chameera , awalpita20@student.oulu.fi
* Student 2. Piushana Abeygunawardane
* Student 3. Chathushka Hendalage 
* Student 3. Nisita Weerasinghe

__*Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

Please install all the dependencies using
```  
    pip install -r requirements.txt
```


#How to Run
__Add following- Run in a powershell (Windows)__

* $env:FLASK_ENV = "development"
* $env:FLASK_APP = "project"
* flask run


1. __init__.py file contains the script to create the HRCore database and then insert data to the database. You can change/add/delete insert values in there.
```  
    flask init-db
    flask testgen
```

Install pylit using below command
```
pip install pylint
```


How to install required libries for testing - pytest, pytest-cov
```
pip install pytest
pip install pytest-cov
```




