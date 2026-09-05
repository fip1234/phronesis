#combines assessment and attendance together
import pandas as pd


def merge_model_features(assessment_features, attendance_features):
    #combine attendance onto assessment data with student id
    merged_features = assessment_features.merge(attendance_features,on="student_id",how="left")

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