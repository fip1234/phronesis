#imports
import streamlit as st
from data_management.subjects import show_subjects
from data_management.classes import show_classes
from data_management.students import show_students
from data_management.assessments import show_assessments
from data_management.attendance import show_attendance

def show_data_upload():

    st.header("Data Upload")

    st.write(
        "Upload and manage your data for subjects, classes, students, assessments, and attendance."
    )

    #DROP DOWN BOX
    data_type =st.selectbox(
        "Choose data type",
        ["Subjects","Classes","Students","Assessments","Attendance"]
    )

    ##########SUBJECTS##########
    if data_type =="Subjects":
        show_subjects()

    ##########CLASSES##########

    elif data_type =="Classes":
        show_classes()

    ##########STUDENTS##########
    elif data_type =="Students":
        show_students()

    ##########ASSESSMENTS##########
    elif data_type =="Assessments":
        show_assessments()

    ##########ATTENDANCE##########
    elif data_type =="Attendance":
        show_attendance()

#show page
show_data_upload()