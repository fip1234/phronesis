import streamlit as st
import pandas as pd

from risk_engine import (
    calculate_risk,
    risk_category,
    generate_reasons,
    generate_recommendations
)

st.set_page_config(page_title="Phronesis", layout="wide")

# ---------------- CUSTOM COLOURS ----------------
st.markdown("""
<style>

/* Main app */
.stApp {
    background-color: #EDEDED;
    color: #000000;
    font-family: "Segoe UI", sans-serif;
}

/* Make ALL text black */
.stApp,
.stMarkdown,
p,
span,
div,
label,
h1,
h2,
h3,
h4,
h5,
h6 {
    color: #000000 !important;
    font-family: "Segoe UI", sans-serif !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FF8266;
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-family: "Segoe UI", sans-serif !important;
}

/* Risk cards */
.high-risk {
    background-color: #FF8266;
    color: black;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.medium-risk {
    background-color: #FFB866;
    color: black;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

.low-risk {
    background-color: #FFFF83;
    color: black;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("Phronesis")

st.sidebar.write("""
AI-Driven Student Risk Analytics Prototype
""")

st.sidebar.markdown("---")

st.sidebar.write("Features")
st.sidebar.write("• Student Risk Dashboard")
st.sidebar.write("• Risk Explanations")
st.sidebar.write("• Recommended Actions")

# ---------------- MAIN TITLE ----------------
st.title("Phronesis")
st.subheader("AI-Driven Student Risk Analytics Prototype")

# Load CSV files
students = pd.read_csv("data/students.csv")
attendance = pd.read_csv("data/attendance.csv")
assessment = pd.read_csv("data/assessment.csv")
behaviour = pd.read_csv("data/behaviour.csv")
homework = pd.read_csv("data/homework.csv")

# Check required columns exist
required_columns = {
    "students": ["student_id", "name", "year_group"],
    "attendance": ["student_id", "attendance_percentage"],
    "assessment": ["student_id", "assessment_score"],
    "behaviour": ["student_id", "behaviour_points"],
    "homework": ["student_id", "homework_completion"]
}

datasets = {
    "students": students,
    "attendance": attendance,
    "assessment": assessment,
    "behaviour": behaviour,
    "homework": homework
}

for file_name, columns in required_columns.items():
    for column in columns:
        if column not in datasets[file_name].columns:
            st.error(f"Missing column '{column}' in {file_name}.csv")
            st.stop()

#MERGE ALL DATASETS INTO ONE BASED ON STUDENT ID
df =students.merge(attendance,on="student_id")
df =df.merge(assessment,on="student_id")
df =df.merge(behaviour,on="student_id")
df =df.merge(homework,on="student_id")

df["missing_data"] = df.isnull().any(axis=1)

# Apply risk engine
df["risk_score"] = df.apply(calculate_risk, axis=1)
df["risk_level"] = df["risk_score"].apply(risk_category)

df = df.sort_values(by="risk_score", ascending=False)

# ---------------- DASHBOARD ----------------
st.header("Student Risk Dashboard")

high_count = (df["risk_level"] == "High").sum()
medium_count = (df["risk_level"] == "Medium").sum()
low_count = (df["risk_level"] == "Low").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"<div class='high-risk'>High Risk Students<br><h2>{high_count}</h2></div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"<div class='medium-risk'>Medium Risk Students<br><h2>{medium_count}</h2></div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"<div class='low-risk'>Low Risk Students<br><h2>{low_count}</h2></div>",
        unsafe_allow_html=True
    )

st.markdown("")

display_df = df.fillna("Data Missing")

display_df = display_df[
    [
        "student_id",
        "name",
        "attendance_percentage",
        "assessment_score",
        "behaviour_points",
        "homework_completion",
        "risk_score",
        "risk_level"
    ]
]

st.dataframe(display_df, use_container_width=True)

# ---------------- STUDENT EXPLANATION ----------------
st.header("Student Risk Explanation")

selected_student = st.selectbox(
    "Choose a student",
    df["name"]
)

student_row = df[df["name"] == selected_student].iloc[0]

st.subheader(selected_student)

if student_row["missing_data"]:
    st.warning("Some student data is missing. Risk calculations may be less accurate.")

if student_row["risk_level"] == "High":
    st.markdown(
        f"<div class='high-risk'>High Risk Student — Score: {student_row['risk_score']}</div>",
        unsafe_allow_html=True
    )
elif student_row["risk_level"] == "Medium":
    st.markdown(
        f"<div class='medium-risk'>Medium Risk Student — Score: {student_row['risk_score']}</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<div class='low-risk'>Low Risk Student — Score: {student_row['risk_score']}</div>",
        unsafe_allow_html=True
    )

st.write("### Reasons")

reasons = generate_reasons(student_row)

for reason in reasons:
    st.write(f"- {reason}")

st.write("### Recommended Actions")

recommendations = generate_recommendations(student_row)

for recommendation in recommendations:
    st.write(f"- {recommendation}")