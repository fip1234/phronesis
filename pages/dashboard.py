#imports
import streamlit as st
import pandas as pd

from app_data import load_app_data


st.title("Dashboard")
st.write("Overview of your classes and students requiring attention.")


##########LOAD DATA##########

df =load_app_data()

#test fix!-no teacher data uploaded yet
if len(df) ==0:
    st.info(
        "No student data has been added yet. "
        "Go to Data Management to add your subjects, classes and students."
    )
    st.stop()
    
dashboard_data =df.copy()

#make numeric columns safe
dashboard_data["attendance_percentage"] =pd.to_numeric(dashboard_data["attendance_percentage"],errors="coerce")
dashboard_data["grade_average"] =pd.to_numeric(dashboard_data["grade_average"],errors="coerce")
dashboard_data["grade_change"] =pd.to_numeric(dashboard_data["grade_change"],errors="coerce")
dashboard_data["model_score"] =pd.to_numeric(dashboard_data["model_score"],errors="coerce")
dashboard_data["homework_completion"] =pd.to_numeric(dashboard_data["homework_completion"],errors="coerce")
dashboard_data["behaviour_incidents"] =pd.to_numeric(dashboard_data["behaviour_incidents"],errors="coerce")

#teacher-friendly assessment percentage
dashboard_data["assessment_percentage"] =dashboard_data["grade_average"] *5


##########SUMMARY##########

total_students =dashboard_data["student_id"].nunique()
total_classes =dashboard_data["class_id"].nunique()

at_risk_students =dashboard_data[
    dashboard_data["risk_prediction"] =="At Risk"
]["student_id"].nunique()

classes_with_risk =dashboard_data[
    dashboard_data["risk_prediction"] =="At Risk"
]["class_id"].nunique()

col1,col2,col3,col4 =st.columns(4)

with col1:
    st.metric("My Classes",total_classes)

with col2:
    st.metric("Students",total_students)

with col3:
    st.metric("Students At Risk",at_risk_students)

with col4:
    st.metric("Classes With Risk",classes_with_risk)


##########STUDENTS REQUIRING ATTENTION##########

st.write("## Students Requiring Attention")

attention_data =dashboard_data[
    dashboard_data["risk_prediction"] =="At Risk"
].copy()

#highest model score first
attention_data =attention_data.sort_values(
    by=["model_score","attendance_percentage"],
    ascending=[False,True]
)

attention_table =attention_data[
    [
        "student_id",
        "name",
        "class_name",
        "subject",
        "attendance_percentage",
        "assessment_percentage",
        "risk_prediction"
    ]
].head(10)

attention_table =attention_table.rename(columns={
    "student_id":"Student ID",
    "name":"Student",
    "class_name":"Class",
    "subject":"Subject",
    "attendance_percentage":"Attendance %",
    "assessment_percentage":"Assessment Average %",
    "risk_prediction":"Risk"
})

if len(attention_table) ==0:
    st.success("No students are currently identified as At Risk.")
else:
    st.dataframe(attention_table,use_container_width=True,hide_index=True)


##########QUICK INSIGHTS##########

st.write("## Quick Insights")

#attendance concern
attendance_concerns =dashboard_data[
    dashboard_data["attendance_percentage"] <95
]["student_id"].nunique()

#academic concern
academic_concerns =dashboard_data[
    dashboard_data["assessment_percentage"] <50
]["student_id"].nunique()

#homework concern
homework_concerns =dashboard_data[
    dashboard_data["homework_completion"] <80
]["student_id"].nunique()

#behaviour concern
behaviour_concerns =dashboard_data[
    dashboard_data["behaviour_incidents"] >=2
]["student_id"].nunique()

col1,col2,col3,col4 =st.columns(4)

with col1:
    st.metric("Attendance Concerns",attendance_concerns)

with col2:
    st.metric("Academic Concerns",academic_concerns)

with col3:
    if dashboard_data["homework_completion"].notna().any():
        st.metric("Homework Concerns",homework_concerns)
    else:
        st.metric("Homework Concerns","No data")

with col4:
    if dashboard_data["behaviour_incidents"].notna().any():
        st.metric("Behaviour Concerns",behaviour_concerns)
    else:
        st.metric("Behaviour Concerns","No data")


##########CLASS SUMMARY DATA##########

#create flags for class calculations
dashboard_data["at_risk_flag"] =(dashboard_data["risk_prediction"] =="At Risk").astype(int)
dashboard_data["ready_flag"] =(dashboard_data["prediction_status"] =="Ready").astype(int)
dashboard_data["insufficient_flag"] =(dashboard_data["prediction_status"] =="Insufficient data").astype(int)

class_summary =dashboard_data.groupby(
    ["class_id","class_name","subject","year_group"],
    as_index=False
).agg({
    "student_id":"nunique",
    "at_risk_flag":"sum",
    "ready_flag":"sum",
    "insufficient_flag":"sum",
    "attendance_percentage":"mean",
    "assessment_percentage":"mean"
})

class_summary =class_summary.rename(columns={
    "student_id":"students",
    "at_risk_flag":"at_risk",
    "ready_flag":"ready",
    "insufficient_flag":"insufficient",
    "attendance_percentage":"average_attendance",
    "assessment_percentage":"average_assessment"
})

#calculate class risk percentage
class_summary["at_risk_percentage"] =0.0

has_predictions =class_summary["ready"] >0

class_summary.loc[has_predictions,"at_risk_percentage"] =(
    class_summary.loc[has_predictions,"at_risk"]
    /
    class_summary.loc[has_predictions,"ready"]
)*100


##########KEY INSIGHTS##########

st.write("## Key Insights")

if len(class_summary) >0:

    #class with highest risk percentage
    highest_risk =class_summary.sort_values(
        by="at_risk_percentage",
        ascending=False
    ).iloc[0]

    #class with lowest attendance
    attendance_classes =class_summary.dropna(subset=["average_attendance"])

    st.warning(
        f"{highest_risk['class_name']} currently has the highest proportion "
        f"of At Risk predictions at {highest_risk['at_risk_percentage']:.1f}%."
    )

    if len(attendance_classes) >0:
        lowest_attendance =attendance_classes.sort_values(
            by="average_attendance"
        ).iloc[0]

        st.info(
            f"{lowest_attendance['class_name']} currently has the lowest average "
            f"attendance at {lowest_attendance['average_attendance']:.1f}%."
        )

    if at_risk_students >0:
        st.write(
            f"**{at_risk_students} students** have been identified as At Risk "
            f"across **{classes_with_risk} classes** and may require further review."
        )
    else:
        st.write("No students currently require priority academic intervention.")


##########MY CLASSES##########

st.write("## My Classes")

#filters
filter1,filter2 =st.columns(2)

with filter1:
    year_options =["All"] +sorted(class_summary["year_group"].dropna().unique().tolist())
    selected_year =st.selectbox("Year Group",year_options)

with filter2:
    subject_options =["All"] +sorted(class_summary["subject"].dropna().unique().tolist())
    selected_subject =st.selectbox("Subject",subject_options)

filtered_classes =class_summary.copy()

if selected_year !="All":
    filtered_classes =filtered_classes[
        filtered_classes["year_group"] ==selected_year
    ]

if selected_subject !="All":
    filtered_classes =filtered_classes[
        filtered_classes["subject"] ==selected_subject
    ]

class_table =filtered_classes[
    [
        "class_name",
        "subject",
        "year_group",
        "students",
        "at_risk",
        "at_risk_percentage",
        "insufficient",
        "average_attendance",
        "average_assessment"
    ]
].copy()

class_table =class_table.rename(columns={
    "class_name":"Class",
    "subject":"Subject",
    "year_group":"Year",
    "students":"Students",
    "at_risk":"At Risk",
    "at_risk_percentage":"At Risk %",
    "insufficient":"Insufficient Data",
    "average_attendance":"Average Attendance %",
    "average_assessment":"Average Assessment %"
})

class_table =class_table.sort_values(
    by="At Risk %",
    ascending=False
)

st.dataframe(class_table,use_container_width=True,hide_index=True)


##########GRAPHS##########

st.write("## Class Overview Charts")

graph1,graph2 =st.columns(2)


##########RISK GRAPH##########

with graph1:

    st.write("### Classes With Highest Risk")

    risk_chart =filtered_classes.sort_values(
        by="at_risk_percentage",
        ascending=False
    ).head(10)

    risk_chart =risk_chart[
        ["class_name","at_risk_percentage"]
    ].set_index("class_name")

    st.bar_chart(risk_chart)


##########ATTENDANCE GRAPH##########

with graph2:

    st.write("### Classes With Lowest Attendance")

    attendance_chart =filtered_classes.dropna(
        subset=["average_attendance"]
    ).sort_values(
        by="average_attendance"
    ).head(10)

    attendance_chart =attendance_chart[
        ["class_name","average_attendance"]
    ].set_index("class_name")

    st.bar_chart(attendance_chart)