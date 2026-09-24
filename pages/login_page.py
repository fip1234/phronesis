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

            if st.button(
                "← Back to Phronesis",
                key="back_to_intro",
                use_container_width=True
            ):
                st.session_state["public_view"] ="intro"
                st.rerun()


        ##########MAIN LAYOUT##########

        intro_col,form_col =st.columns(
            [0.9,1.1],
            gap="large"
        )


        ##########LEFT PANEL##########

        with intro_col:

            with st.container(key="auth_intro_panel"):

                st.caption(
                    "PHRONESIS"
                )

                st.title(
                    "Welcome back."
                )

                st.subheader(
                    "Student insight without losing teacher judgement."
                )

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


        ##########RIGHT PANEL##########

        with form_col:

            with st.container(key="auth_form_panel"):

                st.title(
                    "Welcome"
                )

                st.write(
                    "Sign in to continue or create your Phronesis account."
                )


                ##########TABS##########

                login_tab,signup_tab =st.tabs([
                    "Sign In",
                    "Create Account"
                ])


                ##########SIGN IN##########

                with login_tab:

                    st.subheader(
                        "Sign In"
                    )

                    st.caption(
                        "Enter your account details to continue."
                    )


                    with st.form("login_form"):

                        email =st.text_input(
                            "Email",
                            placeholder="name@example.com"
                        )

                        password =st.text_input(
                            "Password",
                            type="password",
                            placeholder="Enter your password"
                        )

                        login_button =st.form_submit_button(
                            "Sign In",
                            use_container_width=True
                        )


                    if login_button:

                        teacher =login_teacher(
                            email,
                            password
                        )


                        if teacher is None:

                            st.error(
                                "Incorrect email or password."
                            )


                        else:

                            #store signed-in teacher information
                            st.session_state["logged_in"] =True
                            st.session_state["teacher_id"] =teacher["teacher_id"]
                            st.session_state["teacher_name"] =teacher["name"]
                            st.session_state["teacher_email"] =teacher["email"]

                            #make sure teacher has their own data workspace
                            create_user_files()

                            #check if tutorial has already been completed
                            tutorial_seen =str(
                                teacher["tutorial_seen"]
                            ).lower() =="true"

                            st.session_state["tutorial_seen"] =tutorial_seen

                            st.rerun()


                ##########CREATE ACCOUNT##########

                with signup_tab:

                    st.subheader(
                        "Create Account"
                    )

                    st.caption(
                        "Create your own Phronesis teacher workspace."
                    )


                    with st.form("signup_form"):

                        name =st.text_input(
                            "Name",
                            placeholder="Your name"
                        )

                        email =st.text_input(
                            "Email Address",
                            placeholder="name@example.com"
                        )

                        password =st.text_input(
                            "Password",
                            type="password",
                            placeholder="Create a password"
                        )

                        confirm_password =st.text_input(
                            "Confirm Password",
                            type="password",
                            placeholder="Enter your password again"
                        )

                        signup_button =st.form_submit_button(
                            "Create Account",
                            use_container_width=True
                        )


                    if signup_button:

                        if password !=confirm_password:

                            st.error(
                                "Passwords do not match."
                            )


                        else:

                            success,message,teacher =create_account(
                                name,
                                email,
                                password
                            )


                            if not success:

                                st.error(
                                    message
                                )


                            else:

                                #automatically sign teacher in
                                st.session_state["logged_in"] =True
                                st.session_state["teacher_id"] =teacher["teacher_id"]
                                st.session_state["teacher_name"] =teacher["name"]
                                st.session_state["teacher_email"] =teacher["email"]

                                #new users should see tutorial
                                st.session_state["tutorial_seen"] =False

                                #create separate teacher data workspace
                                create_user_files()

                                st.rerun()