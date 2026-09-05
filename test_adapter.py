#imports
import pandas as pd
from model_adapter import process_assessments
from model_adapter import validate_assessment_data

#read in assessment data
assessment= pd.read_csv("data/new/assessment.csv")

#generate assessment features
assessment_features= process_assessments(assessment)

print(assessment_features)

##########Test#########
#read test data
test_assessment = pd.read_csv("data/new/assessment_test.csv")

#validate test data
validation_results = validate_assessment_data(test_assessment)

#check if expected result matches actual result
validation_results["test_passed"] =(validation_results["expected_valid"]==validation_results["valid_record"])

print("\nASSESSMENT VALIDATION TESTS:")
print(validation_results[["test_case","expected_valid","valid_record","test_passed"]])