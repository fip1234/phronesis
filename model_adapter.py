import pandas as pd


def process_assessments(assessment):

    #make copy so original data is not changed
    assessment= assessment.copy()

    #columns needed for assessment processing
    required_columns= [
        "student_id",
        "subject",
        "assessment_title",
        "assessment_date",
        "score",
        "max_score",
        "pass_mark"
    ]

    #check required columns exist
    missing_columns= [
        column for column in required_columns
        if column not in assessment.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing assessment columns: {missing_columns}"
        )

    #convert assessment numbers to numeric values
    assessment["score"]= pd.to_numeric(
        assessment["score"],
        errors="coerce"
    )

    assessment["max_score"]= pd.to_numeric(
        assessment["max_score"],
        errors="coerce"
    )

    assessment["pass_mark"]= pd.to_numeric(
        assessment["pass_mark"],
        errors="coerce"
    )

    #convert dates into proper dates
    assessment["assessment_date"]= pd.to_datetime(
        assessment["assessment_date"],
        errors="coerce"
    )

    #check whether each assessment record is valid
    assessment["valid_record"]= (
        assessment["student_id"].notna()
        & assessment["subject"].notna()
        & assessment["assessment_title"].notna()
        & assessment["assessment_date"].notna()
        & assessment["score"].notna()
        & assessment["max_score"].notna()
        & assessment["pass_mark"].notna()
        & (assessment["max_score"] > 0)
        & (assessment["score"] >= 0)
        & (assessment["score"] <= assessment["max_score"])
        & (assessment["pass_mark"] >= 0)
        & (assessment["pass_mark"] <= assessment["max_score"])
    )

    #convert valid assessment results onto 0-20 scale
    assessment["model_grade"]= pd.NA

    assessment.loc[
        assessment["valid_record"],
        "model_grade"
    ]= (
        assessment.loc[
            assessment["valid_record"],
            "score"
        ]
        /
        assessment.loc[
            assessment["valid_record"],
            "max_score"
        ]
    ) * 20

    #store calculated features for each student
    assessment_features= []

    #only rows with student and subject can be grouped
    assessment_groups= assessment.dropna(
        subset=["student_id","subject"]
    )

    #process each student separately for each subject
    for (student_id,subject), student_assessments in assessment_groups.groupby(
        ["student_id","subject"]
    ):

        #only use valid assessments
        valid_assessments= student_assessments[
            student_assessments["valid_record"]
        ].copy()

        #put assessments in date order
        valid_assessments= valid_assessments.sort_values(
            by="assessment_date"
        )

        #need at least two assessments
        if len(valid_assessments) < 2:

            assessment_features.append({
                "student_id":student_id,
                "subject":subject,
                "prev_failure":pd.NA,
                "grade_average":pd.NA,
                "grade_change":pd.NA,
                "assessment_status":"Insufficient data"
            })

            continue

        #get latest two assessments
        latest_two= valid_assessments.tail(2)

        #average of latest two model grades
        grade_average= latest_two[
            "model_grade"
        ].astype(float).mean()

        #latest grade minus previous grade
        grade_change= (
            float(latest_two["model_grade"].iloc[-1])
            -
            float(latest_two["model_grade"].iloc[-2])
        )

        #all assessments before the latest assessment
        previous_assessments= valid_assessments.iloc[:-1]

        #check whether student previously failed
        prev_failure= int(
            (
                previous_assessments["score"]
                <
                previous_assessments["pass_mark"]
            ).any()
        )

        assessment_features.append({
            "student_id":student_id,
            "subject":subject,
            "prev_failure":prev_failure,
            "grade_average":grade_average,
            "grade_change":grade_change,
            "assessment_status":"Valid"
        })

    #turn calculated results into dataframe
    assessment_features= pd.DataFrame(
        assessment_features
    )

    return assessment_features