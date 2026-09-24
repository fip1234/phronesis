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

    ##########LOGIN / SIGN UP##########
    if st.session_state["public_view"] =="login":
        #load styling only for login/signup page
        load_styles("login_styles.css")
        show_login_page()

    ##########ABOUT / LANDING PAGE##########
    else:
        #load styling only for landing page
        load_styles("about_styles.css")
        show_about_page()

    #prevent logged-in pages loading underneath
    st.stop()

##########FIRST LOGIN TUTORIAL##########
if not st.session_state.get("tutorial_seen",False):
    #use clean public styling because normal navbar is hidden
    load_styles("tutorial_styles.css")
    # apply_accessibility_settings()

    #hide normal navigation during tutorial
    tutorial_page =st.Page(show_tutorial,title="Welcome")

    page =st.navigation([tutorial_page],position="hidden")

    page.run()
    st.stop()

##########LOGGED IN STYLING##########

#main application styling
load_styles("styles.css")

#user accessibility preferences only apply inside logged-in app
apply_accessibility_settings()

##########LOGGED IN PAGES##########

#FIX!- add full styling - hover,navbar,riskcolours
load_styles("styles.css")
apply_accessibility_settings()

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
