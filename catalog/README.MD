# Udacity Project: Catalog App Project
This is a Flask/Python project for the Udacity Nanodegree Program "Full Stack Web Developer"

The main objective of this project is create a web site Using Flask/Python. 
The solution implements API Dev, CRUD and Google Authentication

## Software Used
1. PostgreSQL
2. Python3 ( import psycopg2 for DB-API ) 
3. Vagrant (Virtual Machine) installed on VirtualBox 

## Installing Required Sofware
1. Download and install Virtual Box [link](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Download and install Vagrant [link](https://www.vagrantup.com/downloads.html)
3. Download the VM Configuration provide for Udacity. To do best practices, you can use Github to fork and clone the repository [Git Link to repository](https://github.com/udacity/fullstack-nanodegree-vm)
4. Now using a terminal (On windows or linux) change directory to vagrant folder ```cd /vagrant```

## Required Libraries
This are the libraries that need to pre-install before to run the project:
1. ```python3 -m pip install flask```
2. ```python3 -m pip install sqlalchemy```
3. ```python3 -m pip install oauth2client```
4. ```python3 -m pip install  requests```

#### List of commands to run the project on the terminal in vagrant: 
1. ```vagrant up``` to start up the VM.
2. ```vagrant ssh``` to log into the VM.
3. ```cd /vagrant``` to change to your vagrant directory.
4. ```cd /catalog``` to change to the directory where the user wants to store the source files (python and slq files)
5. ```python3 database_setup.py``` to create the Database
6. ```python3 project.py``` to run the project.
7. ```Access the application locally using http://localhost:5000``` to run the project.

#### Optional: 
```python3 addDatatoDB.py``` to add Dummy Data







