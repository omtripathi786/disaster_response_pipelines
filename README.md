# Disaster Response Pipeline Project

## Installation
The code contained in this repository was written in HTML and Python 3, and requires the following Python packages: json, plotly, pandas, nltk, flask, sklearn, sqlalchemy, sys, numpy, re, pickle, warnings.

## Project Overview
This repository contains code for a web app which an emergency worker could use during a disaster event (e.g. an earthquake or hurricane), to classify a disaster message into several categories, in order that the message can be directed to the appropriate aid agencies. 

The app uses a ML model to categorize any new messages received, and the repository also contains the code used to train the model and to prepare any new datasets for model training purposes.

## File Descriptions
* **process_data.py**: This code takes as its input csv files containing message data and message categories (labels), and creates an SQLite database containing a merged and cleaned version of this data.
* **train_classifier.py**: This code takes the SQLite database produced by process_data.py as an input and uses the data contained within it to train and tune a ML model for categorizing messages. The output is a pickle file containing the fitted model. Test evaluation metrics are also printed as part of the training process.
* **ETL Pipeline Preparation.ipynb**: The code and analysis contained in this Jupyter notebook was used in the development of process_data.py. process_data.py effectively automates this notebook.
* **ML Pipeline Preparation.ipynb**: The code and analysis contained in this Jupyter notebook was used in the development of train_classifier.py. In particular, it contains the analysis used to tune the ML model and determine which algorithm to use. train_classifier.py effectively automates the model fitting process contained in this notebook.
* **data**: This folder contains sample messages and categories datasets in csv format.
* **app**: This folder contains all of the files necessary to run and render the web app.

## Running Instructions
### ***Run process_data.py***
1. Save the data folder in the current working directory and process_data.py in the data folder.
2. From the current working directory, run the following command:
`python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`

### ***Run train_classifier.py***
1. In the current working directory, create a folder called 'models' and save train_classifier.py in this.
2. From the current working directory, run the following command:
`python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

### ***Run the web app***
1. Save the app folder in the current working directory.
2. Run the following command in the app directory:
    `python run.py`
3. Go to http://127.0.0.1:9000/

Note :- before running the web app make sure you have run both pipeline script.
inorder to genrate the db and model file. and then give the same db file name in run.py file.

## ***Project screenshots and Data visualization***
![Alt text](screenshots//ss1.jpg?raw=true )
![Alt text](screenshots//ss2.jpg?raw=true )
![Alt text](screenshots//ss3.jpg?raw=true )

## ***Licensing, Authors, Acknowledgements***
This app was completed as part of the [Udacity Data Scientist Nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025). Code templates and data were provided by Udacity. The data was originally sourced by Udacity from Figure Eight
