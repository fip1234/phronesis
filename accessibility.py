#imports
import streamlit as st


def apply_accessibility_settings():

    ##########FONT SIZE##########

    font_size =st.session_state.get(
        "font_size",
        "Medium"
    )

    if font_size =="Small":
        text_size ="14px"

    elif font_size =="Large":
        text_size ="18px"

    elif font_size =="Extra Large":
        text_size ="20px"

    else:
        text_size ="16px"


    ##########FONT##########

    dyslexia_font =st.session_state.get(
        "dyslexia_font",
        False
    )

    if dyslexia_font:
        font_family ="Verdana, Arial, sans-serif"

    else:
        font_family ="Arial, sans-serif"


    ##########THEME##########

    display_mode =st.session_state.get(
        "display_mode",
        "Light"
    )

    if display_mode =="Dark":

        background ="#121212"
        secondary_background ="#1E1E1E"
        text_colour ="#F5F5F5"

    else:

        background ="#FFFFFF"
        secondary_background ="#F5F5F5"
        text_colour ="#202020"


    ##########APPLY STYLES##########

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-color:{background};
            color:{text_colour};
            font-family:{font_family};
        }}

        .stApp p,
        .stApp label,
        .stApp button,
        .stApp input,
        .stApp textarea {{
            font-family:{font_family};
        }}

        .stApp p,
        .stApp label {{
            font-size:{text_size};
        }}

        [data-testid="stSidebar"] {{
            background-color:{secondary_background};
        }}

        /* DO NOT override material icon font */
        span[data-testid="stIconMaterial"] {{
            font-family:"Material Symbols Rounded" !important;
            font-weight:normal !important;
            font-style:normal !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )