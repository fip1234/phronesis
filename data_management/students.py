#Add student data
#imports
import streamlit as st
import pandas as pd

def show_students():
    st.subheader("Students")
    st.write("Add, view and manage students.")

    #read student,class and class-student data
    students =pd.read_csv("data/new/students.csv")
    classes =pd.read_csv("data/new/classes.csv")
    class_students =pd.read_csv("data/new/class_students.csv")

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
            #remove whitespace
            student_name =student_name.strip()

            #empty?-check and flag error
            if student_name =="":
                st.error("Student name is required.")

            #no classes selected?-check
            elif len(selected_classes) ==0:
                st.error("Please select at least one class.")

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
                students.to_csv("data/new/students.csv",index=False)
                #save success message
                st.session_state["students_message"] ="Student added successfully!"
                st.rerun()

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
                class_students.to_csv("data/new/class_students.csv",index=False)

                #save success message
                st.session_state["student_message"] ="Student added successfully!"
                st.rerun()

    #button which opens add student box
    if st.button("Add Student"):
        add_student_dialog(students,classes,class_students)

    ##########DOWNLOAD STUDENT TEMPLATE##########
    #empty template with subject csv headers
    student_template =pd.DataFrame(columns=["name","year_group", "classes"])

    #turn template into csv
    student_template_csv =student_template.to_csv(index=False)

    #download template button
    st.download_button("Download Student Template",data=student_template_csv,file_name="student_template.csv",mime="text/csv")

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

                #remove whitespace class - string
                uploaded_students["classes"] =(uploaded_students["classes"].astype(str).str.strip())

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
                students.to_csv("data/new/students.csv",index=False)
                class_students.to_csv( "data/new/class_students.csv", index=False)
                #save success message
                st.session_state["student_upload_message"] =(f"{len(new_students)}  students uploaded successfully!")

                st.rerun()


    #button-upload student box
    if st.button("Upload Student CSV"):
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
                students.to_csv("data/new/students.csv",index=False)
                class_students.to_csv("data/new/class_students.csv",index=False)
                st.session_state["delete_student_message"] ="Student deleted successfully!"
                st.rerun()


        #NO button column 2
        with col2:
            if st.button("Cancel",use_container_width=True):
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
        student_table =st.dataframe(student_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row")

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

            st.write("### Manage Selected Student")
            #bold student
            st.write(f"Selected: **{selected_student_name}**")

            ##########EDIT STUDENT##########
            #input box-   prefill with current name
            new_student_name =st.text_input("Student Name",value=selected_student_name)

            #year group-   prefill with current year name
            new_year_group =st.number_input("Year Group",min_value=1,max_value=13,value=int(selected_year_group),step=1)

            #get classes for selected year group
            available_classes =classes[classes["year_group"] ==new_year_group].copy()

            #classes exist for year goup? yes-multiselect, no- flag error
            if len(available_classes) >0:
                #create class options
                available_classes["class_option"] =(available_classes["class_name"]+ " - " + available_classes["class_id"])

                #find students current classes
                current_class_ids =class_students[class_students["student_id"]==selected_student_id]["class_id"].tolist()

                #get current class options
                current_class_options =available_classes[available_classes["class_id"].isin(current_class_ids)]["class_option"].tolist()

                #choose classes
                selected_classes =st.multiselect("Classes",available_classes["class_option"],default=current_class_options)

            else:
                selected_classes =[]
                st.warning("No classes have been created for this year group.")

            #if update button clicked-remove whitespace,check empty
            if st.button("Update Student"):
                new_student_name =new_student_name.strip()

                #if empty-flag error
                if new_student_name =="":
                    st.error("Student name is required.")

                #no class selected?-flag error
                elif len(selected_classes) ==0:
                    st.error("Please select at least one class.")

                else:
                    #change name-update in dataframe with id
                    students.loc[students["student_id"] ==selected_student_id,"name"] =new_student_name

                    ##change year group-update in dataframe with id
                    students.loc[students["student_id"] ==selected_student_id,"year_group"] =new_year_group

                    #remove old class pairs for student
                    class_students =class_students[class_students["student_id"]!=selected_student_id].copy()

                    #add new selected class pair
                    for class_option in selected_classes:
                        #get class id
                        class_id =class_option.split(" - ")[-1]

                        #create new pair for class student pair
                        new_class_student =pd.DataFrame(
                            {
                                "class_id":[class_id],
                                "student_id":[selected_student_id]
                            }
                        )

                        #add pair
                        class_students =pd.concat([class_students,new_class_student],ignore_index=True)

                    #save updated students
                    students.to_csv("data/new/students.csv",index=False)

                    #save updated class student pairs
                    class_students.to_csv("data/new/class_students.csv",index=False)
                    st.session_state["update_student_message"] ="Student updated successfully."
                    st.rerun()

            ##########DELETE STUDENT BUTTON##########
            #delete button only show when student selected
            if st.button("Delete Student",type="primary"):
                confirm_delete_student(students,class_students,selected_student_id,selected_student_name)