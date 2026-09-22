####STYLES
 
##imports
import streamlit as st
from style_loader import load_styles
from pages.about import show_about_page
from pages.login_page import show_login_page
from pages.tutorial import show_tutorial
from accessibility import apply_accessibility_settings

##########APP SETUP##########
st.set_page_config(page_title="Phronesis",layout="wide",initial_sidebar_state="auto")

##########LOGIN STATE##########
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] =False

#controls intro page or sign in/create account page
if "public_view" not in st.session_state:
    st.session_state["public_view"] ="intro"

##########NOT LOGGED IN##########
if not st.session_state["logged_in"]: 
    #use styling specifically designed for public pages
    load_styles("public_styles.css")

    #apply accessibility preferences
    apply_accessibility_settings()

    #show sign in/create account page
    if st.session_state["public_view"] =="login":
        show_login_page()

    #first page shown when app opens
    else:
        show_about_page()

    st.stop()

##########FIRST LOGIN TUTORIAL##########
if not st.session_state.get("tutorial_seen",False):
    #use clean public styling because normal navbar is hidden
    load_styles("public_styles.css")
    apply_accessibility_settings()

    #hide normal navigation during tutorial
    tutorial_page =st.Page(show_tutorial,title="Welcome")

    page =st.navigation([tutorial_page],position="hidden")

    page.run()
    st.stop()


##########LOGGED IN PAGES##########

dashboard_page =st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon=":material/home:",
    default=True
)

class_page =st.Page(
    "pages/class_page.py",
    title="My Classes",
    icon=":material/groups:"
)

data_upload_page =st.Page(
    "pages/data_upload.py",
    title="Data Management",
    icon=":material/folder:"
)

settings_page =st.Page(
    "pages/settings.py",
    title="Settings",
    icon=":material/settings:"
)


##########NORMAL NAV##########
page =st.navigation(
    [dashboard_page,class_page,data_upload_page,settings_page],
    position="sidebar",
    expanded=False
)

#content under the navigation
st.sidebar.title("Phronesis")
st.sidebar.write("AI-Driven Student Risk Analytics")
st.sidebar.markdown("---")
st.sidebar.write(f"**{st.session_state['teacher_name']}**")
st.sidebar.caption(st.session_state["teacher_email"])
st.sidebar.markdown("---")

#whole page run
page.run()