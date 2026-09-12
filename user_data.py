#imports
import os
import pandas as pd
import streamlit as st


##########GET USER FOLDER##########

def get_user_folder():

    teacher_id =st.session_state["teacher_id"]

    folder =f"data/users/{teacher_id}"

    os.makedirs(folder,exist_ok=True)

    return folder


##########GET USER FILE##########

def get_user_file(filename):

    folder =get_user_folder()

    return f"{folder}/{filename}"


##########CREATE EMPTY USER DATA##########

def create_user_files():

    folder =get_user_folder()

    files ={

        "students.csv":[
            "student_id",
            "name",
            "year_group"
        ],

        "subjects.csv":[
            "subject_id",
            "subject_name"
        ],

        "classes.csv":[
            "class_id",
            "class_name",
            "subject_id",
            "year_group"
        ],

        "class_students.csv":[
            "class_id",
            "student_id"
        ],

        "assessment.csv":[
            "student_id",
            "subject",
            "assessment_title",
            "assessment_date",
            "score",
            "max_score",
            "pass_mark"
        ],

        "attendance.csv":[
            "student_id",
            "total_sessions",
            "sessions_attended"
        ],

        "homework_completion.csv":[
            "student_id",
            "homework_completion"
        ],

        "behaviour.csv":[
            "student_id",
            "behaviour_incidents"
        ]
    }

    for filename,columns in files.items():

        filepath =f"{folder}/{filename}"

        if not os.path.exists(filepath):

            empty_data =pd.DataFrame(
                columns=columns
            )

            empty_data.to_csv(
                filepath,
                index=False
            )