import streamlit as st

from style_loader import load_styles


#set up app
st.set_page_config(
    page_title="Phronesis",
    layout="wide",
    initial_sidebar_state="expanded"
)


#apply styling
load_styles()


##########Pages##########

dashboard_page = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

student_page = st.Page(
    "pages/student_page.py",
    title="Students",
    icon="👥"
)

data_upload_page = st.Page(
    "pages/data_upload.py",
    title="Data Upload",
    icon="📁"
)

about_page = st.Page(
    "pages/about.py",
    title="About",
    icon="ℹ️"
)


##########Navigation##########

page = st.navigation(
    [
        dashboard_page,
        student_page,
        data_upload_page,
        about_page
    ],
    position="sidebar",
    expanded=True
)


#sidebar heading
st.sidebar.title("Phronesis")
st.sidebar.write(
    "AI-Driven Student Risk Analytics"
)

st.sidebar.markdown("---")


#run selected page
page.run()