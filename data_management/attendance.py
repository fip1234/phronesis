#Add info like students, classes, subjects
#imports
import streamlit as st
import pandas as pd

def show_attendance():
    st.subheader("Attendance")
    st.write("Add, view and manage student attendance.")

    #read attendance,student,class and class-student data
    attendance =pd.read_csv("data/new/attendance.csv")
    students =pd.read_csv("data/new/students.csv")
    classes =pd.read_csv("data/new/classes.csv")
    class_students =pd.read_csv("data/new/class_students.csv")

    ##########SUCCESS MESSAGES##########

    #add attendance
    if "attendance_message" in st.session_state:
        st.success(st.session_state["attendance_message"])
        del st.session_state["attendance_message"]

    #delete
    if "delete_attendance_message" in st.session_state:
        st.success(st.session_state["delete_attendance_message"])
        del st.session_state["delete_attendance_message"]

    #update
    if "update_attendance_message" in st.session_state:
        st.success(st.session_state["update_attendance_message"])
        del st.session_state["update_attendance_message"]

    #upload csv
    if "attendance_upload_message" in st.session_state:
        st.success(st.session_state["attendance_upload_message"])
        del st.session_state["attendance_upload_message"]


    ##########ADD ATTENDANCE##########
    @st.dialog("Add Attendance")
    def add_attendance_dialog(attendance,students,classes,class_students):
        st.write("Enter the student attendance below.")

        #no classes exist for year? flag error
        if len(classes) ==0:
            st.warning("Please create a class before adding attendance.")
            return

        ##########CHOOSE CLASS##########
        #create class options
        class_options =[]

        for index,class_row in classes.iterrows():
            class_option =(class_row["class_name"] + " - " + class_row["class_id"])
            class_options.append(class_option)

        #choose class
        selected_class =st.selectbox("Class",class_options)

        #get selected class id
        selected_class_id =selected_class.split(" - ")[-1]

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

        ##########ATTENDANCE DETAILS##########
        total_sessions =st.number_input("Total Sessions", min_value=1,step=1)
        sessions_attended =st.number_input("Sessions Attended",min_value=0,max_value=int(total_sessions),step=1)

        #if add button clicked
        if st.button("Add Attendance",type="primary"):
            #does student already has attendance data?
            attendance_exists =(attendance["student_id"] ==student_id ).any()

            #attendance already exists?-flag error
            if attendance_exists:
                st.error("Attendance already exists for this student. Please update the existing attendance record.")

            else:
                #add new attendance to dataframe
                new_attendance =pd.DataFrame(
                    {
                        "student_id":[student_id],
                        "total_sessions":[total_sessions],
                        "sessions_attended":[sessions_attended]
                    }
                )


                #add attendance
                attendance =pd.concat([attendance,new_attendance],ignore_index=True)

                #save attendance
                attendance.to_csv("data/new/attendance.csv",index=False)

                #save success message
                st.session_state["attendance_message"] ="Attendance added successfully!"
                st.rerun()

    #button which opens add attendance box
    if st.button("Add Attendance"):
        add_attendance_dialog(attendance,students,classes,class_students)

    ##########DOWNLOAD ATTENDANCE TEMPLATE##########
    #create empty template with correct headers
    attendance_template =pd.DataFrame(
        columns=["student_id","total_sessions","sessions_attended"])

    #turn template into csv
    attendance_template_csv =attendance_template.to_csv(index=False)

    #download template
    st.download_button("Download Attendance Template",data=attendance_template_csv,file_name="attendance_template.csv",mime="text/csv")

    ##########UPLOAD ATTENDANCE CSV##########
    @st.dialog("Upload Attendance CSV")
    def upload_attendance_csv(attendance,students):
        st.write("Upload a completed attendance template.")
        #nice box
        st.info("Enter one attendance record per student. Use the student's ID shown in the Students section.")

        #must be csv
        uploaded_file =st.file_uploader("Choose Attendance CSV",type=["csv"])

        #if file uploaded- read and show preview
        if uploaded_file is not None:
            #read uploaded csv
            uploaded_attendance =pd.read_csv(uploaded_file)

            #show uploaded data
            st.write("### Preview")
            st.dataframe(uploaded_attendance,use_container_width=True,hide_index=True)

            if st.button("Upload Attendance",type="primary"):
                ##########VALIDATE CSV##########
                #columns needed
                required_columns =["student_id", "total_sessions","sessions_attended"]

                #missing columns list- if any needed columns missing-flag error
                missing_columns =[]
                for column in required_columns:
                    if column not in uploaded_attendance.columns:
                        missing_columns.append(column )

                #missing columns?-flag error
                if missing_columns:
                    st.error(f"Missing required columns: {missing_columns}")
                    return


                #if csv has no rows
                if len(uploaded_attendance) ==0:
                    st.error("The uploaded file contains no assessment records.")
                    return

                #check missing values
                missing_values =uploaded_attendance[required_columns].isna().any().any()

                if missing_values:
                    st.error("The uploaded file contains missing required values.")
                    return

                ##########STUDENT ID##########
                #remove whitespace
                uploaded_attendance["student_id"] =(uploaded_attendance["student_id"].astype(str).str.strip())               

                #empty student id?
                empty_student_id =(uploaded_attendance["student_id"] =="").any()

                if empty_student_id:
                    st.error("Student ID cannot be empty.")
                    return

                ##########CHECK NUMBER VALUES##########
                numeric_columns =["total_sessions","sessions_attended"]

                #convert number columns
                for column in numeric_columns:
                    uploaded_attendance[column] =pd.to_numeric(uploaded_attendance[column],errors="coerce")

                #check number conversion worked
                invalid_numbers =uploaded_attendance[numeric_columns].isna().any().any()

                if invalid_numbers:
                    st.error("Score, maximum score and pass mark must contain numbers.")
                    return

                ##########CHECK WHOLE NUMBERS##########
                #do modulus to check if whole number
                invalid_total_sessions =(uploaded_attendance["total_sessions"] %1!=0).any()
                invalid_sessions_attended =(uploaded_attendance["sessions_attended"] %1!=0).any()

                if (invalid_total_sessions or invalid_sessions_attended):
                    st.error("Total sessions and sessions attended must be whole numbers.")
                    return

                ##########CHECK SESSION VALUES##########
                #total sessions should be greater than zero
                invalid_total =(uploaded_attendance["total_sessions"] <=0).any()

                if invalid_total:
                    st.error("Total sessions must be greater than 0.")
                    return

                #sessions cant be negative
                negative_attended =(uploaded_attendance["sessions_attended"] <0).any()

                if negative_attended:
                    st.error("Sessions attended cannot be negative.")
                    return

                #FIX! sessions attended cant be higher than total sessions!
                attended_above_total =(uploaded_attendance["sessions_attended"] >
                                        uploaded_attendance["total_sessions"]).any()

                if attended_above_total:
                    st.error("Sessions attended cannot be greater than total sessions.")
                    return

                ##########CHECK STUDENTS BELONG TO CLASSES##########
                #students that dont exist- if needed colomns missing- flag error
                missing_students =[]

                #loop through uploaded student ids- see exist in df
                for student_id in uploaded_attendance["student_id"]:
                    student_exists =(student_id in students["student_id"].values)

                    if not student_exists:
                        if student_id not in missing_students:
                            missing_students.append(student_id)

                #missing students?-stop upload
                if missing_students:
                    st.error(f"These students do not exist: {missing_students}")
                    return

                ##########FIX DUPLICATES IN UPLOAD##########
                duplicate_student_ids =[]

                #student ids that appear more than once 
                #keep=false-   flag all duplicates not just the first or last
                duplicated_rows =uploaded_attendance[uploaded_attendance["student_id"].duplicated(keep=False)]

                #store duplicate ids
                for student_id in duplicated_rows["student_id"]:
                    if student_id not in duplicate_student_ids:
                        duplicate_student_ids.append(student_id)

                #duplicates?-stop upload
                if duplicate_student_ids:
                    st.error(
                        f"These students appear more than once in the uploaded file: {duplicate_student_ids}")
                    return

                #########EXISTING ATTENDANCE ERRORS##########
                existing_attendance =[]

                #loop through uploaded student ids-see if already have attendance
                for student_id in uploaded_attendance["student_id"]:
                    attendance_exists =(attendance["student_id"]==student_id).any()

                    #student not existing- add to list of existing attendance
                    if attendance_exists:
                        if student_id not in existing_attendance:
                            existing_attendance.append(student_id)

                #existing attendance?-stop upload
                if existing_attendance:
                    st.error(f"Attendance already exists for these students: {existing_attendance}. Please update their existing attendance records instead.")
                    return

                ##########ADD ATTENDANCE##########
                #convert session values to integers
                uploaded_attendance["total_sessions"] =(uploaded_attendance["total_sessions"].astype(int))
                uploaded_attendance["sessions_attended"] =(uploaded_attendance["sessions_attended"].astype(int))


                #only keep columns used by attendance csv
                new_attendance =uploaded_attendance[
                    [
                        "student_id",
                        "total_sessions",
                        "sessions_attended"
                    ]
                ].copy()

                #add uploaded attendance
                attendance =pd.concat([attendance,new_attendance],ignore_index=True)

                #save attendance
                attendance.to_csv("data/new/attendance.csv",index=False)
                #save success message
                st.session_state["attendance_upload_message"] =(f"{len(new_attendance)} attendance records uploaded successfully!")
                st.rerun()

    #button which opens upload attendance box
    if st.button("Upload Attendance CSV"):
        upload_attendance_csv(attendance,students)

    ##########DELETE ATTENDANCE##########
    #pop-up window to confirm delete assessment
    @st.dialog("Delete Attendance")
    def confirm_delete_attendance(attendance,selected_student_id,selected_student_name):
        st.warning( f"Are you sure you want to delete the attendance data for {selected_student_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #remove selected attendance
                attendance =attendance[attendance["student_id"]!=selected_student_id].copy()

                #save
                attendance.to_csv("data/new/attendance.csv",index=False)
                st.session_state["delete_attendance_message"] ="Attendance deleted successfully!"
                st.rerun()

        #NO button column 2
        with col2:
            if st.button("Cancel",use_container_width=True):
                st.rerun()

    ##########VIEW ATTENDANCE##########
    #bold
    st.write("### Current Attendance")

    #if no attendance added
    if len(attendance) ==0:
        st.info("No attendance data has been added yet.")

    else:
        attendance_display =attendance.copy()

        #add student name to display table
        attendance_display =attendance_display.merge(students[["student_id","name"]],
                                                    on="student_id", how="left")

        #calculate attendance percentage for display
        attendance_display["attendance_percentage"] =(attendance_display["sessions_attended"] /
                                                        attendance_display["total_sessions"])*100

        #only show useful columns
        attendance_display =attendance_display[
            [
                "student_id",
                "name",
                "total_sessions",
                "sessions_attended",
                "attendance_percentage"
            ]
        ]

        #choose attendance directly from table
        attendance_table =st.dataframe(attendance_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row")

        ##########SELECTED ATTENDANCE##########
        #get selected rows
        selected_rows =attendance_table.selection.rows

        #attendance selected? options to edit delete
        if len(selected_rows) >0:
            #get selected row
            selected_row =selected_rows[0]


            #get selected student from display table
            selected_student_id =attendance_display.iloc[selected_row]["student_id"]
            selected_attendance =attendance_display.iloc[selected_row]["student_id"]
            selected_student =attendance_display.iloc[selected_row]["name"]

            #if student still exists
            if len(selected_student) >0:
                selected_student_name =selected_student["name"].iloc[0]

            else:
                selected_student_name =(selected_student_id + " - Student no longer exists")


            st.write( "### Manage Selected Attendance")
            #bold student
            st.write(f"Selected: **{selected_student_name}**")

            ##########EDIT ATTENDANCE##########
            #input box-   prefill with current assessment name
            new_total_sessions =st.number_input("Total Sessions", min_value=1,
                                                value=int(selected_attendance["total_sessions"]), step=1 )
            

            #make sure current attended does not go above new total sessions
            current_sessions_attended =min(int(selected_attendance["sessions_attended"]),
                                           int(new_total_sessions))

            #input box-prefill current sessions attended
            new_sessions_attended =st.number_input(
                "Sessions Attended",
                min_value=0,
                max_value=int(new_total_sessions),
                value=current_sessions_attended,
                step=1
            )

            #show calculated absences
            new_absences =(new_total_sessions - new_sessions_attended)

            #show calculated percentage
            new_attendance_percentage =(new_sessions_attended /
                                        new_total_sessions)*100

            st.write(f"Absences: **{new_absences}**")
            st.write(f"Attendance: **{new_attendance_percentage:.1f}%**")

            #if update button pressed
            if st.button("Update Attendance"):
                #update total sessions
                attendance.loc[attendance["student_id"] == selected_student_id, 
                               "total_sessions"] =new_total_sessions

                #update sessions attended
                attendance.loc[ attendance["student_id"] == selected_student_id,
                    "sessions_attended"] =new_sessions_attended

                #save attendance
                attendance.to_csv("data/new/attendance.csv",index=False)
                #save success message
                st.session_state["update_attendance_message"] ="Attendance updated successfully."
                st.rerun()

            ##########DELETE ATTENDANCE BUTTON##########
            #delete button only show when attendance selected
            if st.button("Delete Attendance",type="primary"):
                confirm_delete_attendance(attendance,selected_student_id,selected_student_name)