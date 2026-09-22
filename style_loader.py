#imports
import streamlit as st


def load_styles(style_file="styles.css"):

    #open chosen css styling file
    with open(f"styles/{style_file}",encoding="utf-8") as css_file:
        css =css_file.read()

    #apply styling to streamlit app
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )