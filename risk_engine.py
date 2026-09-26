# risk_engine.py- rule based risk engine by awarding different risk points based on student data
#eeps risk logic separate from the user interface

import pandas as pd

def is_missing(value):
    return pd.isna(value)

def calculate_risk(row):
    risk = 0

    #if attendance < 75% add high risk points
    # if attendance < 90% add medium risk points
    if not is_missing(row["attendance_percentage"]):
        if row["attendance_percentage"] <75:
            risk += 30
        elif row["attendance_percentage"] < 90:
            risk += 10

    #if assessment score < 50 add high risk points
    # if assessment score < 70 add medium risk points
    if not is_missing(row["assessment_score"]):
        if row["assessment_score"] <50:
            risk += 30
        elif row["assessment_score"] <70:
            risk += 15

    #if homework < 50 add high risk points
    # if homework < 75 add medium risk points
    if not is_missing(row["homework_completion"]):
        if row["homework_completion"] <50:
            risk += 20
        elif row["homework_completion"] <75:
            risk += 10

    #if behaviour points > 4 add high risk points
    # if behaviour points > 1 add medium risk points
    if not is_missing(row["behaviour_points"]):
        if row["behaviour_points"] >4:
            risk += 20
        elif row["behaviour_points"] > 1:
            risk += 10

    return risk


###########RISK CATEGORISATION
def risk_category(score):
    if score >=60:
        return "High"
    elif score >=30:
        return "Medium"
    else:
        return "Low"


def generate_reasons(row):
    reasons = []

    if is_missing(row["attendance_percentage"]):
        reasons.append("Attendance data is missing")
    elif row["attendance_percentage"] <75:
        reasons.append("Attendance is below 75%")
    elif row["attendance_percentage"] <90:
        reasons.append("Attendance is below 90%")

    if is_missing(row["assessment_score"]):
        reasons.append("Assessment data is missing")
    elif row["assessment_score"] <50:
        reasons.append("Assessment score is below 50%")
    elif row["assessment_score"] <70:
        reasons.append("Assessment score is below 70%")

    if is_missing(row["homework_completion"]):
        reasons.append("Homework data is missing")
    elif row["homework_completion"] <50:
        reasons.append("Homework completion is below 50%")
    elif row["homework_completion"] <75:
        reasons.append("Homework completion is below 75%")

    if is_missing(row["behaviour_points"]):
        reasons.append("Behaviour data is missing")
    elif row["behaviour_points"] > 4:
        reasons.append("Behaviour points are high")
    elif row["behaviour_points"] > 1:
        reasons.append("Behaviour points show some concern")

    if not reasons:
        reasons.append("No major risk factors currently identified")

    return reasons


def generate_recommendations(row):
    recommendations = []

    if row["risk_level"] == "Low":
        recommendations.append("Continue current teaching strategies")
        recommendations.append("Maintain regular monitoring")
        recommendations.append("Recognise and celebrate positive progress")
        return recommendations

    if is_missing(row["attendance_percentage"]):
        recommendations.append("Review or update attendance data")
    elif row["attendance_percentage"] <75:
        recommendations.append("Contact parent/carer about attendance")
        recommendations.append("Arrange an attendance review meeting")
    elif row["attendance_percentage"] <90:
        recommendations.append("Monitor attendance over the next two weeks")

    if is_missing(row["assessment_score"]):
        recommendations.append("Review or update assessment data")
    elif row["assessment_score"] <50:
        recommendations.append("Add student to targeted academic intervention")
        recommendations.append("Review recent assessment topics")
    elif row["assessment_score"] <70:
        recommendations.append("Provide additional revision resources")

    if is_missing(row["homework_completion"]):
        recommendations.append("Review or update homework data")
    elif row["homework_completion"] <50:
        recommendations.append("Set up homework support or check-ins")
    elif row["homework_completion"] <75:
        recommendations.append("Monitor homework completion")

    if is_missing(row["behaviour_points"]):
        recommendations.append("Review or update behaviour data")
    elif row["behaviour_points"] > 4:
        recommendations.append("Please refer to pastoral or behaviour support")
        recommendations.append("Review behaviour incidents with form tutor")
    elif row["behaviour_points"] > 1:
        recommendations.append("Monitor behaviour patterns")

    return recommendations