#Add assessment data
#imports
import streamlit as st
import pandas as pd

def show_assessments():
    st.subheader("Assessments")
    st.write("Add, view and manage assessment results.")

    #read assessment,class,subject,student and class-student data
    assessments =pd.read_csv("data/new/assessment.csv")
    classes =pd.read_csv("data/new/classes.csv")
    subjects =pd.read_csv("data/new/subjects.csv")
    students =pd.read_csv("data/new/students.csv")
    class_students =pd.read_csv("data/new/class_students.csv")

    ##########SUCCESS MESSAGES##########

    #add assessment
    if "assessment_message" in st.session_state:
        st.success(st.session_state["assessment_message"])
        del st.session_state["assessment_message"]

    #delete
    if "delete_assessment_message" in st.session_state:
        st.success(st.session_state["delete_assessment_message"])
        del st.session_state["delete_assessment_message"]

    #update
    if "update_assessment_message" in st.session_state:
        st.success(st.session_state["update_assessment_message"])
        del st.session_state["update_assessment_message"]

    #upload csv
    if "assessment_upload_message" in st.session_state:
        st.success(st.session_state["assessment_upload_message"])
        del st.session_state["assessment_upload_message"]

    ##########ADD ASSESSMENT##########
    @st.dialog("Add Assessment")
    def add_assessment_dialog(assessments,classes,subjects,students,class_students):
        st.write("Enter the assessment result below.")

        #no classes exist for year? flag error
        if len(classes) ==0:
            st.warning("Please create a class before adding assessments.")
            return

        #class option-name + id
        class_options =[]

        #get class options 
        for index,class_row in classes.iterrows():
            class_option =(class_row["class_name"]+" - "+class_row["class_id"])
            class_options.append(class_option)

        #choose class
        selected_class =st.selectbox("Class",class_options)

        #get selected class id
        selected_class_id =selected_class.split(" - ")[-1]

        #get selected class data
        selected_class_data =classes[classes["class_id"] ==selected_class_id]

        #if selected class does not exist
        if len(selected_class_data) ==0:
            st.error("The selected class no longer exists.")
            return

        selected_class_data =selected_class_data.iloc[0]

        #get subject id from class
        subject_id =selected_class_data["subject_id"]

        #get matching subject
        selected_subject =subjects[subjects["subject_id"] ==subject_id]

        #if subject does not exist
        if len(selected_subject) ==0:
            st.error("The subject linked to this class no longer exists. Please update the class.")
            return

        #get subject name
        subject_name =selected_subject["subject_name"].iloc[0]

        #prefill subject name
        st.write(f"Subject: **{subject_name}**")

        ##########GETTING STUDENTS IN THAT SPECIFIC CLASS##########
        #student ids belonging to selected class
        student_ids =class_students[class_students["class_id"] ==selected_class_id]["student_id"].tolist()

        #students belonging to selected class
        available_students =students[students["student_id"].isin(student_ids)].copy()

        #if no students in class
        if len(available_students) ==0:
            st.warning("No students have been added to this class.")
            return

        #student options-name + id
        available_students["student_option"] =(available_students["name"] +" - " +available_students["student_id"])

        #selection box for choosing students for that specific class
        selected_student =st.selectbox("Student",available_students["student_option"])

        #get student id
        student_id =selected_student.split(" - ")[-1]

        ##########ASSESSMENT DETAILS##########
        assessment_title =st.text_input("Assessment Title")
        assessment_date =st.date_input("Assessment Date",max_value="today")
        max_score =st.number_input("Maximum Score",min_value=1.0,step=1.0)
        #max score-whatever was defined above
        score =st.number_input("Student Score", min_value=0.0,max_value=float(max_score),step=1.0)
        pass_mark =st.number_input("Pass Mark", min_value=0.0,max_value=float(max_score),step=1.0)

        #if add button clicked
        if st.button("Add Assessment",type="primary"):
            #remove whitespace
            assessment_title =assessment_title.strip()
            #empty title?-check and flag error
            if assessment_title =="":
                st.error("Assessment name is required.")

            else:
                #does assessment already exist for student?
                duplicate_assessment =((assessments["student_id"] ==student_id)&
                    (assessments["subject"].str.lower()==subject_name.lower())&
                    (assessments["assessment_title"].str.lower()==assessment_title.lower())&
                    (pd.to_datetime(assessments["assessment_date"]).dt.date==assessment_date)).any()

                #duplicate?-flag error
                if duplicate_assessment:
                    st.error("This assessment result already exists for this student.")

                else:
                    #add new assessment to dataframe
                    new_assessment =pd.DataFrame(
                        {
                            "student_id":[student_id],
                            "subject":[subject_name],
                            "assessment_title":[assessment_title],
                            "assessment_date":[assessment_date],
                            "score":[score],
                            "max_score":[max_score],
                            "pass_mark":[pass_mark]
                        }
                    )

                    #add assessment
                    assessments =pd.concat([assessments,new_assessment],ignore_index=True)

                    #save assessments
                    assessments.to_csv("data/new/assessment.csv",index=False)

                    #save success message
                    st.session_state["assessment_message"] ="Assessment added successfully!"
                    st.rerun()

    #button which opens add assessment box
    if st.button("Add Assessment"):
        add_assessment_dialog(assessments,classes,subjects,students,class_students)

    ##########DOWNLOAD ASSESSMENT TEMPLATE##########
    #empty template with assessment csv headers
    assessment_template =pd.DataFrame(columns=["student_id","class_name","assessment_title","assessment_date","score","max_score","pass_mark"])

    #turn template into csv
    assessment_template_csv =assessment_template.to_csv(index=False)

    #download template button
    st.download_button("Download Assessment Template",data=assessment_template_csv,file_name="assessment_template.csv",mime="text/csv")

    ##########UPLOAD ASSESSMENT CSV##########
    @st.dialog("Upload Assessment CSV")
    def upload_assessment_csv(assessments,classes,subjects,students,class_students):
        st.write("Upload a completed assessment template.")
        #nice box
        st.info("Assessment dates should be entered as YYYY-MM-DD.")

        #must be csv
        uploaded_file =st.file_uploader("Choose Assessment CSV",type=["csv"])

        #if file uploaded- read and show preview
        if uploaded_file is not None:
            #read uploaded csv
            uploaded_assessments =pd.read_csv(uploaded_file)

            #show uploaded data
            st.write("### Preview")
            st.dataframe(uploaded_assessments,use_container_width=True,hide_index=True)

            if st.button("Upload Assessments",type="primary"):
                ##########VALIDATE CSV##########
                #columns needed
                required_columns =["student_id","class_name","assessment_title","assessment_date","score","max_score","pass_mark"]

                #missing columns list- if any needed columns missing-flag error
                missing_columns =[]
                for column in required_columns:
                    if column not in uploaded_assessments.columns:
                        missing_columns.append(column)

                #missing columns?-flag error
                if missing_columns:
                    st.error(f"Missing required columns: {missing_columns}")
                    return

                #if csv has no rows
                if len(uploaded_assessments) ==0:
                    st.error("The uploaded file contains no assessment records.")
                    return

                #check missing values
                missing_values =uploaded_assessments[required_columns].isna().any().any()

                if missing_values:
                    st.error("The uploaded file contains missing required values.")
                    return

                ##########REMOVE WHITESPACE##########
                uploaded_assessments["student_id"] =(uploaded_assessments["student_id"].astype(str).str.strip())
                uploaded_assessments["class_name"] =(uploaded_assessments["class_name"].astype(str).str.strip())
                uploaded_assessments["assessment_title"] =(uploaded_assessments["assessment_title"].astype(str).str.strip())

                #check empty text fields
                empty_values =(
                    (uploaded_assessments["student_id"] =="")|
                    (uploaded_assessments["class_name"] =="")|
                    (uploaded_assessments["assessment_title"] =="")
                )

                if empty_values.any():
                    st.error("Student ID, class name and assessment title cannot be empty.")
                    return

                ##########CHECK NUMBER VALUES##########
                numeric_columns =["score","max_score","pass_mark"]

                #convert number columns
                for column in numeric_columns:
                    uploaded_assessments[column] =pd.to_numeric(uploaded_assessments[column],errors="coerce")

                #check number conversion worked
                invalid_numbers =uploaded_assessments[numeric_columns].isna().any().any()

                if invalid_numbers:
                    st.error("Score, maximum score and pass mark must contain numbers.")
                    return

                ##########CHECK SCORE VALUES##########
                #max score should be greater than zero
                invalid_max_score =(uploaded_assessments["max_score"] <=0).any()

                if invalid_max_score:
                    st.error("Maximum score must be greater than 0.")
                    return

                #score cant be negative
                negative_score =(uploaded_assessments["score"] <0).any()

                if negative_score:
                    st.error("Student score cannot be negative.")
                    return

                # FIX! score cant be higher than max score
                score_above_maximum =(uploaded_assessments["score"]  >
                                      uploaded_assessments["max_score"]).any()


                if score_above_maximum:
                    st.error("Student score cannot be greater than maximum score.")
                    return

                #pass mark cant be negative
                negative_pass_mark =(uploaded_assessments["pass_mark"] <0).any()

                if negative_pass_mark:
                    st.error("Pass mark cannot be negative.")
                    return

                #FIX! score cant be higher than max score
                pass_mark_above_maximum =(uploaded_assessments["pass_mark"]  >
                                          uploaded_assessments["max_score"]).any()

                if pass_mark_above_maximum:
                    st.error("Pass mark cannot be greater than maximum score.")
                    return

                ##########CHECK DATES##########
                #convert dates
                uploaded_assessments["assessment_date"] =pd.to_datetime(
                    uploaded_assessments["assessment_date"],
                    errors="coerce"
                )

                #invalid date?-flag error
                invalid_dates =uploaded_assessments["assessment_date"].isna().any()

                if invalid_dates:
                    st.error("One or more assessment dates are invalid.")
                    return

                # FIX! date cant be higher than current date
                future_dates =(uploaded_assessments["assessment_date"] >
                               pd.Timestamp.today().normalize()).any()

                if future_dates:
                    st.error("Assessment date cannot be in the future.")
                    return

                ##########CHECK STUDENTS##########
                #students that dont exist- if needed colomns missing- flag error
                missing_students =[]

                #loop through uploaded students and see if exist in existing students
                for student_id in uploaded_assessments["student_id"]:
                    student_exists =(student_id in students["student_id"].values)

                    #if subject does not exist-add to missing list
                    if not student_exists:
                        if student_id not in missing_students:
                            missing_students.append(student_id)

                #missing students?-stop upload
                if missing_students:
                    st.error(f"These students do not exist: {missing_students}")
                    return

                ##########CHECK CLASSES##########
                #classes that dont exist- if needed colomns missing- flag error
                missing_classes =[]

                #loop through uploaded classes and see if exist in existing classes
                for class_name in uploaded_assessments["class_name"]:
                    class_exists =(class_name.lower()
                        in classes["class_name"].str.lower().values)

                    if not class_exists:
                        if class_name not in missing_classes:
                            missing_classes.append(class_name)

                #missing classes?-stop upload
                if missing_classes:
                    st.error(f"These classes do not exist: {missing_classes}. Please create them first.")
                    return

                ##########CHECK STUDENTS BELONG TO CLASSES##########
                #students that dont exist- if needed colomns missing- flag error
                class_errors =[]

                #loop through uploaded assessment-see if student belongs to class
                for index,assessment_row in uploaded_assessments.iterrows():
                    student_id =assessment_row["student_id"]
                    class_name =assessment_row["class_name"]

                    #get selected class
                    selected_class =classes[classes["class_name"].str.lower()
                                            == class_name.lower()]

                    class_id =selected_class["class_id"].iloc[0]

                    #does student belong to class
                    student_in_class =(
                        (class_students["class_id"]==class_id)  &
                        (class_students["student_id"]==student_id)                    ).any()

                    #student not in class?-store error
                    if not student_in_class:
                        error =(student_id + " - " + class_name)

                        if error not in class_errors:
                            class_errors.append(error)

                #class errors?-stop upload
                if class_errors:
                    st.error(f"These students are not assigned to the selected classes: {class_errors}")
                    return

                ##########CHECK SUBJECT LINKS##########
                subject_errors =[]

                #loop through uploaded assessment-see if class has valid subject link
                for index,assessment_row in uploaded_assessments.iterrows():
                    class_name =assessment_row["class_name"]

                    #get class
                    selected_class =classes[ classes["class_name"].str.lower()==class_name.lower()]
                    subject_id =selected_class["subject_id"].iloc[0]

                    #check subject exists
                    selected_subject =subjects[subjects["subject_id"]==subject_id]

                    #subject not exist?-store error
                    if len(selected_subject) ==0:
                        if class_name not in subject_errors:
                            subject_errors.append(class_name)

                #class errors?-stop upload
                if subject_errors:
                    st.error(f"These classes do not have a valid subject: {subject_errors}. Please update the classes first.")
                    return

                ##########CREATE ASSESSMENT RECORDS##########
                new_assessments =[]
                duplicate_errors =[]

                #go through uploaded assessment rows
                for index,assessment_row in uploaded_assessments.iterrows():
                    student_id =assessment_row["student_id"]
                    class_name =assessment_row["class_name"]
                    assessment_title =assessment_row["assessment_title"]
                    assessment_date =assessment_row["assessment_date"]
                    score =assessment_row["score"]
                    max_score =assessment_row["max_score"]
                    pass_mark =assessment_row["pass_mark"]

                    #get selected class
                    selected_class =classes[classes["class_name"].str.lower()
                                    ==class_name.lower()]
                    #get subject id
                    subject_id =selected_class["subject_id"].iloc[0]

                    #get subject name
                    selected_subject =subjects[subjects["subject_id"]
                                    ==subject_id]
                    subject_name =selected_subject["subject_name"].iloc[0]
                    ##########CHECK EXISTING DUPLICATE##########
                    existing_duplicate =(
                        (assessments["student_id"]==student_id)
                        &
                        (assessments["subject"].str.lower()==subject_name.lower())
                        &
                        (assessments["assessment_title"].str.lower()==assessment_title.lower())
                        &
                        (pd.to_datetime(assessments["assessment_date"]).dt.date
                            ==assessment_date.date())).any()

                    ##########CHECK DUPLICATE IN UPLOAD##########
                    uploaded_duplicate =False
                    for new_assessment in new_assessments:
                        if(new_assessment["student_id"]==student_id
                            and
                            new_assessment["subject"].lower()==subject_name.lower()
                            and
                            new_assessment["assessment_title"].lower()==assessment_title.lower()
                            and
                            pd.to_datetime(new_assessment["assessment_date"]).date()==assessment_date.date()):
                            uploaded_duplicate =True

                    #duplicate?-store error
                    if existing_duplicate or uploaded_duplicate:
                        duplicate_error =(student_id +" - "+assessment_title)

                        if duplicate_error not in duplicate_errors:
                            duplicate_errors.append(duplicate_error )

                    else:
                        #store assessment
                        new_assessments.append(
                            {
                                "student_id":student_id,
                                "subject":subject_name,
                                "assessment_title":assessment_title,
                                "assessment_date":assessment_date.date(),
                                "score":score,
                                "max_score":max_score,
                                "pass_mark":pass_mark
                            }
                        )

                #duplicates?-stop whole upload
                if duplicate_errors:
                    st.error(f"These assessment results already exist: {duplicate_errors}")
                    return

                #if nothing to add
                if len(new_assessments) ==0:
                    st.warning("No new assessments were found.")
                    return

                #turn new assessments into dataframe
                new_assessments =pd.DataFrame(new_assessments)

                #add uploaded assessments
                assessments =pd.concat([assessments,new_assessments],ignore_index=True)

                #save assessments
                assessments.to_csv("data/new/assessment.csv", index=False)
                #save success message
                st.session_state["assessment_upload_message"] =(f"{len(new_assessments)} assessments uploaded successfully!")
                st.rerun()

    #button which opens upload assessment box
    if st.button("Upload Assessment CSV"):
        upload_assessment_csv(assessments,classes,subjects,students,class_students)

    ##########DELETE ASSESSMENT##########
    #pop-up window to confirm delete assessment
    @st.dialog("Delete Assessment")
    def confirm_delete_assessment(assessments,selected_assessment_index,selected_assessment_title):
        st.warning(f"Are you sure you want to delete {selected_assessment_title}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #remove selected assessment
                assessments =assessments.drop(selected_assessment_index).reset_index(drop=True)

                #save
                assessments.to_csv("data/new/assessment.csv",index=False)
                st.session_state["delete_assessment_message"] ="Assessment deleted successfully!"
                st.rerun()


        #NO button column 2
        with col2:
            if st.button("Cancel",use_container_width=True):
                st.rerun()

    ##########VIEW ASSESSMENTS##########
    #bold
    st.write("### Current Assessments")

    #if no assessments added
    if len(assessments) ==0:
        st.info("No assessments have been added yet.")

    else:
        assessment_display =assessments.copy()

        #add student name to table
        assessment_display =assessment_display.merge(students[["student_id","name"]],
                                                    on="student_id",how="left")

        #only show useful columns
        assessment_display =assessment_display[
            [
                "student_id",
                "name",
                "subject",
                "assessment_title",
                "assessment_date",
                "score",
                "max_score",
                "pass_mark"
            ]
        ]

        #choose assessment directly from table
        assessment_table =st.dataframe(assessment_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row")

        ##########SELECTED ASSESSMENT##########
        #get selected rows
        selected_rows =assessment_table.selection.rows

        #assessment selected? options to edit delete
        if len(selected_rows) >0:
            #get selected row
            selected_row =selected_rows[0]

            #get selected assessment
            selected_assessment =assessments.iloc[selected_row]
            selected_assessment_index =assessments.index[selected_row]
            selected_assessment_title =selected_assessment["assessment_title"]
            selected_student_id =selected_assessment["student_id"]

            #get current student
            selected_student =students[students["student_id"]==selected_student_id]

            #if student still exists
            if len(selected_student) >0:
                selected_student_name =selected_student["name"].iloc[0]

            else:
                selected_student_name =(selected_student_id + " - Student no longer exists")

            st.write("### Manage Selected Assessment")
            #bold assessment
            st.write(f"Selected: **{selected_assessment_title} - {selected_student_name}**")

            ##########EDIT ASSESSMENT##########
            #input box-   prefill with current assessment name
            new_assessment_title =st.text_input("Assessment Title", value=selected_assessment_title)

            #convert saved date into date
            current_date =pd.to_datetime(selected_assessment["assessment_date"]).date()

            #date- prefill with current assessment date,max value today
            new_assessment_date =st.date_input("Assessment Date",value=current_date,max_value="today")

            #number input- prefill with current max score, min value 1
            #CHECK!- max score higher than current score and pass mark!!!!!!!!!
            new_max_score =st.number_input("Maximum Score",
                min_value=1.0,
                value=float(selected_assessment["max_score"]),
                step=1.0)

            new_score =st.number_input("Student Score",
                min_value=0.0,
                max_value=float(new_max_score),
                value=min(float(selected_assessment["score"]),float(new_max_score)),
                step=1.0)

            new_pass_mark =st.number_input(
                "Pass Mark",
                min_value=0.0,
                max_value=float(new_max_score),
                #prefill with current pass mark,
                #saved pass mark higher than new max score? prefill with new max score
                value=min(float(selected_assessment["pass_mark"]),float(new_max_score)),
                step=1.0
            )

            #if update button clicked-remove whitespace,check empty
            if st.button("Update Assessment"):
                new_assessment_title =new_assessment_title.strip()

                #empty?-flag error
                if new_assessment_title =="":
                    st.error("Assessment title is required.")

                else:
                    #check if updated assessment would create duplicate
                    duplicate_assessment =(
                        (assessments["student_id"]==selected_student_id) 
                        &
                        (assessments["subject"].str.lower()
                         ==str(selected_assessment["subject"]).lower())  
                         &
                        (assessments["assessment_title"].str.lower()
                         ==new_assessment_title.lower()) 
                         &
                        (pd.to_datetime(assessments["assessment_date"]).dt.date
                         ==new_assessment_date)   
                         &
                        (assessments.index!=selected_assessment_index)).any()

                    #duplicate?-flag error
                    if duplicate_assessment:
                        st.error("This assessment result already exists for this student.")

                    else:
                        #update assessment data
                        assessments.loc[selected_assessment_index,"assessment_title"] =new_assessment_title
                        assessments.loc[selected_assessment_index,"assessment_date"] =new_assessment_date
                        assessments.loc[selected_assessment_index,"score"] =new_score
                        assessments.loc[selected_assessment_index,"max_score"] =new_max_score
                        assessments.loc[selected_assessment_index,"pass_mark"] =new_pass_mark

                        #save updated classes
                        assessments.to_csv("data/new/assessment.csv",index=False)
                        #save success message
                        st.session_state["update_assessment_message"] ="Assessment updated successfully."
                        st.rerun()

            ##########DELETE ASSESSMENT BUTTON##########
            #delete button only show when assessment selected
            if st.button("Delete Assessment",type="primary"):
                confirm_delete_assessment(assessments,selected_assessment_index,selected_assessment_title)