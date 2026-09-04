#imports
import pandas as pd
from model_adapter import process_assessments

#read in assessment data
assessment= pd.read_csv("data/new/assessment.csv")

#generate assessment features
assessment_features= process_assessments(assessment)

print(assessment_features)