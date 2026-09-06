import streamlit as st

from style_loader import load_styles
from pages.sidebar import show_sidebar
from pages.dashboard import show_dashboard
from app_data import load_app_data
from pages.student_page import show_student_page

st.set_page_config(
    page_title="Phronesis",
    layout="wide"
)

#load styling
load_styles()

#show sidebar
show_sidebar()

#main title
st.title("Phronesis")
st.subheader("AI-Driven Student Risk Analytics")

#load final processed data
df = load_app_data()

#show dashboard
show_dashboard(df)
show_student_page(df)