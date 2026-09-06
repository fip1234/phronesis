import streamlit as st
from app_data import load_app_data


def show_student_page(df):

    st.header("Students")


    ##########Student table##########

    st.subheader("Student Overview")

    #copy data so original dataframe not changed
    display_df = df.copy()

    #make missing subject clearer
    display_df["subject"] = (
        display_df["subject"]
        .fillna("No assessment data")
    )

    #set order for risk results
    risk_order = {
        "At Risk": 1,
        "Not At Risk": 2,
        "Insufficient data": 3
    }

    #temporary column used for sorting
    display_df["sort_order"] = (
        display_df["risk_prediction"]
        .map(risk_order)
    )

    #sort at risk students first
    display_df = display_df.sort_values(
        by="sort_order"
    )

    #only display useful teacher information
    display_df = display_df[
        [
            "student_id",
            "name",
            "subject",
            "attendance_percentage",
            "prediction_status",
            "risk_prediction"
        ]
    ]

    #replace remaining missing values
    display_df = display_df.fillna(
        "Data Missing"
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )


    ##########Select student##########

    st.markdown("---")

    st.subheader("Student Insights")

    #get one row for each student
    student_list = df[
        ["student_id", "name"]
    ].drop_duplicates()

    #create display option for dropdown
    student_list["student_option"] = (
        student_list["name"]
        + " - "
        + student_list["student_id"]
    )

    #choose student
    selected_student = st.selectbox(
        "Choose a student",
        student_list["student_option"]
    )

    #get selected student id
    selected_student_id = student_list[
        student_list["student_option"] == selected_student
    ]["student_id"].iloc[0]


    ##########Selected student##########

    #get all rows for selected student
    student_data = df[
        df["student_id"] == selected_student_id
    ]

    #get student name
    selected_student_name = student_data[
        "name"
    ].iloc[0]

    st.markdown("---")

    st.header(selected_student_name)

    st.write(
        f"Student ID: {selected_student_id}"
    )


    ##########Subject##########

    #get available subjects
    subjects = student_data[
        "subject"
    ].dropna().unique()

    if len(subjects) > 0:

        selected_subject = st.selectbox(
            "Choose a subject",
            subjects
        )

        #get selected subject row
        student_row = student_data[
            student_data["subject"] == selected_subject
        ].iloc[0]

    else:

        #student has no assessment subject data
        student_row = student_data.iloc[0]

        st.warning(
            "No assessment data available for this student."
        )


    ##########Prediction result##########

    st.write("### Risk Prediction")

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


#load final app data
df = load_app_data()

#show student page
show_student_page(df)