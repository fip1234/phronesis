import pandas as pd

def validate_assessment_data(assessment):
    #make copy so original data not changed
    assessment= assessment.copy()

    #columns needed for assessment processing
    required_columns= ["student_id","subject","assessment_title","assessment_date","score","max_score","pass_mark"]

    #check required columns exist- if not add to missing columns list
    missing_columns = []

    for column in required_columns:
        if column not in assessment.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(f"Missing assessment columns: {missing_columns}")

    #convert assessment numbers to numeric values
    #coerce- turn invalid values into NaN
    assessment["score"]= pd.to_numeric(assessment["score"],errors="coerce")
    assessment["max_score"]= pd.to_numeric(assessment["max_score"],errors="coerce")
    assessment["pass_mark"]= pd.to_numeric(assessment["pass_mark"],errors="coerce")

    #convert dates into proper dates
    assessment["assessment_date"]= pd.to_datetime(assessment["assessment_date"],errors="coerce")
    #check if date is not in future
    valid_date=(assessment["assessment_date"]<= pd.Timestamp.today())

    #check all required values are present
    complete_record = assessment[required_columns].notna().all(axis=1)

    #check values are within valid ranges
    valid_scores = (
        (assessment["max_score"] >0)
        & (assessment["score"] >=0)
        & (assessment["score"] <=assessment["max_score"])
        & (assessment["pass_mark"] >=0)
        & (assessment["pass_mark"] <=assessment["max_score"])
    )

    #valid record-has all required values and valid scores
    assessment["valid_record"] = (complete_record & valid_scores & valid_date)

    return assessment





################Process assessment data- normal#####################
def process_assessments(assessment):
    #validate assessment data first
    assessment = validate_assessment_data(assessment)

    #convert valid assessmentresults onto 0-20 scale
    assessment["model_grade"]= pd.NA

    valid_rows = assessment["valid_record"]

    #calculate model grade for valid rows
    #find the valid rows, take score,divide by max score, multiply by 20 save the result in model_grade
    assessment.loc[valid_rows, "model_grade"]=(
        assessment.loc[valid_rows,"score"]
        /
        assessment.loc[valid_rows,"max_score"]
    )*20

    #store calculated features for each student
    assessment_features= []

    #only rows with student and subject can be grouped
    assessment_groups= assessment.dropna(subset=["student_id","subject"])

    ############process each student separately for each subject##############
    #go through each student
    for student_id in assessment_groups["student_id"].unique():
        #get all data for that student
        student_data=assessment_groups[assessment_groups["student_id"] ==student_id]

        #go through each subject for that student
        for subject in student_data["subject"].unique():
            #get all data for that student and subject
            subject_data = student_data[student_data["subject"] ==subject].copy() 

            #only keep valid assessments
            valid_assessments = subject_data[subject_data["valid_record"]].copy() 

            #put assessments in dates order
            valid_assessments = valid_assessments.sort_values("assessment_date")

            #if less than 2 valid assessments, cant calculate features
            if len(valid_assessments)<2:
                assessment_features.append({
                    "student_id": student_id,
                    "subject": subject,
                    "prev_failure": pd.NA,
                    "grade_average": pd.NA,
                    "grade_change": pd.NA,
                    "assessment_status": "Insufficient data"
                })
                continue

            
            #get latest two assessments
            latest_two =valid_assessments.tail(2)

            previous_grade =float(latest_two["model_grade"].iloc[0])
            latest_grade =float(latest_two["model_grade"].iloc[1])

            #average grade
            grade_average =(previous_grade +latest_grade)/2

            #grade change
            grade_change = latest_grade -previous_grade

            #get all assessments before latest one
            previous_assessments = valid_assessments.iloc[:-1]

            #check if failed any previous assessments-score less than pass mark
            failed_before =(previous_assessments["score"]< previous_assessments["pass_mark"]).any()

            if failed_before:
                prev_failure =1
            else:
                prev_failure =0

            #store calculated features
            assessment_features.append({
                "student_id": student_id,
                "subject": subject,
                "prev_failure": prev_failure,
                "grade_average": grade_average,
                "grade_change": grade_change,
                "assessment_status": "Valid"
            })


    #turn results into a dataframe
    assessment_features = pd.DataFrame(assessment_features)

    return assessment_features
