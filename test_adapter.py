#imports
import pandas as pd
from assessment_adapter import process_assessments
from assessment_adapter import validate_assessment_data
from attendance_adapter import process_attendances
from attendance_adapter import validate_attendance_data
from model_adapter import merge_model_features
from model_adapter import risk_predict

##########Assessment##########
#read in assessment data
assessment = pd.read_csv("data/new/assessment.csv")

#generate assessment features
assessment_features = process_assessments(assessment)

print("\nASSESSMENT FEATURES:")
print(assessment_features)

##########Assessment Test##########
#read assessment test data
test_assessment = pd.read_csv("data/new/tests/assessment_test.csv")

#validate test data
assessment_validation_results = validate_assessment_data(test_assessment)

#check if expected result matches actual result
assessment_validation_results["test_passed"] =(assessment_validation_results["expected_valid"]==assessment_validation_results["valid_record"])

print("\nASSESSMENT VALIDATION TESTS:")
print(assessment_validation_results[["test_case","expected_valid","valid_record","test_passed"]])

##########Attendance##########
#read in attendance data
attendance = pd.read_csv("data/new/attendance.csv")

#generate attendance features
attendance_features = process_attendances(attendance)

print("\nATTENDANCE FEATURES:")
print(attendance_features)

##########Attendance Test##########
#read attendance test data
test_attendance = pd.read_csv("data/new/tests/attendance_test.csv")

#validate attendance test data
attendance_validation_results = validate_attendance_data(test_attendance)

#check expected result matches actual result
attendance_validation_results["test_passed"] =(attendance_validation_results["expected_valid"]==attendance_validation_results["valid_record"])

print("\nATTENDANCE VALIDATION TESTS:")
print(attendance_validation_results[["test_case","expected_valid","valid_record","test_passed"]])


##########Students##########
#read student list
students = pd.read_csv("data/new/students.csv")

##########Model Merge Tests##########

test_students = pd.read_csv("data/new/merge_tests/merge_test_students.csv")
test_assessment_features = pd.read_csv("data/new/merge_tests/merge_test_assessment.csv")
test_attendance_features = pd.read_csv("data/new/merge_tests/merge_test_attendance.csv")
test_merged = merge_model_features(test_students,test_assessment_features,test_attendance_features)

print("\nMODEL MERGE TEST DATA:")

print(test_merged[["student_id","subject","prev_failure","absences","grade_average","grade_change","prediction_status"]])


##########Model##########
#merge assessment and attendance features
merged_features = merge_model_features(students,assessment_features, attendance_features)

print("\nCOMBINED MODEL FEATURES:")
print(merged_features[["student_id","subject","prev_failure","absences","grade_average","grade_change","prediction_status"]])


##########Random Forest Prediction##########
#generate risk predictions
prediction_results = risk_predict(merged_features)

print("\nRANDOM FOREST PREDICTIONS:")
print(prediction_results[["student_id","subject","prediction_status","risk_prediction"]])

##########Random Forest Prediction Tests##########
#read expected prediction results
prediction_test = pd.read_csv("data/new/tests/prediction_test.csv")
#attach actual results to expected results
prediction_test_results = prediction_test.merge(
    prediction_results[["student_id","prediction_status","risk_prediction"]],on="student_id",how="left")

#check prediction status
prediction_test_results["status_test_passed"] =(
    prediction_test_results["expected_status"]
    ==
    prediction_test_results["prediction_status"]
)

#check risk prediction
prediction_test_results["prediction_test_passed"] =(
    prediction_test_results["expected_prediction"]
    ==
    prediction_test_results["risk_prediction"]
)

print("\nRANDOM FOREST PREDICTION TESTS:")
print(prediction_test_results[["student_id","expected_status", "prediction_status", "status_test_passed", "expected_prediction", "risk_prediction","prediction_test_passed"]])

