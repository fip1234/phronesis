#Add student data
#imports
import streamlit as st
import pandas as pd
from user_data import get_user_file

def show_students():
    st.subheader("Students")
    st.write("Add, view and manage students.")

    #read student,class and class-student data
    students =pd.read_csv(get_user_file("students.csv"))
    classes =pd.read_csv(get_user_file("classes.csv"))
    class_students =pd.read_csv(get_user_file("class_students.csv"))

    ##########SUCCESS MESSAGES##########

    #add student
    if "student_message" in st.session_state:
        st.success(st.session_state["student_message"])
        del st.session_state["student_message"]

    #delete
    if "delete_student_message" in st.session_state:
        st.success(st.session_state["delete_student_message"])
        del st.session_state["delete_student_message"]

    #update
    if "update_student_message" in st.session_state:
        st.success(st.session_state["update_student_message"])
        del st.session_state["update_student_message"]

    #upload csv
    if "student_upload_message" in st.session_state:
        st.success(st.session_state["student_upload_message"])
        del st.session_state["student_upload_message"]

    ##########ADD STUDENT##########
    @st.dialog("Add Student")
    def add_student_dialog(students,classes,class_students):
        st.write("Enter the new student below.")
        student_name =st.text_input("Student Name")

        #choose year group- max year 13
        year_group =st.number_input("Year Group",min_value=1,max_value=13,step=1)

        #get classes for selected year group
        available_classes =classes[classes["year_group"] ==year_group].copy()

        #no classes exist for year? flag error
        if len(available_classes) ==0:
            st.warning("No classes have been created for this year group.")
            selected_classes =[]
        else:
            #class option-name + id
            available_classes["class_option"] =(available_classes["class_name"] +" - " + available_classes["class_id"])

            #pick one or more classes-multiselect
            selected_classes =st.multiselect("Classes",available_classes["class_option"])

        #if add button clicked
        if st.button("Add Student",type="primary"):
            #!TEST FIX- get rid of more white spaces
            student_name =" ".join(student_name.split())

            #TEST FIX!---student not in two classes for same subject at once??
            selected_subject_ids =[]
            duplicate_subject =False

            for class_option in selected_classes:
                #get classid, selected class, subject id so duplicates checked 
                class_id =class_option.split(" - ")[-1]
                selected_class =classes[classes["class_id"] ==class_id]
                subject_id =selected_class["subject_id"].iloc[0]

                #same subject already selected?
                if subject_id in selected_subject_ids:
                    duplicate_subject =True
                else:
                    selected_subject_ids.append(subject_id)


            #empty?-check and flag error
            if student_name =="":
                st.error("Student name is required.")

            #no classes selected?-check
            elif len(selected_classes) ==0:
                st.error("Please select at least one class.")

            #test fix!- more than one class for the same subject
            elif duplicate_subject:
                st.error("A student cannot be assigned to more than one class for the same subject.")

            else:
                #find highest existing student id number
                highest_student_number =0

                #loop through students to find highest number
                #replace s with empty string,convert to int,compare to highest number
                for student_id in students["student_id"]:
                    student_number =int(student_id.replace("S",""))

                    #compare to highest number-if higher,set as new highest number
                    if student_number >highest_student_number:
                        highest_student_number =student_number

                #new student id +1
                new_student_number =highest_student_number +1

                #new id-three digits, leading zeros, prefix s
                student_id =("S"+str(new_student_number).zfill(3))

                #add new student to dataframe
                new_student =pd.DataFrame(
                    {
                        "student_id":[student_id],
                        "name":[student_name],
                        "year_group":[year_group]
                    }
                )

                #add student
                students =pd.concat([students,new_student],ignore_index=True)

                #save students
                students.to_csv(get_user_file("students.csv"),index=False)
                
                #deleted the rerun after saving students-test fix!

                ##########ADD STUDENT TO CLASSES##########
                #go through selected classes
                for class_option in selected_classes:
                    #get class id from option- split by - and take last part 
                    class_id =class_option.split(" - ")[-1]

                    #new class to dataframe
                    new_class_student =pd.DataFrame(
                        {
                            "class_id":[class_id],
                            "student_id":[student_id]
                        }
                    )

                    #add student to class  
                    class_students =pd.concat([class_students,new_class_student],ignore_index=True)

                #save classes student
                class_students.to_csv(get_user_file("class_students.csv"),index=False)

                #save success message
                st.session_state["student_message"] ="Student added successfully!"
                st.rerun()


    ##########DOWNLOAD STUDENT TEMPLATE##########
    #empty template with subject csv headers
    student_template =pd.DataFrame(columns=["name","year_group", "classes"])

    #turn template into csv
    student_template_csv =student_template.to_csv(index=False)

    ##########UPLOAD STUDENT CSV##########
    @st.dialog("Upload Student CSV")
    def upload_student_csv(students,classes,class_students):
        st.write("Upload a CSV file following the template. The file should contain the following columns: name, year_group, classes.")
        st.info("If a student belongs to more than one class, separate the class names with a semicolon. Example: 10A Maths;10B English")

        #must be csv
        uploaded_file =st.file_uploader("Choose Student CSV",type=["csv"])

        #if file uploaded- read and show preview
        if uploaded_file is not None:
            #read uploaded csv
            uploaded_students =pd.read_csv(uploaded_file)

            #show uploaded data
            st.write("### Preview")
            st.dataframe(uploaded_students,use_container_width=True,hide_index=True)

            if st.button("Upload Students",type="primary"):
                ##########VALIDATE CSV##########
                #columns needed for upload
                required_columns =["name", "year_group", "classes"]

                #missing columns list- if any needed columns missing-flag error
                missing_columns =[]
                for column in required_columns:
                    if column not in uploaded_students.columns:
                        missing_columns.append(column)

                #missing columns?-flag error
                if missing_columns:
                    st.error(f"Missing required columns: {missing_columns}")
                    return

                #remove missing class/subject rows
                uploaded_students =uploaded_students.dropna(subset=required_columns).copy()

                #remove whitespace student names - string
                uploaded_students["name"] =(uploaded_students["name"].astype(str).str.strip())

                #remove extra spaces inside student names
                uploaded_students["name"] =(uploaded_students["name"].str.split().str.join(" "))

                #test fix!-get rid of more whitespaces
                #remove whitespace class - string
                uploaded_students["classes"] =(uploaded_students["classes"].astype(str).str.strip())

                #test fix! get rid of whitespaces when someone enrolled to multiple classes
                #remove extra spaces inside each class name
                cleaned_classes =[]

                #loop through all classes, remove extra spaces
                for class_list in uploaded_students["classes"]:
                    class_names =class_list.split(";")
                    clean_class_names =[]

                    for class_name in class_names:
                        clean_class =" ".join(class_name.split())
                        clean_class_names.append(clean_class)

                    cleaned_classes.append(";".join(clean_class_names))
                uploaded_students["classes"] =cleaned_classes

                #year group to number for validation
                uploaded_students["year_group"] =pd.to_numeric(uploaded_students["year_group"],errors="coerce")

                #invalid year group- remove
                uploaded_students =uploaded_students[uploaded_students["year_group"].notna()].copy()

                #year group is between 1-13?
                valid_year_group =((uploaded_students["year_group"] >=1)&
                    (uploaded_students["year_group"] <=13))

                #upload valid year group rows to new dataframe
                uploaded_students =uploaded_students[valid_year_group].copy()

                #remove empty class or student names
                uploaded_students =uploaded_students[(uploaded_students["name"] !="")&
                                                     (uploaded_students["classes"] !="")].copy()

                #if no valid classes left after validation-flag error
                if len(uploaded_students) ==0:
                    st.error("No valid students were found in the uploaded file.")
                    return

                ##########CHECK CLASSES##########
                #store classes that do not exist
                missing_classes =[]

                #loop through uploaded students and see if exist in existing students
                for index,student_row in uploaded_students.iterrows():
                    #split class names using ;
                    class_names =student_row["classes"].split(";")

                    #go through each class
                    for class_name in class_names:
                        class_name =class_name.strip()
                        class_exists =(class_name.lower()in classes["class_name"].str.lower().values)

                        #if subject does not exist-add to missing list
                        if not class_exists:
                            if class_name not in missing_classes:
                                missing_classes.append(class_name)

                #missing classes?-stop upload
                if missing_classes:
                    st.error(f"These classes do not exist: {missing_classes}. Please create them first.")
                    return

                ##########CHECK YEAR GROUPS########## FIX
                #class year doesnt match student year-store
                year_group_errors =[]

                #go through uploaded students
                for index,student_row in uploaded_students.iterrows():
                    student_name =student_row["name"]

                    year_group =int(student_row["year_group"] )
                    class_names =student_row["classes"].split(";")

                    for class_name in class_names:
                        class_name =class_name.strip()
                        selected_class =classes[classes["class_name"].str.lower()==class_name.lower()]

                        class_year_group =int(selected_class["year_group"].iloc[0])

                        #class year matches student year?-if not, add to error list
                        if class_year_group !=year_group:
                            error =(student_name+" - " + class_name)

                            if error not in year_group_errors:
                                year_group_errors.append(error)

                #year group does not match?-stop upload
                if year_group_errors:
                    st.error(f"These students have been assigned to classes in a different year group: {year_group_errors}")
                    return

                ##########CHECK DOUBLE SAME SUBJECTS##########
                #test fix! get rid of whitespaces when someone enrolled to multiple classes
                #remove extra spaces inside each class name
                duplicate_subject_errors =[]

                #loop through all classes, remove extra spaces
                for index,student_row in uploaded_students.iterrows():
                    student_name =student_row["name"]
                    class_names =student_row["classes"].split(";")
                    #store subject ids already chosen for this student
                    selected_subject_ids =[]

                    #each class checked for duplicate subjects
                    for class_name in class_names:
                        class_name =class_name.strip()

                        #get classid, selected class, subject id so duplicates checked 
                        selected_class =classes[classes["class_name"].str.lower() ==class_name.lower()]
                        subject_id =selected_class["subject_id"].iloc[0]

                        #same subject already selected?
                        if subject_id in selected_subject_ids:
                            if student_name not in duplicate_subject_errors:
                                duplicate_subject_errors.append(student_name)

                        else:
                            selected_subject_ids.append(subject_id)

                #duplicate subject found?-stop upload
                if duplicate_subject_errors:
                    st.error(f"These students have been assigned to more than one class for the same subject: {duplicate_subject_errors}")
                    return


                ##########ADD STUDENTS##########
                #find highest existing student id number
                highest_student_number =0

                #loop through existing classes- get number from class_id (remove S)
                for student_id in students["student_id"]:
                    student_number =int(student_id.replace("S",""))

                    #compare to highest number
                    if student_number >highest_student_number:
                        highest_student_number =student_number

                #store new students
                new_students =[]

                #store new class to student pairs
                new_class_students =[]

                #go through uploaded students to add to existing students 
                for index,student_row in uploaded_students.iterrows():
                    student_name =student_row["name"]
                    year_group =int(student_row["year_group"])
                    class_names =student_row["classes"].split(";")

                    #loookup id
                    highest_student_number =highest_student_number +1

                    #next class id is highest number +1,stored with prefix c
                    student_id =("S"+str(highest_student_number).zfill(3))

                    #store new student
                    new_students.append(
                        {
                            "student_id":student_id,
                            "name":student_name,
                            "year_group":year_group
                        }
                    )

                    ##########ADD STUDENT TO CLASSES##########
                    #go through class names
                    for class_name in class_names:
                        class_name =class_name.strip()

                        #get class id from class name
                        selected_class =classes[classes["class_name"].str.lower()==class_name.lower()]

                       #loookup id 
                        class_id =selected_class["class_id"].iloc[0]

                        #store new class student pair
                        new_class_students.append(
                            {
                                "class_id":class_id,
                                "student_id":student_id
                            }
                        )


                #turn new students into dataframe
                new_students =pd.DataFrame(new_students)

                #turn new class student pair into dataframe
                new_class_students =pd.DataFrame(new_class_students)

                #add uploaded students
                students =pd.concat([students,new_students],ignore_index=True)

                #add uploaded class student pairs
                class_students =pd.concat([class_students,new_class_students],ignore_index=True)

                #####save
                students.to_csv(get_user_file("students.csv"),index=False)
                class_students.to_csv(get_user_file("class_students.csv"),index=False)
                #save success message
                st.session_state["student_upload_message"] =(f"{len(new_students)}  students uploaded successfully!")

                st.rerun()

    ##########STUDENT ACTIONS##########
    #main student buttons all in one row so neat
    with st.container(key="data_actions"):
        addCol,downloadCol,uploadCol,spaceCol =st.columns([1.4,1.8,1.4,4])

        with addCol:
            if st.button("＋ Add Student",key="add_student",use_container_width=True):
                add_student_dialog(students,classes,class_students)

        with downloadCol:
            st.download_button("Download Template",data=student_template_csv,file_name="student_template.csv",
                mime="text/csv",key="download_student_template",use_container_width=True)

        with uploadCol:
            if st.button("Upload CSV",key="upload_student_csv",use_container_width=True):
                upload_student_csv(students,classes,class_students)

    ##########DELETE STUDENT##########
    #pop-up window to confirm delete subject
    @st.dialog("Delete Student")
    def confirm_delete_student(students,class_students,selected_student_id,selected_student_name):
        st.warning(f"Are you sure you want to delete {selected_student_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #students is now dataframe without selected student
                students =students[students["student_id"] !=selected_student_id].copy()

                #remove student from classes alsoo
                class_students =class_students[class_students["student_id"] !=selected_student_id].copy()

                #save-student and class student pairs
                students.to_csv(get_user_file("students.csv"),index=False)
                class_students.to_csv(get_user_file("class_students.csv"),index=False)
                st.session_state["delete_student_message"] ="Student deleted successfully!"
                st.rerun()


        #NO button column 2
        with col2:
            if st.button("Cancel",use_container_width=True):
                st.rerun()
                
    ##########EDIT STUDENT##########
    #popup to edit selected student
    @st.dialog("Edit Student")
    def editStudentPopup(students,classes,class_students,selectedStudentId,selectedStudentName,selectedYearGroup):
        st.write(f"Update the details for **{selectedStudentName}**.")

        #student details input fields
        newStudentName =st.text_input("Student Name",value=selectedStudentName)
        newYearGroup =st.number_input("Year Group",min_value=1,max_value=13,value=int(selectedYearGroup),step=1)

        ##########AVAILABLE CLASSES##########
        #only show classes for selected year group
        availableClasses =classes[classes["year_group"] ==newYearGroup].copy()

        if len(availableClasses) >0:
            availableClasses["class_option"] =(availableClasses["class_name"] +" - "+ availableClasses["class_id"])

            #find students current classes
            currentClassIds =class_students[class_students["student_id"] ==selectedStudentId]["class_id"].tolist()

            #only preselect classes which still match year group
            currentClassOptions =availableClasses[availableClasses["class_id"].isin(currentClassIds)]["class_option"].tolist()

            selectedClasses =st.multiselect("Classes",availableClasses["class_option"],default=currentClassOptions)

        else:
            selectedClasses =[]
            st.warning("No classes have been created for this year group.")

        ##########BUTTONS##########
        cancelCol,saveCol =st.columns(2)

        with cancelCol:
            if st.button("Cancel",key="cancel_student_edit",use_container_width=True):
                st.rerun()

        with saveCol:
            if st.button("Save Changes",type="primary",key="save_student_edit",use_container_width=True):
                #get rid of extra spaces
                newStudentName =" ".join(newStudentName.split())

                #check same subject twice
                selectedSubjectIds =[]
                duplicateSubject =False

                for classOption in selectedClasses:
                    #get class id
                    classId =classOption.split(" - ")[-1]
                    selectedClass =classes[classes["class_id"] ==classId]
                    #get the subject id for this class
                    subjectId =selectedClass["subject_id"].iloc[0]

                    #same subject already selected?
                    if subjectId in selectedSubjectIds:
                        duplicateSubject =True
                    else:
                        selectedSubjectIds.append(subjectId)

                ##########ERROR CHECKING##########
                if newStudentName =="":
                    st.error("Student name is a required.")
                    return

                elif len(selectedClasses) ==0:
                    st.error("Please select at least one class.")
                    return

                elif duplicateSubject:
                    st.error("A student cannot be assigned to more than one class for the same subject.")
                    return

                #update name and year group
                students.loc[students["student_id"] ==selectedStudentId,"name"] =newStudentName
                students.loc[students["student_id"] ==selectedStudentId,"year_group"] =newYearGroup

                #remove old class links
                class_students =class_students[class_students["student_id"] !=selectedStudentId].copy()

                #add new class links
                for classOption in selectedClasses:
                    classId =classOption.split(" - ")[-1]
                    newClassStudent =pd.DataFrame({"class_id":[classId],"student_id":[selectedStudentId]})
                    class_students =pd.concat([class_students,newClassStudent],ignore_index=True)

                #save updates
                students.to_csv(get_user_file("students.csv"),index=False)
                class_students.to_csv(get_user_file("class_students.csv"),index=False)
                st.session_state["update_student_message"] ="Student updated successfully."
                st.rerun()

    ##########VIEW STUDENTS##########
    #bold
    st.write("### Current Students")

    #if no students added
    if len(students) ==0:
        st.info("No students have been added yet.")

    else:
        #so original not changed
        student_display =students.copy()

        #store class names for each student
        student_classes =[]

        #go through each student
        for student_id in student_display["student_id"]:

            #find class id and class names which student belongs to
            class_ids =class_students[class_students["student_id"] ==student_id]["class_id"].tolist()
            class_names =classes[classes["class_id"].isin(class_ids)]["class_name"].tolist()

            #join class names together
            class_names =", ".join(class_names)
            student_classes.append(class_names)

        #add classes to display table
        student_display["classes"] =student_classes

        #choose student directly from table
        #fix!-so it allows selecting a single student directly from table
        student_table =st.dataframe(student_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row",
        column_config={
            "student_id":st.column_config.TextColumn("Student ID"),
            "name":st.column_config.TextColumn("Student"),
            "year_group":st.column_config.NumberColumn("Year Group"),
            "classes":st.column_config.TextColumn("Classes")
        }
    )

        
        ##########SELECTED STUDENT##########
        #get selected rows
        selected_rows =student_table.selection.rows

        #class selected? options to edit delete
        if len(selected_rows) >0:
            #get selected row
            selected_row =selected_rows[0]

            #get selected student
            selected_student =students.iloc[selected_row]
            selected_student_id =selected_student["student_id"]
            selected_student_name =selected_student["name"]
            selected_year_group =selected_student["year_group"]

            ##########MANAGE SELECTED STUDENT##########
            #display selected students info -  give delete/edit options
            #better styling for selected student info
            with st.container(key="selected_record"):
                infoCol,editCol,deleteCol =st.columns([5,1.2,1.2])

                with infoCol:
                    st.write(f"Selected: **{selected_student_name}**")

                with editCol:
                    if st.button("Edit",key="edit_selected_student",use_container_width=True):
                        editStudentPopup(students,classes,class_students,selected_student_id,selected_student_name,selected_year_group)

                with deleteCol:
                    if st.button("Delete",type="primary",key="delete_selected_student",use_container_width=True):
                        confirm_delete_student(students,class_students,selected_student_id,selected_student_name)            
