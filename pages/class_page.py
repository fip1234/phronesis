#imports
import streamlit as st
import pandas as pd
from style_loader import load_styles
from app_data import load_app_data

load_styles("class_Overview_styles.css")
st.title("Class Overview")
st.write("View student performance, risk information and recommended actions.")


##########STUDENT INSIGHTS##########
#give the information based on student data
def get_student_insights(student):
    insights =[]
    #attendance
    attendance =student["attendance_percentage"]

    #if no attendance or if low attendance then insight given
    if pd.isna(attendance):
        insights.append("No attendance data is currently available.")
    elif attendance <90:
        insights.append(f"Attendance is {attendance:.1f}%, which is low and may be affecting the student's learning.")
    elif attendance <95:
        insights.append(f"Attendance is {attendance:.1f}% and should continue to be monitored.")

    #assessment average
    grade_average =student["grade_average"]

    #if no grade average or if low grade average then insight given
    if pd.isna(grade_average):
        insights.append("There is not enough assessment data to calculate recent academic performance.")
    else:
        grade_percentage =grade_average *5
        ##convert grade avgto percentage
        if grade_percentage <50:
            insights.append(f"The student's recent assessment average is {grade_percentage:.1f}%, showing low academic performance.")
        elif grade_percentage <60:
            insights.append(f"The student's recent assessment average is {grade_percentage:.1f}% and should continue to be monitored.")

    ###assessment change
    grade_change =student["grade_change"]

    #no gradechange? - only give inisht if theres change
    if not pd.isna(grade_change):
        grade_change_percentage  =grade_change *5

        if grade_change_percentage <0:
            insights.append(f"Recent assessment performance has declined by approximately {abs(grade_change_percentage):.1f} percentage points.")

    ###previous failure
    previous_failure =student["prev_failure"]

    if not pd.isna(previous_failure) and previous_failure ==1:
        insights.append("The student has previously failed an assessment in this subject.")

    ###homework
    ###-not currently added homework upload feature, future addition will contain homework upload
    homework =student["homework_completion"]

    if pd.isna(homework):
        insights.append("No homework completion data is currently available.")
    elif homework <60:
        insights.append(f"Homework completion is currently {homework:.1f}%, which is a significant area of concern.")
    elif homework <80:
        insights.append(f"Homework completion is {homework:.1f}% and greater consistency would be beneficial.")

    ###behaviour
    ###-not currently added homework upload feature, future addition will contain homework upload
    behaviour =student["behaviour_incidents"]

    if pd.isna(behaviour):
        insights.append("No behaviour information is currently available.")
    elif behaviour >=4:
        insights.append(f"{int(behaviour)} behaviour incidents have been recorded, which may be affecting the student's learning.")
    elif behaviour >=2:
        insights.append(f"{int(behaviour)} behaviour incidents have been recorded and should continue to be monitored.")

    if len(insights) ==0:
        insights.append("No significant concerns have currently been identified from the available data.")

    return insights

##########RECOMMENDATIONS##########
#recommendations of next steps based on student data
#future improvements will be more personlised to eac student
def get_recommendations(student):
    recommendations =[]

    attendance =student["attendance_percentage"]

    ###attendance recommendations
    if not pd.isna(attendance):
        if attendance <90:
            recommendations.append("Discuss attendance with the student and parent/carer and identify any barriers affecting attendance.")
        elif attendance <95:
            recommendations.append("Monitor attendance regularly and encourage improved consistency.")

    grade_average =student["grade_average"]

    ###grade average recommendations
    if not pd.isna(grade_average):
        grade_percentage =grade_average *5

        if grade_percentage <50:
            recommendations.append("Provide targeted academic support in areas where the student is experiencing difficulty.")
        elif grade_percentage <60:
            recommendations.append("Review recent assessment work and provide focused revision support.")

    grade_change =student["grade_change"]

    ###grade change recommendations
    if not pd.isna(grade_change) and grade_change <0:
        recommendations.append("Review recent assessments to identify possible reasons for the decline in performance.")

    previous_failure =student["prev_failure"]

    ###previous failure recommendations
    if not pd.isna(previous_failure) and previous_failure ==1:
        recommendations.append("Review previously failed assessment topics and provide additional revision where needed.")

    homework =student["homework_completion"]

    ###homework recommendations
    if not pd.isna(homework):
        if homework <60:
            recommendations.append("Introduce a homework completion plan with regular check-ins.")
        elif homework <80:
            recommendations.append("Monitor homework completion and encourage a more consistent routine.")

    behaviour =student["behaviour_incidents"]

    ###behaviour recommendations
    if not pd.isna(behaviour):
        if behaviour >=4:
            recommendations.append("Review behaviour incidents and consider appropriate pastoral or classroom support.")
        elif behaviour >=2:
            recommendations.append("Monitor behaviour patterns and discuss recurring issues with the student.")

    ###insufficient data recommendations
    if student["prediction_status"] =="Insufficient data":
        recommendations.append("Collect additional assessment data before relying on an academic risk prediction.")

    if student["risk_prediction"] =="At Risk":
        recommendations.append("Review the student's progress again after an appropriate intervention period.")

    if len(recommendations) ==0:
        recommendations.append("Continue normal monitoring of the student's progress.")

    return recommendations


##########CREATE EMAIL##########
def create_parent_email(student_name,subject,class_name,risk_prediction,prediction_status,insights,recommendations):

    if prediction_status =="Insufficient data":
        risk_text ="There is currently not enough information available to generate a reliable academic risk prediction."
    elif risk_prediction =="At Risk":
        risk_text =f"Our current analysis suggests that {student_name} may benefit from additional support in {subject}."
    else:
        risk_text =f"{student_name} is not currently identified as academically at risk in {subject}, although their progress will continue to be monitored."

    #add in the insights and recommendations in email
    insight_text =""
    for insight in insights:
        insight_text +=f"- {insight}\n"

    recommendation_text =""
    for recommendation in recommendations:
        recommendation_text +=f"- {recommendation}\n"

#####actual email insert
    email =f"""Dear Parent/Carer,

I am writing to provide an update regarding {student_name}'s progress in {subject} ({class_name}).
{risk_text}
The information currently available highlights the following:
{insight_text}
Recommended next steps:
{recommendation_text}
We will continue to monitor {student_name}'s progress and provide support where appropriate.
Please feel free to contact me if you would like to discuss this further.
Kind regards,

[Teacher Name]"""

    return email

##########EMAIL POPUP##########

@st.dialog("Generated Parent Email")
def show_parent_email(student_name,subject,email):

    st.write("Please review and edit the email before using it.")

    #let user edit the email subject and body
    email_subject =st.text_input("Subject",value=f"Progress Update - {student_name} -{subject}")
    edited_email =st.text_area("Email",value=email,height=400)

    st.write("### Copy Email")
    st.code(f"Subject: {email_subject}\n\n{edited_email}",language=None)

#load application data
df =load_app_data()

##########FILTERS##########
#select class options- popup
with st.container(key="class_filters"):
    st.write("### Select Class")

    filterCol1,filterCol2,filterCol3 =st.columns(3)

    #fix!this filters by getting unique year group values-prevent multiple years in selections
    with filterCol1:
        year_groups =sorted(df["year_group"].dropna().unique())
        selected_year =st.selectbox("Year Group",year_groups)

    year_data =df[df["year_group"]==selected_year]

    with filterCol2:
        subjects =sorted(year_data["subject"].dropna().unique())
        selected_subject =st.selectbox("Subject",subjects)

    subject_data =year_data[year_data["subject"]==selected_subject]

    with filterCol3:
        class_names =sorted(subject_data["class_name"].dropna().unique())
        selected_class =st.selectbox("Class",class_names)

#so that only selected class data used
class_data =subject_data[subject_data["class_name"] ==selected_class].copy()

##########CLASS SUMMARY##########
student_count =len(class_data)
at_risk_count =(class_data["risk_prediction"] =="At Risk").sum()
ready_count =(class_data["prediction_status"] =="Ready").sum()
insufficient_count =(class_data["prediction_status"] =="Insufficient data").sum()

#risk perentage
if ready_count >0:
    at_risk_percentage =(at_risk_count /ready_count)*100
else:
    at_risk_percentage =0

average_attendance =class_data["attendance_percentage"].dropna().mean()

##########SUMMARY CARDS##########
#fix!new summary cards section
with st.container(key="class_summary"):
    st.write(f"## {selected_class}")
    st.write(f"{selected_subject} | Year {int(selected_year)}")

    #make 5 columns for summary cards
    col1,col2,col3,col4,col5 =st.columns(5)

    with col1:
        st.metric("Students",student_count)

    with col2:
        st.metric("At Risk",at_risk_count)

    with col3:
        #calculate ratio of at risk students to ready students
        st.metric("At Risk %",f"{at_risk_percentage:.1f}%")

    with col4:
        st.metric("Insufficient Data",insufficient_count)

    with col5:
        if pd.isna(average_attendance):
            st.metric("Average Attendance","No data")
        else:
            #mean attendance_percentage colomn
            st.metric("Average Attendance",f"{average_attendance:.1f}%")

##########STUDENT TABLE##########
#display students in table with specific risk highlighting
risk_order ={"At Risk":1,"Not At Risk":2,"Insufficient data":3}
class_data["risk_order"]  =class_data["risk_prediction"].map(risk_order)
class_data =class_data.sort_values(by=["risk_order","name"]). reset_index(drop=True)

student_table =class_data[["student_id","name","attendance_percentage","grade_average","grade_change","risk_prediction"]].copy()
student_table["grade_average"] =student_table["grade_average"]*5
student_table["grade_change"] =student_table["grade_change"]*5

student_table =student_table.rename(columns={
    "student_id":"Student ID",
    "name":"Student",
    "attendance_percentage":"Attendance %",
    "grade_average":"Assessment Average %",
    "grade_change":"Assessment Change %",
    "risk_prediction":"Risk"
})

#highlight students at risk, not at risk etc
def highlightRisk(row):
    if row["Risk"]=="At Risk":
        #red 
        return ["background-color:#FFF0EC"]*len(row)
    elif row["Risk"]=="Not At Risk":
        #green
        return ["background-color:#EAF7F5"]*len(row)
    elif row["Risk"]=="Insufficient data":
        #yellow
        return ["background-color:#FAF7F5"]*len(row)
    return [""]*len(row)

#add styling to each row(axis1)
styledStudentTable =student_table.style.apply(highlightRisk,axis=1)

#styled table in streamlit container
with st.container(key="class_students"):
    st.write("### Students")
    student_selection =st.dataframe(styledStudentTable,use_container_width= True,hide_index= True,
                                    on_select="rerun",selection_mode="single-row")

##########SELECT STUDENT##########
selected_rows  =student_selection.selection.rows
 
if len(selected_rows) ==0:
    st.info("Select a student from the table to view their details.")

else:
    selected_row =selected_rows[0]
    selected_student =class_data.iloc[selected_row]

    selected_student_id =selected_student["student_id"]
    selected_student_name =selected_student["name"]

    ##########STUDENT PROFILE##########
    #show each student's profile information
    with st.container(key="student_profile_header"):
        st.write("## Student Profile")
        st.write(f"### {selected_student_name}")
        st.write(
            f"**Student ID:** {selected_student_id} | "
            f"**Year Group:** {int(selected_student['year_group'])} | "
            f"**Class:** {selected_student['class_name']} | "
            f"**Subject:** {selected_student['subject']}"
        )

    ##########RISK##########
    #new container for student risk prediction
    with st.container(key="student_risk"):
        st.write("### Risk Prediction")

        #insufficient data warning
        if selected_student["prediction_status"]=="Insufficient data":
            st.warning("Insufficient data available to generate a risk prediction.")

        elif selected_student["risk_prediction"]=="At Risk":
            st.error("At Risk")

        else:
            st.success("Not At Risk")

    ##########INDICATORS##########
    #indicators-meaning quick overview of data
    with st.container(key="student_indicators"):
        st.write("### Student Indicators")
        #3 indicators per row
        col1,col2,col3 =st.columns(3)

        with col1:
            attendance =selected_student["attendance_percentage"]

            if pd.isna(attendance):
                st.metric("Attendance","No data")
            else:
                st.metric("Attendance",f"{attendance:.1f}%")

        with col2:
            grade_average =selected_student["grade_average"]

            if pd.isna(grade_average):
                st.metric("Assessment Average","No data")
            else:
                st.metric("Assessment Average",f"{grade_average *5:.1f}%")

        with col3:
            homework =selected_student["homework_completion"]

            if pd.isna(homework):
                st.metric("Homework Completion","No data")
            else:
                st.metric("Homework Completion",f"{homework:.1f}%")

        col4,col5,col6 =st.columns(3)

        with col4:
            absences =selected_student["absences"]

            if pd.isna(absences):
                st.metric("Absences","No data")
            else:
                st.metric("Absences",int(absences))

        with col5:
            grade_change =selected_student["grade_change"]

            if pd.isna(grade_change):
                st.metric("Assessment Change","No data")
            else:
                st.metric("Assessment Change",f"{grade_change *5:+.1f}%")

        with col6:
            behaviour =selected_student["behaviour_incidents"]

            if pd.isna(behaviour):
                st.metric("Behaviour Incidents","No data")
            else:
                st.metric("Behaviour Incidents",int(behaviour))


    ##########INSIGHTS AND RECOMMENDATIONS##########
    #edit- all in one nice clean look
    student_insights =get_student_insights(selected_student)
    student_recommendations =get_recommendations(selected_student)
    insightCol,recommendationCol =st.columns(2)

    with insightCol:
        with  st.container(key="student_insights"):
            st.write("### Insights")

            for insight in student_insights:
                st.write("| "+insight)

    with recommendationCol:
        with  st.container(key="student_recommendations"):
            st.write("### Recommended Next Steps")

            for recommendation in student_recommendations:
                st.write("| "+recommendation)


    ##########EMAIL##########
    with st.container(key="parent_communication"):
        st.write("### Parent Communication")
        st.write("Generate a draft progress email using the student's current information.")

        if st.button("Generate Parent Email",type="primary",key=f"email_{selected_student_id}_{selected_subject}"):
            parent_email =create_parent_email(
                selected_student_name,
                selected_subject,selected_class,
                selected_student["risk_prediction"],
                selected_student["prediction_status"],
                student_insights,student_recommendations
            )

            show_parent_email(selected_student_name,selected_subject,parent_email)

