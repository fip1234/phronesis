# Phronesis

Phronesis is a teacher-facing educational decision-support application developed as part of the University of London CM3070 Final Project.

The project follows:

**CM3005 Data Science 1.1 Project Idea 1: Data-Driven Personalised Educational Content Recommendation**

Phronesis combines teacher-entered educational data with machine learning to identify students who may be academically at risk. It also provides contextual student indicators, suggested teacher actions and an editable parent/carer email draft.

The system is designed to support teacher professional judgement rather than replace it.

---

## Important Project Documentation

**Please check the notebook document in the `notebooks` folder when reviewing this project.**

The notebook contains important evidence relating to the machine-learning development process, including exploratory data analysis, preprocessing, feature engineering, model experimentation, model comparison, evaluation metrics and the development of the final Random Forest model.

The main notebook is:

```text
notebooks/01_eda.ipynb
```

The final trained model is already included in the repository, so the notebook does **not** need to be run in order to use the application. However, it should be reviewed alongside the application and project documentation to understand how the final machine-learning solution was developed and evaluated.

---

## Main Features

Phronesis includes:

- Teacher account creation and login
- Teacher-specific data storage
- Subject management
- Class management
- Student management
- Assessment management
- Attendance management
- Manual data entry
- Downloadable CSV templates
- Bulk CSV upload
- Input validation and error handling
- Machine-learning academic risk classification:
  - `At Risk`
  - `Not At Risk`
  - `Insufficient data`
- Dashboard with student and class summaries
- Class Overview with year, subject and class filters
- Individual student information
- Contextual student indicators
- Suggested teacher actions
- Editable parent/carer email generation
- Accessibility settings
- Adjustable font size
- Optional OpenDyslexic font
- First-time user tutorial

---

# Machine Learning

The final prediction model is a trained Random Forest classifier.

Several models were tested during development, including:

- Majority-class baseline
- Logistic Regression
- Decision Tree
- Random Forest

The final tuned Random Forest was selected after model comparison and cross-validation.

The model uses four features:

- `prev_failure`
- `absences`
- `grade_average`
- `grade_change`

## Machine-Learning Notebook

**The notebook document should be checked for the full machine-learning development process.**

It contains the exploratory analysis and experimentation that led to the final model used by Phronesis.

```text
notebooks/01_eda.ipynb
```

This includes evidence of areas such as:

- Dataset exploration
- Data preprocessing
- Class distribution
- Feature investigation
- Feature engineering
- Baseline testing
- Model experimentation
- Model comparison
- Cross-validation
- Evaluation metrics
- Confusion matrices
- Final model selection

The application itself loads the final trained model rather than retraining the models each time it is launched.

---

## Feature Meaning

### `prev_failure`

Indicates whether the student previously failed an assessment in the relevant subject.

### `absences`

Calculated using:

```text
total_sessions - sessions_attended
```

### `grade_average`

Calculated from the two most recent valid assessment results:

```text
(previous_grade + latest_grade) / 2
```

### `grade_change`

Measures the change between the two most recent assessment results:

```text
latest_grade - previous_grade
```

Assessment information is processed separately for each subject so that, for example, a student's Maths assessment history does not influence their Spanish prediction.

---

# Missing and Incomplete Data

Phronesis does not force a prediction when required model information is unavailable.

Students with sufficient model data can receive:

- `At Risk`
- `Not At Risk`

Students without all required model features remain visible in the application but receive:

- `Insufficient data`

Missing model values are not replaced with arbitrary zeros simply to generate a prediction.

This was implemented to avoid presenting teachers with potentially unreliable classifications.

---

# Running Phronesis Locally

Phronesis is a Python Streamlit application.

The trained Random Forest model is already included in the repository, so the model does not need to be retrained before running the application.

---

## 1. Clone the Repository

Clone the repository using Git:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then move into the project directory:

```bash
cd YOUR_REPOSITORY_FOLDER
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

---

## 2. Create a Virtual Environment

Using a virtual environment is recommended.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Required Packages

Install the project dependencies using:

```bash
pip install -r requirements.txt
```

The main packages used by Phronesis include:

```text
streamlit
pandas
scikit-learn
joblib
```

---

## 4. Run the Application

From the project root directory run:

```bash
streamlit run app.py
```

Streamlit should automatically open the application in a browser.

If it does not open automatically, the terminal should display a local address similar to:

```text
http://localhost:8501
```

Open this address in a web browser.

---

# Using Phronesis

## 1. Create an Account or Sign In

Phronesis supports teacher accounts with separate stored data.

A new account can be created directly through the application.

New accounts initially contain no school data.

---

## 2. Add School Data

The recommended setup order is:

1. Add a subject
2. Add a class linked to that subject
3. Add students
4. Assign students to classes
5. Add assessment records
6. Add attendance records

Data can be added manually or through CSV upload.

---

## 3. Manual Data Entry

The Data Management area allows teachers to add, edit and delete:

- Subjects
- Classes
- Students
- Assessments
- Attendance records

---

## 4. CSV Upload

Phronesis provides downloadable CSV templates.

Teachers can:

1. Select the relevant data type
2. Download a template
3. Complete the template
4. Upload the completed CSV
5. Review validation feedback

For assessment templates, student information and assessment details can be pre-filled so that the teacher mainly needs to enter student scores.

---

## 5. Validation

Uploaded information is validated before being added to the application.

Validation includes checks for:

- Required columns
- Missing required values
- Empty text fields
- Unknown student IDs
- Unknown classes
- Duplicate records
- Invalid assessment dates
- Future assessment dates
- Non-numeric scores
- Negative scores
- Scores greater than maximum score
- Invalid pass marks
- Non-numeric attendance sessions
- Non-whole attendance sessions
- Negative attendance values
- `sessions_attended > total_sessions`
- Duplicate attendance records
- Invalid class/student relationships

Where invalid data is detected, Phronesis displays an error message and prevents the invalid record from entering the prediction pipeline.

---

# Application Processing Pipeline

The main application processing is centralised through:

```python
load_app_data()
```

This prevents individual Streamlit pages from repeating the same backend operations.

The general pipeline is:

```text
Teacher Data
    ↓
Validation and Storage
    ↓
load_app_data()
    ↓
Assessment Processing
    ↓
Attendance Processing
    ↓
Feature Engineering
    ↓
Dataset Merge
    ↓
Random Forest Prediction
    ↓
Risk Status
    ↓
Contextual Insights
    ↓
Rule-Based Recommendations
    ↓
Dashboard / Class Overview / Student Output
```

`load_app_data()`:

1. Loads the current teacher's data
2. Processes assessment records
3. Processes attendance records
4. Engineers model features
5. Merges the processed datasets
6. Applies the trained Random Forest model to eligible students
7. Keeps incomplete students visible
8. Returns one combined dataset for use throughout the interface

---

# Dashboard

The Dashboard provides a quick overview of the teacher's current data.

It includes information such as:

- Number of classes
- Number of students
- Number of students currently At Risk
- Classes containing At Risk students
- Students requiring attention
- Average attendance
- Class-level summaries
- Risk distribution
- At Risk / Not At Risk / Insufficient data breakdown

The purpose of the Dashboard is to reduce the need for teachers to manually inspect every individual student record.

---

# Class Overview

The Class Overview page allows teachers to filter using:

- Year group
- Subject
- Class

The class table combines student data with model outputs.

Students can then be selected individually for a more detailed view.

The student view can include:

- Risk status
- Attendance
- Recent assessment average
- Assessment change
- Previous assessment failure
- Homework information where available
- Behaviour information where available
- Contextual insights
- Recommended actions

---

# Contextual Insights

The Random Forest produces the academic risk classification.

It does not directly generate explanations for individual predictions.

A separate rule-based layer examines observable student information and generates readable contextual statements.

Examples include:

- Low attendance
- Declining assessment performance
- Low recent assessment average
- Previous failed assessments
- Homework concerns where data is available
- Behaviour concerns where data is available

These statements are intended to provide context for teacher interpretation.

They should not be treated as exact explanations of the internal reasoning of the Random Forest model.

---

# Recommendations

Recommendations are generated separately using rule-based logic.

Examples include:

- Monitor attendance
- Discuss attendance with the student or parent/carer
- Review previously failed assessment topics
- Provide targeted academic support
- Review recent assessments
- Monitor homework completion
- Consider pastoral or classroom support

Recommendations are intended to support teacher judgement rather than automatically decide what intervention must take place.

---

# Parent / Carer Email Generator

Phronesis can create an editable parent/carer communication draft.

The draft uses:

- Student information
- Risk status
- Contextual insights
- Suggested next steps

Before use, the teacher is explicitly instructed to review and edit the email.

The generated email is therefore intended as a starting point rather than an automatically sent communication.

---

# Accessibility and Usability

Phronesis includes several accessibility and usability features.

These include:

- Consistent layout across pages
- Consistent risk-state highlighting
- Adjustable font size
- Optional OpenDyslexic font
- Clear navigation
- First-time user tutorial
- Tutorial access through Settings
- Simple visual summaries
- Colour-coded risk information

The OpenDyslexic font is offered as an optional preference rather than being presented as universally more accessible.

---

# Project Structure

The project is separated into modular components.

A simplified structure is shown below:

```text
Phronesis/
│
├── app.py
├── app_data.py
├── authenticate.py
├── assessment_adapter.py
├── attendance_adapter.py
├── model_adapter.py
│
├── data_management/
│   ├── assessments.py
│   ├── attendance.py
│   ├── classes.py
│   ├── students.py
│   └── subjects.py
│
├── pages/
│
├── styles/
│
├── models/
│   └── final_random_forest_2b.joblib
│
├── notebooks/
│   └── 01_eda.ipynb
│
├── data/
│
├── outputs/
│
├── requirements.txt
├── README.md
│
└── report_documents/
```

---

# Supporting Project Documents

The `report_documents` folder contains supporting evidence produced during the project.

Suggested contents:

```text
report_documents/
│
├── development_log.xlsx
├── testing_log.xlsx
├── functional_requirements.xlsx
├── questionnaire_results.pdf
├── interview_notes.pdf
└── README.md
```

## `development_log.xlsx`

Contains a chronological record of development work, including:

- Model experimentation
- Feature engineering
- Application development
- Bugs
- Fixes
- Design changes
- Testing
- Final implementation decisions

## `testing_log.xlsx`

Contains functional, validation, integration and edge-case testing carried out during development.

## `functional_requirements.xlsx`

Contains project requirements and requirement priorities used during design and development.

## `questionnaire_results`

Contains anonymised results from the final user evaluation.

Only responses with appropriate consent were included in the final project analysis.

## `interview_notes`

Contains anonymised notes from follow-up user interviews used during evaluation.

---

# Evaluation

Phronesis was evaluated using both technical and user-based methods.

Technical evaluation included:

- Model experimentation
- Cross-validation
- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- Average Precision
- Holdout testing
- Functional testing
- Integration testing
- Validation testing
- Incomplete-data testing
- Edge-case testing

User evaluation included:

- Task-based prototype testing
- Questionnaire responses
- Follow-up interviews
- Accessibility feedback

The final evaluation also considered limitations, usability issues and possible future improvements.

**For detailed machine-learning experimentation and evaluation evidence, the notebook in `notebooks/01_eda.ipynb` should also be reviewed.**

---

# Dataset

The machine-learning model was developed using the UCI Student Performance dataset.

The dataset includes student performance and contextual educational variables.

The final Phronesis model uses an engineered subset of information based mainly on:

- Previous assessment failure
- Absences
- Recent grade average
- Recent grade change

The dataset was used for academic project purposes.

Please refer to the project report, notebook and repository documentation for full dataset attribution and details of the data-processing process.

---

# Important Limitations

Phronesis is an academic prototype.

It is not intended for immediate production use within a real school.

Important limitations include:

- The model was trained using the UCI Portuguese Student Performance dataset.
- The model has not been validated using a large representative UK school dataset.
- Holdout testing showed that false positives and false negatives still occur.
- Recent assessment performance has a strong influence on predictions.
- Recommendations are rule-based.
- Recommendations have not been validated against long-term classroom outcomes.
- Behaviour and homework are contextual information rather than Random Forest prediction features.
- The current CSV-based storage system is suitable for prototype development but not production school infrastructure.
- The authentication implementation is prototype-level and should not be treated as production-grade security.
- Accessibility evaluation was limited.
- The user evaluation sample was relatively small.
- The application has not been deployed with real sensitive school data.

---

# Intended Use

Phronesis should be treated as a teacher decision-support system.

It is designed to:

- Highlight potentially concerning patterns
- Help teachers review student information
- Provide contextual indicators
- Suggest possible next steps

It is not designed to:

- Replace teacher professional judgement
- Automatically determine interventions
- Make final decisions about students
- Replace an existing school Management Information System

---

# Future Development

Possible future improvements include:

- Validation using a larger UK school dataset
- Production-grade database storage
- Stronger authentication and security
- MIS integration
- Intervention tracking
- Teacher notes
- Student progress graphs
- Improved dashboard filtering
- Improved mobile responsiveness
- Improved accessibility testing
- Additional contextual student data
- Further validation of recommendation strategies
- Exportable student summaries

---

# Academic Project

This repository was produced as part of the:

**University of London BSc Computer Science**

**CM3070 Final Project**

Project:

**Phronesis – Educational Decision Support for Teachers**

Template:

**CM3005 Data Science 1.1 Project Idea 1: Data-Driven Personalised Educational Content Recommendation**

---

# Author

Final-year University of London BSc Computer Science project.

---

# Disclaimer

Phronesis is a research and academic prototype.

Any predictions, contextual insights or recommendations produced by the application should be interpreted by a qualified education professional and should not be used as the sole basis for decisions affecting a student.