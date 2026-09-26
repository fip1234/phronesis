#accessibility.py- for better accessibility and user experience changing fonts,sizes etc
# #imports
import streamlit as st


def apply_accessibility_settings():
    ##########FONT SIZE############
    font_size =st.session_state.get("font_size","Medium")
    text_size ={"Small":"14px","Medium":"16px","Large":"18px","Extra Large":"20px"}.get(font_size,"16px")

    ##########FONTS##########
    dyslexia_font =st.session_state.get("dyslexia_font",False)
    if dyslexia_font:
        font_family ="OpenDyslexic, Arial, sans-serif"
        heading_font ="OpenDyslexic, Arial, sans-serif"
        #get open dyslexic font from CDN
        st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/opendyslexic@5.3.0/400.css">',
                    unsafe_allow_html=True)
    else:
        font_family ="var(--bodyFont)"
        heading_font ="var(--headerFont)"

    #############THEME#######
    #fixme-is not fully yet implemented
    display_mode =st.session_state.get("display_mode","Light")
    if display_mode =="Dark":
        background,secondary_background,text_colour ="#121212","#1E1E1E","#F5F5F5"
    else:
        background,secondary_background,text_colour ="#FFFFFF","#F5F5F5","#202020"

    ##########APPLY STYLES##########
    st.markdown(
        f"""
        <style>
        .stApp{{background-color:{background};color:{text_colour};font-family:{font_family};}}

        # apply font family and weight to various elements
        .stApp p,.stApp label,.stApp button,.stApp input,.stApp textarea,
        .stApp select,.stApp [data-testid="stMetricLabel"],
        #apply font family and weight to metric values
        .stApp [data-testid="stMetricValue"]{{font-family:{font_family} !important; font-weight:400 !important;}}

        .stApp p,.stApp label{{font-size:{text_size};}}
        .stApp h1,.stApp h2,.stApp h3{{font-family:{heading_font} !important;}}

        [data-testid="stSidebar"]{{background-color:{secondary_background};}}

        span[data-testid="stIconMaterial"]{{font-family:"Material Symbols Rounded" !important;
                                            font-weight:normal !important;font-style:normal !important;}}

        #responsive font size for small screens
        @media(max-width:600px){{.stApp h1{{font-size:1.8rem;}}.stApp h2{{font-size:1.5rem;}}}}
        </style>
        """,
        unsafe_allow_html=True
    )