#imports
import pandas as pd

from assessment_adapter import process_assessments
from attendance_adapter import process_attendances
from model_adapter import merge_model_features
from model_adapter import risk_predict


def load_app_data():
    #read student assessment and attendance data
    students =pd.read_csv("data/new/students.csv")
    assessment =pd.read_csv("data/new/assessment.csv")
    attendance =pd.read_csv("data/new/attendance.csv")

    #generate assessment features
    assessment_features =process_assessments(assessment)

    #generate attendance features
    attendance_features =process_attendances(attendance)

    #merge student, assessment and attendance features
    merged_features = merge_model_features(students,assessment_features,attendance_features)

    #generate random forest risk predictions
    prediction_results = risk_predict(merged_features)

    return prediction_results