#imports
import streamlit as st

from authenticate import set_tutorial_seen


def show_tutorial():

    st.title("Welcome to Phronesis")

    st.write(
        f"Welcome, {st.session_state['teacher_name']}! "
        "Here is a quick guide to getting started."
    )

    st.markdown("---")


    ##########DASHBOARD##########

    st.write("### 1. Dashboard")

    st.info(
        "Your Dashboard gives you a quick overview of your classes, "
        "students requiring attention and important patterns in your data."
    )


    ##########CLASSES##########

    st.write("### 2. Classes")

    st.info(
        "Select a year group, subject and class to review class performance. "
        "You can then select an individual student to view their risk prediction, "
        "learning indicators, insights and recommended next steps."
    )


    ##########DATA MANAGEMENT##########

    st.write("### 3. Data Management")

    st.info(
        "Start here when adding your own data. Create your subjects, classes "
        "and students, then add assessment and attendance information or "
        "upload data using the provided CSV templates."
    )


    ##########RECOMMENDATIONS##########

    st.write("### 4. Insights and Recommendations")

    st.info(
        "Phronesis combines available student data to identify academic risk. "
        "The student profile provides supporting insights, recommended actions "
        "and an editable parent communication."
    )


    ##########GET STARTED##########

    st.markdown("---")

    if st.button(
        "Get Started",
        type="primary",
        use_container_width=True
    ):

        set_tutorial_seen(
            st.session_state["teacher_id"],
            True
        )

        st.session_state["tutorial_seen"] =True

        st.rerun()