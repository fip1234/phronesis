#style_loader.py- so that Streamlit can load custom styles that override default styles
# #imports
import base64
import streamlit as st


def load_styles(style_file="styles.css"):
    #load css into a string
    with open(f"styles/{style_file}",encoding="utf-8") as css_file:
        css =css_file.read()

    #local background image into css data so streamlit can render
    if style_file =="styles.css":

        #local background image into base64 encoded string
        with open("assets/phronesis_background.png","rb") as image_file:
            image_data =base64.b64encode(image_file.read()).decode()

        css =css.replace('url("../assets/phronesis_background.png")',
            f'url("data:image/png;base64,{image_data}")' )

    #css injected into streamlit app
    st.markdown(f"<style>{css}</style>",unsafe_allow_html=True)