# Udacity Project: Logs Analysis
This is the first project for the Udacity Nanodegree Program "Full Stack Web Developer"

The main objective of this project is to show some analysis from a database data. The solution requires to build some sql queries and show the result in plain text

## Software Used
1. PostgreSQL
2. Python3 ( import psycopg2 for DB-API ) 
3. Vagrant (Virtual Machine) installed on VirtualBox 

##Installing Required Sofware
1. Download and install Virtual Box [link](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Download and install Vagrant [link](https://www.vagrantup.com/downloads.html)
3. Download the VM Configuration provide for Udacity. To do best practices, you can use Github to fork and clone the repository [Git Link to repository](https://github.com/udacity/fullstack-nanodegree-vm)

## Project Task
Then analysis solution needs to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The code needs to follow the next criterias:
- [x] The projects need to run without any erros
- [x] The code conforms to the PEP8 style recomendations
- [x] Each of the questions must be answered using one SQL query.
- [x] The resulst output needs to be in plain text

#### List of commands to run the project on the terminal in vagrant: 
1. ```vagrant up``` to start up the VM.
2. ```vagrant ssh``` to log into the VM.
3. ```cd /vagrant``` to change to your vagrant directory.
4. ```cd /<directory Name>``` to change to the directory where the user wants to store the source files (python and slq files)
5. ```python LogAnalysisMain.py``` to run the project.

## Views used
#### Used in the question #3 to create a log status
````sql
CREATE or REPLACE VIEW log_status as
        SELECT Date,Total,Error, (Error::float*100)/Total::float as Percent FROM
        (SELECT time::timestamp::date as Date, count(status) as Total, sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error FROM log
        GROUP BY time::timestamp::date) as result
        WHERE (Error::float*100)/Total::float > 1.0 ORDER BY Percent desc
````

## Expected Output: 
````
*****************************************************
What are the most popular three articles of all time?
*****************************************************

Article                           #of Views
-------------------------------------------
Candidate is jerk, alleges rival  338647
Bears love berries, alleges bear  253801
Bad things gone, say good people  170098

*****************************************************
Who are the most popular article authors of all time?
*****************************************************

Author                           #of Views
-------------------------------------------
Ursula La Multa                 507594
Rudolf von Treppenwitz          423457
Anonymous Contributor           170098
Markoff Chaney                  84557

*******************************************************
On which days did more than 1\% of requests lead to errors?
*******************************************************

Date                    Total           Error           Percent
-------------------------------------------
2016-07-17              55907           1265            2.2626862468
````
## Extra Development  - Not requiered for this project
Just for practicing the Flask examples on the material, I created a webPage to show data.

I used Flask server

#### List of commands to run the web project: 
1. ```vagrant up``` to start up the VM.
2. ```vagrant ssh``` to log into the VM.
3. ```cd /vagrant``` to change to your vagrant directory.
4. ```cd /<directory Name>``` to change to the directory where the user wants to store the source files (python and slq files)
5. ```python LogAnalysis.py``` to run the project.
5. ```http://localhost:8000/``` Open any browser and copy and paste the link

### Files Project Structure:
* ```static``` Folder -- Contains the style.css file for web solution
* ```templates``` Folder -- Contains the LogAnalysis.html for web solution
* ```LogAnalysis.py``` -- Run the tool web solution. 
* ```LogAnalysisDB.py``` -- Contains the python function for web solution
* ```LogAnalysisMain.py``` -- Contains the python logic for plain text solution (:warning:THIS IS THE MAIN FILE REQUESTED IN THE PROJECT)
* ```queries.py``` -- Contains the main queries for the project (This file is used for plain text and web solutions)
