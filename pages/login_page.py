#imports
import streamlit as st

from authenticate import create_account
from authenticate import login_teacher
from user_data import create_user_files


def show_login_page():

    st.title("Phronesis")
    st.write("AI-Driven Student Risk Analytics")

    st.write("### Welcome")

    login_tab,signup_tab =st.tabs([
        "Sign In",
        "Create Account"
    ])


    ##########SIGN IN##########

    with login_tab:

        st.write("### Sign In")

        with st.form("login_form"):

            email =st.text_input("Email")
            password =st.text_input("Password",type="password")

            login_button =st.form_submit_button(
                "Sign In",
                use_container_width=True
            )

        if login_button:

            teacher =login_teacher(email,password)

            if teacher is None:
                st.error("Incorrect email or password.")

            else:
                st.session_state["logged_in"] =True
                st.session_state["teacher_id"] =teacher["teacher_id"]
                st.session_state["teacher_name"] =teacher["name"]
                st.session_state["teacher_email"] =teacher["email"]
                st.session_state["tutorial_seen"] =False

                #create this teacher's own data files
                create_user_files()

                tutorial_seen =str(
                    teacher["tutorial_seen"]
                ).lower() =="true"

                st.session_state["tutorial_seen"] =tutorial_seen

                st.rerun()


    ##########SIGN UP##########

    with signup_tab:

        st.write("### Create Account")

        with st.form("signup_form"):

            name =st.text_input("Name")
            email =st.text_input("Email Address")

            password =st.text_input(
                "Password",
                type="password"
            )

            confirm_password =st.text_input(
                "Confirm Password",
                type="password"
            )

            signup_button =st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if signup_button:

            if password !=confirm_password:
                st.error("Passwords do not match.")

            else:

                success,message,teacher =create_account(
                    name,
                    email,
                    password
                )

                if not success:
                    st.error(message)

                else:
                    #sign teacher in automatically
                    st.session_state["logged_in"] =True
                    st.session_state["teacher_id"] =teacher["teacher_id"]
                    st.session_state["teacher_name"] =teacher["name"]
                    st.session_state["teacher_email"] =teacher["email"]
                    st.session_state["tutorial_seen"] =False

                    st.rerun()