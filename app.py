#imports
import streamlit as st

from style_loader import load_styles
from pages.login_page import show_login_page
from pages.tutorial import show_tutorial
from accessibility import apply_accessibility_settings


##########APP SETUP##########

st.set_page_config(
    page_title="Phronesis",
    layout="wide",
    initial_sidebar_state="expanded"
)

#apply styling
load_styles()

#load accessibility settings
#apply accessibility preferences
apply_accessibility_settings()


##########LOGIN STATE##########

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] =False


##########NOT LOGGED IN##########

if not st.session_state["logged_in"]:

    #only login page exists before signing in
    login_page =st.Page(
        show_login_page,
        title="Sign In"
    )

    page =st.navigation(
        [login_page],
        position="hidden"
    )

    page.run()

    st.stop()


##########FIRST LOGIN TUTORIAL##########

if not st.session_state.get("tutorial_seen",False):

    #hide normal navigation during tutorial
    tutorial_page =st.Page(
        show_tutorial,
        title="Welcome"
    )

    page =st.navigation(
        [tutorial_page],
        position="hidden"
    )

    page.run()

    st.stop()


##########LOGGED IN PAGES##########

dashboard_page =st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

class_page =st.Page(
    "pages/class_page.py",
    title="My Classes",
    icon="👥"
)

data_upload_page =st.Page(
    "pages/data_upload.py",
    title="Data Management",
    icon="📁"
)

settings_page =st.Page(
    "pages/settings.py",
    title="Settings",
    icon="⚙️"
)


##########NORMAL NAVIGATION##########

page =st.navigation(
    [
        dashboard_page,
        class_page,
        data_upload_page,
        settings_page
    ],
    position="sidebar",
    expanded=True
)


##########SIDEBAR##########

st.sidebar.title("Phronesis")

st.sidebar.write(
    "AI-Driven Student Risk Analytics"
)

st.sidebar.markdown("---")

st.sidebar.write(
    f"**{st.session_state['teacher_name']}**"
)

st.sidebar.caption(
    st.session_state["teacher_email"]
)

st.sidebar.markdown("---")


##########RUN PAGE##########

page.run()