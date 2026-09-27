# Phronesis Prototype

## Overview

Phronesis is a prototype student risk analytics system designed to help teachers identify students who may require additional support.

The system combines attendance, assessment, behaviour and homework data to generate:

* Student risk scores
* Risk categories (Low, Medium, High)
* Explanations of contributing factors
* Recommended interventions

## Licence and Attribution
The UCI Student Performance dataset used for model development is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
Dataset citation:
Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. 
https://archive.ics.uci.edu/dataset/320/student+performance


## Running the Prototype

1. Open the project folder.
2. Activate the Python environment.
3. Run:

streamlit run app.py

4. Open the local Streamlit URL shown in the terminal.

## Files

* students.csv
* attendance.csv
* assessment.csv
* behaviour.csv
* homework.csv

## Technologies Used

* Python
* Pandas
* Streamlit
