#loads all finished phronesis data

#imports
import pandas as pd
import os

from assessment_adapter import process_assessments
from attendance_adapter import process_attendances
from model_adapter import merge_model_features
from model_adapter import risk_predict
from user_data import get_user_file


def load_app_data():

    ##########READ DATA##########

    students =pd.read_csv(get_user_file("students.csv"))
    assessment =pd.read_csv(get_user_file("assessment.csv"))
    attendance =pd.read_csv(get_user_file("attendance.csv"))
    classes =pd.read_csv(get_user_file("classes.csv"))
    subjects =pd.read_csv(get_user_file("subjects.csv"))
    class_students =pd.read_csv(get_user_file("class_students.csv"))

    #homework
    homework_file =get_user_file("homework_completion.csv")

    if os.path.exists(homework_file):
        homework =pd.read_csv(homework_file)
    else:
        homework =pd.DataFrame(
            columns=["student_id","homework_completion"]
        )

    #behaviour
    behaviour_file =get_user_file("behaviour.csv")

    if os.path.exists(behaviour_file):
        behaviour =pd.read_csv(behaviour_file)
    else:
        behaviour =pd.DataFrame(
            columns=["student_id","behaviour_incidents"]
        )


    ##########MODEL DATA##########

    assessment_features =process_assessments(assessment)
    attendance_features =process_attendances(attendance)

    merged_features =merge_model_features(
        students,
        assessment_features,
        attendance_features
    )

    prediction_results =risk_predict(
        merged_features
    )


    ##########CLASS DATA##########

    class_data =class_students.merge(
        classes,
        on="class_id",
        how="left"
    )

    class_data =class_data.merge(
        subjects[["subject_id","subject_name"]],
        on="subject_id",
        how="left"
    )

    class_data =class_data.rename(
        columns={"subject_name":"subject"}
    )

    class_data =class_data.merge(
        students[["student_id","name"]],
        on="student_id",
        how="left"
    )


    ##########ATTENDANCE##########

    class_data =class_data.merge(
        attendance_features,
        on="student_id",
        how="left"
    )


    ##########HOMEWORK##########

    class_data =class_data.merge(
        homework[["student_id","homework_completion"]],
        on="student_id",
        how="left"
    )


    ##########BEHAVIOUR##########

    class_data =class_data.merge(
        behaviour[["student_id","behaviour_incidents"]],
        on="student_id",
        how="left"
    )


    ##########PREDICTIONS##########

    prediction_headers =[
        "student_id",
        "subject",
        "prev_failure",
        "grade_average",
        "grade_change",
        "assessment_status",
        "prediction_status",
        "risk_prediction",
        "model_score"
    ]

    app_data =class_data.merge(
        prediction_results[prediction_headers],
        on=["student_id","subject"],
        how="left"
    )


    ##########MISSING DATA##########

    app_data["assessment_status"] =app_data[
        "assessment_status"
    ].fillna("Insufficient data")

    app_data["prediction_status"] =app_data[
        "prediction_status"
    ].fillna("Insufficient data")

    app_data["risk_prediction"] =app_data[
        "risk_prediction"
    ].fillna("Insufficient data")

    app_data["attendance_status"] =app_data[
        "attendance_status"
    ].fillna("Insufficient data")

    return app_data