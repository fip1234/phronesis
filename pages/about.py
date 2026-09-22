#imports
import streamlit as st


def show_about_page():

    ##########INTRO##########

    st.title("Phronesis")

    st.write(
        "AI-Driven Student Risk Analytics"
    )

    st.write(
        """
        Phronesis helps teachers identify students who may need
        additional support and understand the information contributing
        to that prediction.
        """
    )

    #move from intro page to sign in/create account page
    if st.button(
        "Get Started",
        type="primary"
    ):
        st.session_state["public_view"] ="login"
        st.rerun()