#combines assessment and attendance together
import pandas as pd
import joblib

def merge_model_features(students,assessment_features, attendance_features):
    #make copy so original student data not changed
    students = students.copy()

    #start with student data, merge in assessment and attendance features
    # - so all students included even if no assessment or attendance data
    merged_features = students.merge(assessment_features,on="student_id",how="left")

    merged_features = merged_features.merge(attendance_features,on="student_id",how="left")

    #four features needed by random forest
    model_columns=["prev_failure","absences","grade_average","grade_change"]

    #all four model features exist for each row?
    all_features_present = merged_features[model_columns].notna().all(axis=1)

    #assessment and attendance data are valid?
    valid_status =(
        (merged_features["assessment_status"] =="Valid")
        &
        (merged_features["attendance_status"] =="Valid")
    )

    #start with a default-insufficient data
    merged_features["prediction_status"] ="Insufficient data"

    #valid and complete- are ready for prediction
    ready_rows = all_features_present & valid_status

    merged_features.loc[ready_rows,"prediction_status"] ="Ready"

    return merged_features



#################Random Forest Model adaption################
def risk_predict(merged_features):
    #make copy so og data not changed
    prediction_data = merged_features.copy()

    #four random forest features needed for prediction
    model_columns=["prev_failure","absences","grade_average","grade_change"]

    #start every row with insufficient data
    prediction_data["risk_prediction"] ="Insufficient data"

    #store model score internally for later use
    prediction_data["model_score"] = pd.NA

    #only ready rows with all 4 can be predicted
    ready_rows=(prediction_data["prediction_status"]=="Ready")

    #if no ready students, return early
    if not ready_rows.any():
        return prediction_data
    
    #model input- copy of ready 4
    model_input = prediction_data.loc[ready_rows, model_columns].copy()

    #make sure model input is numeric
    for column in model_columns:
        model_input[column] =pd.to_numeric(model_input[column],errors="coerce")

    #CHECK!-no missing values in model input
    if model_input.isna().any().any():
        raise ValueError("Missing values in model input")
    
    #load trained random forest model
    rf_model = joblib.load("models/final_random_forest_2b.joblib")

    #find probability column for atRisk
    at_risk_col= list(rf_model.classes_).index(1)

    #get model score-atRisk
    risk_probabilities = rf_model.predict_proba(model_input)[:,at_risk_col]

    #use original 0.5 threshold to classify as atRisk or not
    risk_predictions = (risk_probabilities >=0.5).astype(int)

    #store score  internally for later use
    prediction_data.loc[ready_rows, "model_score"] = risk_probabilities
    prediction_data.loc[ready_rows, "risk_prediction"] =[
        "At Risk" if pred==1 
        else "Not At Risk" 
        for pred in risk_predictions
    ]

    return prediction_data


