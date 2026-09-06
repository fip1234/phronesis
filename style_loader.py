import streamlit as st


def load_styles():

    #open css styling file
    with open("styles/styles.css") as css_file:
        css = css_file.read()

    #apply styling to streamlit app
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )