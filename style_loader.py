#imports
import base64
import streamlit as st


def load_styles(style_file="styles.css"):

    with open(f"styles/{style_file}",encoding="utf-8") as css_file:
        css =css_file.read()

    #convert local background image into CSS data so Streamlit can render it
    if style_file =="styles.css":

        with open("assets/phronesis_background.png","rb") as image_file:
            image_data =base64.b64encode(image_file.read()).decode()

        css =css.replace(
            'url("../assets/phronesis_background.png")',
            f'url("data:image/png;base64,{image_data}")'
        )

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )