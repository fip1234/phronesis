#imports
import streamlit as st

from authenticate import create_account
from authenticate import login_teacher
from user_data import create_user_files


def show_login_page():


    ##########BACK TO INTRO##########

    #return to public Phronesis introduction page
    if st.button(
        "← Back to Phronesis",
        key="back_to_intro"
    ):
        st.session_state["public_view"] ="intro"
        st.rerun()


    ##########PAGE LAYOUT##########

    #left side explains Phronesis
    #right side contains sign in/create account forms
    intro_col,form_col =st.columns(
        [0.9,1.1],
        gap="large"
    )


    ##########LEFT SIDE##########

    with intro_col:

        st.markdown(
            """
            <div class="auth-intro">

                <div class="public-brand">
                    Phronesis
                </div>

                <h1>
                    Student insight without losing teacher judgement.
                </h1>

                <p>
                    Bring student information together, identify potential
                    risk and understand the evidence behind each prediction.
                </p>

                <p>
                    Sign in to continue to your classes, dashboard and
                    student insights.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    ##########RIGHT SIDE##########

    with form_col:

        st.write("## Welcome")

        #switch between existing account and new account forms
        login_tab,signup_tab =st.tabs([
            "Sign In",
            "Create Account"
        ])


        ##########SIGN IN##########

        with login_tab:

            st.write("### Sign In")

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

                #check entered credentials against teacher account
                teacher =login_teacher(
                    email,
                    password
                )

                if teacher is None:

                    st.error(
                        "Incorrect email or password."
                    )

                else:

                    #store signed-in teacher information for current session
                    st.session_state["logged_in"] =True
                    st.session_state["teacher_id"] =teacher["teacher_id"]
                    st.session_state["teacher_name"] =teacher["name"]
                    st.session_state["teacher_email"] =teacher["email"]

                    #ensure teacher has their own data workspace
                    create_user_files()

                    #check whether teacher has already completed tutorial
                    tutorial_seen =str(
                        teacher["tutorial_seen"]
                    ).lower() =="true"

                    st.session_state["tutorial_seen"] =tutorial_seen

                    #reload app using signed-in state
                    st.rerun()


        ##########SIGN UP##########

        with signup_tab:

            st.write("### Create Account")

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

                #make sure both password entries match
                if password !=confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                else:

                    #create new teacher account
                    success,message,teacher =create_account(
                        name,
                        email,
                        password
                    )

                    if not success:

                        st.error(message)

                    else:

                        #automatically sign teacher in after registration
                        st.session_state["logged_in"] =True
                        st.session_state["teacher_id"] =teacher["teacher_id"]
                        st.session_state["teacher_name"] =teacher["name"]
                        st.session_state["teacher_email"] =teacher["email"]

                        #new users should see tutorial on first login
                        st.session_state["tutorial_seen"] =False

                        #create separate empty data workspace for teacher
                        create_user_files()

                        #reload app and move into first-login tutorial
                        st.rerun()