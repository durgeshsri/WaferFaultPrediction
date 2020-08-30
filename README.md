# WaferFaultPrediction


## Table of Content
  * [Overview](#overview)
  * [Technical Aspect](#technical-aspect)
  * [Installation](#installation)
  * [Technologies Used](#technologies-used)
  * [Team](#team)
  * [Credits](#credits)


## Overview:
   This is a simple wafer quality binary classification Flask app trained on the top of Sklearn API and  XGBoost. The trained models takes a Batch file (All Sensor's Data)  as an input and predict the class of output 0/1(Good/Bad) , and will create a predicted batch csv file in local system which will have two columns wafer name and their quality(Good-0 / Bad-1)



## Technical Aspect:
   This project is divided into two part:
   1. Training
       -  Validating all raw data file according to schema file(Have all the information about Good Raw Data).
       -  Storing good raw data to a SQLite3 data base.
       -  Imporing the data from SQLite3 data base to local in form of csv.
       -  Dividing the data into clusters using KMean Clusterig and train clusters with best Machine learning models using Sklearn and XGBoost API.
       -  Building a Flask web app.
   2. Prediction
       -  Validating all raw data file according to schema file(Have all the information about Good Raw Data).
       -  Storing good raw data to a SQLite3 data base.
       -  Imporing the data from SQLite3 data base to local in form of csv.
       -  Dividing the data into clusters using KMean Clusterig and predict these clusters with best Machine learning models.
       

## Installation
The Code is written in Python 3.7. If you don't have Python installed you can find it [here](https://www.python.org/downloads/). If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip. To install the required packages and libraries, run this command in the project directory after [cloning](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/) the repository:

```bash
pip install -r requirements.txt
```

## Technologies Used
    -  Python
    -  Sklearn
    -  XGBoost
    -  SQLite3
    -  Flask
    -  Gunicorn

## Team

 ![Durgesh Kumar](https://user-images.githubusercontent.com/22117967/91654030-568fac00-eac3-11ea-836b-f2c35eb632c7.jpg) |
 -|
[Durgesh Kumar](https://www.linkedin.com/in/durgesh-kumar-961b0b159/) |)


## Credits
[iNeuron.ai](https://ineuron.ai/) - This project wouldn't have been possible without their helps. They always were with for any kind of problem.
       
