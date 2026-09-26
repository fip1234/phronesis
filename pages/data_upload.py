#data upload.py- page for managing and uploading data related to subjects, classes, students, assessments, and attendance

#imports
import streamlit as st

from style_loader import load_styles
from data_management.subjects import show_subjects
from data_management.classes import show_classes
from data_management.students import show_students
from data_management.assessments import show_assessments
from data_management.attendance import show_attendance

def show_data_upload():
    load_styles("data_management_styles.css")

    #container for data management page
    with st.container(key="data_management_page"):
        st.title("Data Upload")
        st.write("Add, upload and manage the information used by Phronesis.")

        ##########DATA TYPE##########
        #set default selected section if not already set
        if "dataSection" not in st.session_state:
            st.session_state["dataSection"] ="Subjects"

        subjectCol,classCol,studentCol,assessmentCol,attendanceCol =st.columns(5)

        #all the tab buttons in each column
        with subjectCol:
            if st.button("Subjects",key="subject_tab",type="primary" if st.session_state["dataSection"] =="Subjects" else "secondary",use_container_width=True):
                st.session_state["dataSection"] ="Subjects"
                st.rerun()

        with classCol:
            if st.button("Classes",key="class_tab",type="primary" if st.session_state["dataSection"] =="Classes" else "secondary",use_container_width=True):
                st.session_state["dataSection"] ="Classes"
                st.rerun()

        with studentCol:
            if st.button("Students",key="student_tab",type="primary" if st.session_state["dataSection"] =="Students" else "secondary",use_container_width=True):
                st.session_state["dataSection"] ="Students"
                st.rerun()

        with assessmentCol:
            if st.button("Assessments",key="assessment_tab",type="primary" if st.session_state["dataSection"] =="Assessments" else "secondary",use_container_width=True):
                st.session_state["dataSection"] ="Assessments"
                st.rerun()

        with attendanceCol:
            if st.button("Attendance",key="attendance_tab",type="primary" if st.session_state["dataSection"] =="Attendance" else "secondary",use_container_width=True):
                st.session_state["dataSection"] ="Attendance"
                st.rerun()

        ##########CONTENT##########
        #link to datamanagement functions
        with st.container(key="data_content"):
            dataSection =st.session_state["dataSection"]

            #show correct section based on selected tab
            if dataSection =="Subjects":
                show_subjects()
            elif dataSection =="Classes":
                show_classes()
            elif dataSection =="Students":
                show_students()
            elif dataSection =="Assessments":
                show_assessments()
            elif dataSection =="Attendance":
                show_attendance()


#show page
show_data_upload()