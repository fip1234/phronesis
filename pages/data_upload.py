#imports
import streamlit as st
from data_management.subjects import show_subjects
from data_management.classes import show_classes

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

#show page
show_data_upload()