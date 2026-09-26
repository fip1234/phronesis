#imports
import streamlit as st

from authenticate import create_account
from authenticate import login_teacher
from user_data import create_user_files


def show_login_page():

    ##########LOGIN PAGE##########
    with st.container(key="auth_page"):

        ##########BACK BUTTON##########
        back_col,empty_col =st.columns([1.6,7])

        with back_col:
            if st.button("← Back to Phronesis",key="back_to_intro",use_container_width=True):
                st.session_state["public_view"] ="intro"
                st.rerun()

        ##########MAIN LAYOUT##########
        intro_col,form_col =st.columns([0.9,1.1],gap="large")

        ##########LEFT PANEL##########
        with intro_col:
            with st.container(key="auth_intro_panel"):
                st.caption("PHRONESIS")
                st.title("Welcome back.")
                st.subheader("Student insight without losing teacher judgement.")

                st.write(
                    """
                    Bring student information together, identify
                    potential risk and understand the evidence
                    behind each prediction.
                    """
                )

                st.write(
                    """
                    Sign in to continue to your classes,
                    dashboard and student insights.
                    """
                )

        #######RIGHT PANEL##########
        with form_col:
            with st.container(key="auth_form_panel"):
                st.title("Welcome")
                st.write("Sign in to continue or create your Phronesis account.")

                ##########TABS##############
                login_tab,signup_tab =st.tabs(["Sign In","Create Account"])

                #######SIGN IN###########
                with login_tab:
                    st.subheader("Sign In")
                    st.caption("Please enter your account details to continue.")

                    with st.form("login_form"):
                        login_email =st.text_input("Email",placeholder="name@example.com")
                        login_password =st.text_input("Password",type="password",placeholder="Enter your password")
                        login_btn =st.form_submit_button("Sign In",use_container_width=True)

                    if login_btn:
                        teacher_info =login_teacher(login_email,login_password)

                        if teacher_info is None:
                            st.error("Incorrect email or password.")
                        else:
                            #store teacher logininformation
                            st.session_state["logged_in"] =True
                            st.session_state["teacher_id"] =teacher_info["teacher_id"]
                            st.session_state["teacher_name"] =teacher_info["name"]
                            st.session_state["teacher_email"] =teacher_info["email"]

                            #make sure teacher has own data workspace
                            create_user_files()

                            #tutorial has already completed?
                            seen_tutorial_already =str(teacher_info["tutorial_seen"]).lower() =="true"
                            st.session_state["tutorial_seen"] =seen_tutorial_already

                            st.rerun()

                ##########CREATE ACCOUNT##########
                with signup_tab:
                    st.subheader("Create Account")
                    st.caption("Create your own Phronesis teacher workspace.")

                    #new form account creation
                    with st.form("signup_form"):
                        new_name =st.text_input("Name",placeholder="Your name")
                        new_email =st.text_input("Email Address",placeholder="name@example.com")
                        new_password =st.text_input("Password",type="password",placeholder="Create a password")
                        new_password_check =st.text_input("Confirm Password",type="password",placeholder="Enter your password again")
                        signup_btn =st.form_submit_button("Create Account",use_container_width=True)

                    if signup_btn:
                        if new_password !=new_password_check:
                            st.error("Passwords do not match.")
                        else:
                            worked,error_msg,new_teacher =create_account(new_name,new_email,new_password)

                            if not worked:
                                st.error(error_msg)
                            else:
                                #automatically sign teacher in
                                st.session_state["logged_in"] =True
                                st.session_state["teacher_id"] =new_teacher["teacher_id"]
                                st.session_state["teacher_name"] =new_teacher["name"]
                                st.session_state["teacher_email"] =new_teacher["email"]

                                #new users should see tutorial
                                st.session_state["tutorial_seen"] =False

                                #separate teacher data workspace made
                                create_user_files()

                                st.rerun()