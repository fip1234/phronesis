import pandas as pd

def validate_attendance_data(attendance):
    #make copy so original data not changed
    attendance= attendance.copy()

    #columns needed for attendance processing
    required_columns= ["student_id", "total_sessions", "sessions_attended"]
    #check required columns exist- if not add to missing columns list
    missing_columns = []

    for column in required_columns:
        if column not in attendance.columns:
            missing_columns.append(column)

    if missing_columns:
        raise ValueError(f"Missing attendance columns: {missing_columns}")

    #convert attendance numbers to numeric values
    #coerce- turn invalid values into NaN
    attendance["total_sessions"]= pd.to_numeric(attendance["total_sessions"],errors="coerce")
    attendance["sessions_attended"]= pd.to_numeric(attendance["sessions_attended"],errors="coerce")

    #check all required values are present
    complete_record = attendance[required_columns].notna().all(axis=1)

    #check values are within valid ranges
    valid_sessions = (
        (attendance["total_sessions"] >0)
        & (attendance["sessions_attended"] >=0)
        & (attendance["sessions_attended"] <=attendance["total_sessions"])
    )

    #valid record-has all required values and valid sesion values
    attendance["valid_record"] = (complete_record & valid_sessions)

    return attendance





################Process attendance data- normal#####################
def process_attendances(attendance):

    #validate attendance data first
    attendance = validate_attendance_data(attendance)

    #create empty columns for soon calculated values
    attendance["absences"] =pd.NA
    attendance["attendance_percentage"] =pd.NA

    valid_rows = attendance["valid_record"]

    #calculate absences for valid rows
    #find the valid rows, calculate total absence by subtracting sessions attended from total sessions
    attendance.loc[valid_rows, "absences"] =(
        attendance.loc[valid_rows, "total_sessions"] - 
        attendance.loc[valid_rows, "sessions_attended"]
    )

    #calculate attendance percentage for valid rows
    #find the valid rows, calculate attendance percentage by dividing sessions attended by total sessions and *100
    attendance.loc[valid_rows, "attendance_percentage"] =(
        (attendance.loc[valid_rows, "sessions_attended"] / 
         attendance.loc[valid_rows, "total_sessions"]) * 100
    )

    #start each record with a default-insufficient data
    attendance["attendance_status"] = "Insufficient data"

    #valid rows- set attendance status to valid
    attendance.loc[valid_rows, "attendance_status"] = "Valid"

    #only keep values needed later
    attendance_features = attendance[["student_id","absences","attendance_percentage","attendance_status"]].copy()

    return attendance_features