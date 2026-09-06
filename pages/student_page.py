import streamlit as st


def show_student_page(df):

    st.header("Student Risk Details")

    #choose student
    selected_student = st.selectbox(
        "Choose a student",
        df["name"].drop_duplicates()
    )

    #get all rows for selected student
    student_data = df[
        df["name"] == selected_student
    ]

    #if student has subject data
    subjects = student_data["subject"].dropna().unique()

    if len(subjects) > 0:

        #choose subject
        selected_subject = st.selectbox(
            "Choose a subject",
            subjects
        )

        #get selected student and subject row
        student_row = student_data[
            student_data["subject"] == selected_subject
        ].iloc[0]

    else:

        #student has no assessment subject data
        student_row = student_data.iloc[0]


    st.subheader(selected_student)


    ##########Prediction result##########

    if student_row["prediction_status"] == "Insufficient data":

        st.warning(
            "Insufficient data for risk prediction"
        )

    elif student_row["risk_prediction"] == "At Risk":

        st.error(
            "At Risk"
        )

    else:

        st.success(
            "Not At Risk"
        )


    ##########Supporting information##########

    st.write("### Student Indicators")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Attendance:**",
            student_row["attendance_percentage"]
        )

        st.write(
            "**Absences:**",
            student_row["absences"]
        )

    with col2:

        st.write(
            "**Grade Average:**",
            student_row["grade_average"]
        )

        st.write(
            "**Grade Change:**",
            student_row["grade_change"]
        )

        st.write(
            "**Previous Failure:**",
            student_row["prev_failure"]
        )