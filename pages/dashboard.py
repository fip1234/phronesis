#dashboard.py- main page for generalised insights on all classes
#imports
import streamlit as st
import pandas as pd
import altair as alt
from app_data import load_app_data
from style_loader import load_styles

load_styles("dashboard_styles.css")
st.title("Dashboard")
st.write("Overview of your classes and students requiring attention.")

##########LOAD DATA##########
df =load_app_data()

#test fix!-no teacher data uploaded yet
if len(df) ==0:
    st.info("No student data has been added yet. Go to Data Management to add your subjects, classes and students.")
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

##########SUMMARY DATA##########
total_students =dashboard_data["student_id"].nunique()
total_classes =dashboard_data["class_id"].nunique()
#nuinque- only count unique students and classes at risk
at_risk_students =dashboard_data[dashboard_data["risk_prediction"]=="At Risk"]["student_id"].nunique()
classes_with_risk =dashboard_data[dashboard_data["risk_prediction"]=="At Risk"]["class_id"].nunique()

##########SUMMARY##########
with st.container(key="dashboard_summary"):
    col1,col2,col3,col4 =st.columns(4)

    with col1:
        with st.container(key="metric_classes"):
            st.metric("My Classes",total_classes)
    with col2:
        with st.container(key="metric_students"):
            st.metric("Students",total_students)
    with col3:
        with st.container(key="metric_risk"):
            st.metric("Students At Risk",at_risk_students)
    with col4:
        with st.container(key="metric_classes_risk"):
            st.metric("Classes With Risk",classes_with_risk)

##########ATTENTION DATA##########
#filter data so only at risk students display
attention_data =dashboard_data[dashboard_data["risk_prediction"]=="At Risk"].copy()
attention_data =attention_data.sort_values(by=["model_score","attendance_percentage"],ascending=[False,True])

attention_table =attention_data[["student_id","name","class_name","subject","attendance_percentage","assessment_percentage","risk_prediction"]].head(10)

attention_table =attention_table.rename(columns={
    "student_id":"Student ID",
    "name":"Student",
    "class_name":"Class",
    "subject":"Subject",
    "attendance_percentage":"Attendance %",
    "assessment_percentage":"Assessment Average %",
    "risk_prediction":"Risk"
})

#highlight rows based on risk level
def highlightAttention(row):
    #light red
    return ["background-color:#FFF0EC"]*len(row)

styledAttentionTable =attention_table.style.apply(highlightAttention,axis=1)

##########QUICK INSIGHT DATA##########
attendance_concerns =dashboard_data[dashboard_data["attendance_percentage"]<95]["student_id"].nunique()
academic_concerns =dashboard_data[dashboard_data["assessment_percentage"]<50]["student_id"].nunique()
homework_concerns =dashboard_data[dashboard_data["homework_completion"]<80]["student_id"].nunique()
behaviour_concerns =dashboard_data[dashboard_data["behaviour_incidents"]>=2]["student_id"].nunique()

##########MAIN DASHBOARD ROW############
attentionCol,insightCol =st.columns([2.2,1])

with attentionCol:
    with st.container(key="attention_section"):
        st.write("### Students Requiring Attention")

        if len(attention_table)==0:
            st.success("No students are currently identified as At Risk.")
        else:
            #display styled attention table
            st.dataframe(
                styledAttentionTable,  use_container_width=True,hide_index=True, height=210,
                column_config={
                    "Student ID":st.column_config.TextColumn("ID"),
                    "Student":st.column_config.TextColumn("Student"),
                    "Class":st.column_config.TextColumn("Class"),
                    "Subject":st.column_config.TextColumn("Subject"),
                    "Attendance %":st.column_config.NumberColumn("Attendance",format="%.1f%%"),
                    "Assessment Average %":st.column_config.NumberColumn("Assessment",format="%.1f%%"),
                    "Risk":st.column_config.TextColumn("Risk")
                }
            )

with insightCol:
    #quick basic key insights for all categories
    with st.container(key="quick_insights"):
        st.write("### Quick Insights")

        row1Col1,row1Col2 =st.columns(2)
        with row1Col1:
            with st.container(key="metric_attendance"):
                st.metric("Attendance",attendance_concerns)
        with row1Col2:
            with st.container(key="metric_academic"):
                st.metric("Academic",academic_concerns)

        row2Col1,row2Col2 =st.columns(2)
        with row2Col1:
            with st.container(key="metric_homework"):
                if dashboard_data["homework_completion"].notna().any():
                    st.metric("Homework",homework_concerns)
                else:
                    st.metric("Homework","No data")
        with row2Col2:
            with st.container(key="metric_behaviour"):
                if dashboard_data["behaviour_incidents"].notna().any():
                    st.metric("Behaviour",behaviour_concerns)
                else:
                    st.metric("Behaviour","No data")

##########CLASS SUMMARY DATA##########
dashboard_data["at_risk_flag"] =(dashboard_data["risk_prediction"] =="At Risk").astype(int)
dashboard_data["ready_flag"] =(dashboard_data["prediction_status"] =="Ready").astype(int)
dashboard_data["insufficient_flag"] =(dashboard_data["prediction_status"] =="Insufficient data").astype(int)

#agg- aggregate (group by) class summary data
class_summary =dashboard_data.groupby(["class_id","class_name","subject","year_group"],as_index=False).agg({
    "student_id":"nunique",
    "at_risk_flag":"sum",
    "ready_flag":"sum",
    "insufficient_flag":"sum",
    "attendance_percentage":"mean",
    "assessment_percentage":"mean"
})

#rename columns just to be clear
class_summary =class_summary.rename(columns={
    "student_id":"students",
    "at_risk_flag":"at_risk",
    "ready_flag":"ready",
    "insufficient_flag":"insufficient",
    "attendance_percentage":"average_attendance",
    "assessment_percentage":"average_assessment"
})

class_summary["at_risk_percentage"] =0.0
has_predictions =class_summary["ready"] >0
class_summary.loc[has_predictions,"at_risk_percentage"] =(class_summary.loc[has_predictions,"at_risk"]/class_summary.loc[has_predictions,"ready"])*100

##########KEY INSIGHTS##########
#highest risk class and lowest attendance class- all their data
with st.container(key="key_insights"):
    if len(class_summary)>0:
        highest_risk =class_summary.sort_values(by="at_risk_percentage",ascending=False).iloc[0]
        attendance_classes =class_summary.dropna(subset=["average_attendance"])

        insight1,insight2 =st.columns(2)

        with insight1:
            st.write(f"**Highest Risk:** {highest_risk['class_name']} ({highest_risk['at_risk_percentage']:.1f}%)")

        with insight2:
            if len(attendance_classes)>0:
                lowest_attendance =attendance_classes.sort_values(by="average_attendance").iloc[0]
                st.write(f"**Lowest Attendance:** {lowest_attendance['class_name']} ({lowest_attendance['average_attendance']:.1f}%)")

##########MY CLASSES DATA########
year_options =["All"]+sorted(class_summary["year_group"].dropna().unique().tolist())
subject_options =["All"]+sorted(class_summary["subject"].dropna().unique().tolist())

##########LOWER DASHBOARD############
classCol,chartCol =st.columns([1.35,1])

with classCol:
    #display my classes section
    with st.container(key="my_classes"):
        st.write("### My Classes")

        #filter selection bar for year group and subject
        #only display those students
        filter1,filter2 =st.columns(2)
        with filter1:
            selected_year =st.selectbox("Year Group",year_options,key="dashboard_year")
        with filter2:
            selected_subject =st.selectbox("Subject",subject_options,key="dashboard_subject")

        filtered_classes =class_summary.copy()

        if selected_year!="All":
            filtered_classes =filtered_classes[filtered_classes["year_group"]==selected_year]

        if selected_subject!="All":
            filtered_classes =filtered_classes[filtered_classes["subject"]==selected_subject]

        class_table =filtered_classes[["class_name","subject","year_group","students","at_risk","at_risk_percentage","insufficient","average_attendance","average_assessment"]].copy()

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

        class_table =class_table.sort_values(by="At Risk %",ascending=False)

        #add progress column- visually represent percentages as bars
        st.dataframe(
            class_table,  use_container_width=True, hide_index=True,height=250, column_config={
                "At Risk %":st.column_config.ProgressColumn("Risk %",min_value=0,max_value=100,format="%.1f%%"),
                "Average Attendance %":st.column_config.ProgressColumn("Attendance",min_value=0,max_value=100,format="%.1f%%"),
                "Average Assessment %":st.column_config.ProgressColumn("Assessment",min_value=0,max_value=100,format="%.1f%%")
            }
        )

with chartCol:
    #prediction breakdown chart-round
    with st.container(key="risk_chart"):
        st.write("### Prediction Breakdown")

        prediction_data =dashboard_data[["student_id","subject","risk_prediction"]].drop_duplicates()
        prediction_data["risk_prediction"] =prediction_data["risk_prediction"].fillna("Insufficient data")

        prediction_counts =prediction_data["risk_prediction"].value_counts().reset_index()
        prediction_counts.columns =["Risk","Students"]

        #donut chart
        donut =alt.Chart(prediction_counts).mark_arc(innerRadius=60,outerRadius=95).encode(
            #angle for size of each segment
            theta=alt.Theta(field="Students",type="quantitative"),
            #red, green, gray for different risk levels. not risk=green, at risk=red, insufficient data=gray
            color=alt.Color("Risk:N",
                scale=alt.Scale(domain=["At Risk","Not At Risk","Insufficient data"],range=["#FF8266","#70C0B8","#D8D0CC"]),
                legend=alt.Legend(title=None,orient="bottom")
            ),
            tooltip=[alt.Tooltip("Risk:N",title="Prediction"),alt.Tooltip("Students:Q",title="Records")]
        ).properties(height=250)

        st.altair_chart(donut,use_container_width=True)


        