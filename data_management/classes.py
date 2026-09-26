#classes.py- add class data for data upload and management
#imports
import streamlit as st
import pandas as pd
from user_data import get_user_file

def show_classes():
    st.subheader("Classes")
    st.write("Add, view and manage classes.")

    #read class and subject data
    classes =pd.read_csv(get_user_file("classes.csv"))
    subjects =pd.read_csv(get_user_file("subjects.csv"))
    class_students =pd.read_csv(get_user_file("class_students.csv"))

    ##########SUCCESS MESSAGES##########

    #add class
    if "class_message" in st.session_state:
        st.success(st.session_state["class_message"])
        del st.session_state["class_message"]

    #delete
    if "delete_class_message" in st.session_state:
        st.success(st.session_state["delete_class_message"])
        del st.session_state["delete_class_message"]

    #update
    if "update_class_message" in st.session_state:
        st.success(st.session_state["update_class_message"])
        del st.session_state["update_class_message"]

    #upload csv
    if "class_upload_message" in st.session_state:
        st.success(st.session_state["class_upload_message"])
        del st.session_state["class_upload_message"]

    ##########ADD CLASS##########
    @st.dialog("Add Class")
    def add_class_dialog(classes,subjects):
        st.write("Enter the new class below.")
        class_name =st.text_input("Class Name")

        #if no subject exist- flag error
        if len(subjects) ==0:
            st.warning("Please add a subject before creating a class.")
            return

        #choose subject
        subject_name =st.selectbox("Subject",subjects["subject_name"])

        #choose year group- max year 13
        year_group =st.number_input("Year Group",min_value=1,max_value=13,step=1)

        #if add button clicked
        if st.button("Add Class",type="primary"):
            #TEST FIX!-remove extra spaces
            class_name =" ".join(class_name.split())

            #TEST FIX- extra whitespaces from existing subjects removed
            existing_class_names =[]

            for existing_class in classes["class_name"]:
                clean_class =" ".join(existing_class.split()).lower()
                existing_class_names.append(clean_class)

            #empty?-check and flag error
            if class_name =="":
                st.error("Class name is required.")

            #TEST FIX! class already exist? check and flag error
            elif class_name.lower() in existing_class_names:
                st.error("This class already exists.")

            else:
                #get subject id from name and filter df by that name
                selected_subject =subjects[subjects["subject_name"] ==subject_name]
                subject_id =selected_subject["subject_id"].iloc[0]

                #find highest existing class id number
                highest_class_number =0

                #loop through classes to find highest number
                #replace c with empty string,convert to int,compare to highest number
                for class_id in classes["class_id"]:
                    class_number =int(class_id.replace("C",""))

                    #compare to highest number-if higher,set as new highest number
                    if class_number >highest_class_number:
                        highest_class_number =class_number

                #new class id +1
                new_class_number =highest_class_number +1

                #new id-three digits, leading zeros, s prefix
                class_id =("C"+str(new_class_number).zfill(3))

                #add new class to dataframe
                new_class =pd.DataFrame(
                    {
                        "class_id":[class_id],
                        "class_name":[class_name],
                        "subject_id":[subject_id],
                        "year_group":[year_group]
                    }
                )

                #add class
                classes =pd.concat([classes,new_class],ignore_index=True)

                #save classes
                classes.to_csv(get_user_file("classes.csv"),index=False)

                #save success message
                st.session_state["class_message"] ="Class added successfully!"
                st.rerun()


    ##########DOWNLOAD CLASS TEMPLATE##########
    #empty template with subject csv headers
    class_template =pd.DataFrame(columns=["class_name","subject_name","year_group"])

    #turn template into csv
    class_template_csv =class_template.to_csv(index=False)

    ##########UPLOAD CLASS CSV##########
    @st.dialog("Upload Class CSV")
    def upload_class_csv(classes,subjects):
        st.write("Upload a CSV file following the template.")
        #nice box
        st.info("The file should contain the following columns: class_name, subject_name, year_group.")

        #must be csv
        uploaded_file =st.file_uploader("Choose Class CSV",type=["csv"])

        #if file uploaded- read and show preview
        if uploaded_file is not None:
            #read uploaded csv
            uploaded_classes =pd.read_csv(uploaded_file)

            #show uploaded data
            st.write("### Preview")
            st.dataframe(uploaded_classes,use_container_width=True,hide_index=True)

            if st.button("Upload Classes",type="primary"):
                ##########VALIDATE CSV##########
                #columns needed for upload
                required_columns =["class_name", "subject_name", "year_group" ]

                #missing columns list- if any needed columns missing-flag error
                missing_columns =[]
                for column in required_columns:
                    if column not in uploaded_classes.columns:
                        missing_columns.append(column)

                #missing columns?-flag error
                if missing_columns:
                    st.error(f"Missing required columns: {missing_columns}")
                    return

                #remove missing class/subject rows
                uploaded_classes =uploaded_classes.dropna(subset=required_columns).copy()

                #remove whitespace class names - string
                uploaded_classes["class_name"] =(uploaded_classes["class_name"].astype(str).str.strip())
                #TEST FIX!- extra spaces removed from class names
                uploaded_classes["class_name"] =(uploaded_classes["class_name"].str.split().str.join(" "))

                #remove whitespace subject names - string
                uploaded_classes["subject_name"] =(uploaded_classes["subject_name"].astype(str).str.strip())

                #year group to number for validation
                uploaded_classes["year_group"] =pd.to_numeric(uploaded_classes["year_group"],errors="coerce")

                #invalid year group (not 1-13)-remove
                uploaded_classes =uploaded_classes[uploaded_classes["year_group"].notna()].copy()

                #year group is between 1-13?
                valid_year_group =((uploaded_classes["year_group"] >=1)&
                    (uploaded_classes["year_group"] <=13))

                #upload valid year group rows to new dataframe
                uploaded_classes =uploaded_classes[valid_year_group].copy()

                #remove empty class or subject names
                uploaded_classes =uploaded_classes[(uploaded_classes["class_name"] !="") &
                                                   (uploaded_classes["subject_name"] !="")].copy()

                #if no valid classes left after validation-flag error
                if len(uploaded_classes) ==0:
                    st.error("No valid classes were found in the uploaded file.")
                    return

                ##########CHECK SUBJECTS##########
                #subjects that dont exist- if needed colomns missing- flag error
                missing_subjects =[]

                #loop through uploaded subjects and see if exist in existing subjects
                for subject_name in uploaded_classes["subject_name"]:
                    subject_exists =(subject_name.lower()in subjects["subject_name"].str.lower().values)

                    #if subject does not exist-add to missing list
                    if not subject_exists:
                        if subject_name not in missing_subjects:
                            missing_subjects.append(subject_name)

                #missing subject?-stop upload
                if missing_subjects:
                    st.error(f"These subjects do not exist: {missing_subjects}. Please add them first.")
                    return

                ##########ADD CLASSES##########
                #find highest existing class id number
                highest_class_number =0

                #loop through existing classes- get number from class_id (remove c)
                for class_id in classes["class_id"]:
                    class_number =int( class_id.replace("C",""))

                    #compare to highest number
                    if class_number >highest_class_number:
                        highest_class_number =class_number

                #store new classes
                new_classes =[]

                #TEST FIX!-remove extra spaces from uploaded class names
                existing_class_names =[]

                for existing_class in classes["class_name"]:
                    clean_class =" ".join(existing_class.split()).lower()
                    existing_class_names.append(clean_class)

                
                #go through uploaded classes to add to existing classes 
                for index,class_row in uploaded_classes.iterrows():
                    class_name =class_row["class_name"]
                    subject_name =class_row["subject_name"]
                    year_group =int(class_row["year_group"])

                    #test fix! check class doesnt already exist (class_name already cleaned for whitespaces)
                    class_exists =(class_name.lower() in existing_class_names)

                    #check class was not already added from same upload
                    uploaded_duplicate =False

                    for new_class in new_classes:
                        if new_class["class_name"].lower() ==class_name.lower():
                            uploaded_duplicate =True

                    #only add new class
                    if not class_exists and not uploaded_duplicate:
                        #get subject id from subject name
                        selected_subject =subjects[subjects["subject_name"].str.lower()==subject_name.lower()]

                        #loookup id
                        subject_id =selected_subject["subject_id"].iloc[0]

                        #next class id is highest number +1,stored with prefix c
                        highest_class_number =highest_class_number +1
                        class_id =("C"+str(highest_class_number).zfill(3))

                        #store new class
                        new_classes.append(
                            {
                                "class_id":class_id,
                                "class_name":class_name,
                                "subject_id":subject_id,
                                "year_group":year_group
                            }
                        )

                #if every class already exists
                if len(new_classes) ==0:
                    st.warning("No new classes were added. All classes already exist.")
                    return

                #turn new classes into dataframe
                new_classes =pd.DataFrame(new_classes)

                #add uploaded classes
                classes =pd.concat([classes,new_classes],ignore_index=True)

                #####save
                classes.to_csv(get_user_file("classes.csv"),index=False)
                #save success message
                st.session_state["class_upload_message"] =(f"{len(new_classes)}  classes uploaded successfully!")

                st.rerun()

    ##########CLASS ACTIONS##########
    #main class buttons all in one section row
    with st.container(key="data_actions"):
        addCol,downloadCol,uploadCol,spaceCol =st.columns([1.4,1.8,1.4,4])

        #all add, download, upload buttons for classes
        with addCol:
            if st.button("＋ Add Class" , key="add_class", use_container_width=True):
                add_class_dialog(classes,subjects)

        with downloadCol:
            st.download_button("Download Template", data=class_template_csv,
                file_name="class_template.csv",mime="text/csv",
                key="download_class_template",use_container_width=True)

        with uploadCol:
            if st.button("Upload CSV", key="upload_class_csv",use_container_width=True):
                upload_class_csv(classes,subjects)

    ##########DELETE CLASS##########
    #pop-up window to confirm delete subject
    @st.dialog("Delete Class")
    def confirm_delete_class(classes,class_students,selected_class_id,selected_class_name):
        st.warning(f"Are you sure you want to delete {selected_class_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #test fix!- are students assigned to class?
                students_in_class =class_students[class_students["class_id"] ==selected_class_id]

                #if no students are assigned to the class
                if len(students_in_class) >0:
                    st.warning(f"There are {len(students_in_class)} students assigned to this class.")
                    st.info("Consider reassigning or removing these students before deleting the class.")

                else:
                    st.info("No students are assigned to this class.")
                    #class can be removed because no class assigned
                    classes =classes[classes["class_id"] !=selected_class_id].copy()

                    #save
                    classes.to_csv(get_user_file("classes.csv"),index=False)
                    st.session_state["delete_class_message"] ="Class deleted successfully!"
                    st.rerun()


        #NO button column 2
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.rerun()

    ##########EDIT CLASS##########
    #popup to edit selected class
    @st.dialog("Edit Class")
    def editClassPopup(classes,subjects,selectedClassId,selectedClassName,selectedSubjectId,selectedYearGroup):
        st.write(f"Update the details for **{selectedClassName}**.")

        ##current subject
        #get selected classes current subject
        selectedSubject =subjects[subjects["subject_id"] ==selectedSubjectId]

        #dropdown options for subjects
        subjectNames =subjects["subject_name"].tolist()

        #if current subject still exists
        if len(selectedSubject) >0:
            selectedSubjectName =selectedSubject["subject_name"].iloc[0]
            currentSubjectIndex =subjectNames.index(selectedSubjectName)

        else:
            selectedSubjectName =None
            currentSubjectIndex =0
            st.warning("The subject linked to this class no longer exists. Please choose a new subject.")

        #edit fields
        newClassName =st.text_input("Class Name",value=selectedClassName)
        newSubjectName =st.selectbox("Subject",subjectNames,index=currentSubjectIndex)
        newYearGroup =st.number_input("Year Group",min_value=1,max_value=13,value=int(selectedYearGroup),step=1)

        ##########BUTTONS##########
        #row for cancel, save buttons
        cancelCol,saveCol =st.columns(2)

        with cancelCol:
            if st.button("Cancel",key="cancel_class_edit",use_container_width=True):
                st.rerun()

        with saveCol:
            if st.button("Save Changes",type="primary",key="save_class_edit",use_container_width=True):
                #remove extra spaces
                newClassName =" ".join(newClassName.split())

                #check duplicate
                #get other class names so current one doesnt count as duplicate
                otherClasses =classes[classes["class_id"] !=selectedClassId]
                existingClassNames =[]

                for existingClass in otherClasses["class_name"]:
                    cleanClass =" ".join(existingClass.split()).lower()
                    existingClassNames.append(cleanClass)

                if newClassName =="":
                    st.error("Class name is required.")
                    return

                elif newClassName.lower() in existingClassNames:
                    st.error("This class already exists.")
                    return

                ##########UPDATE CLASS##########
                #chosen subject id
                newSubject =subjects[subjects["subject_name"] ==newSubjectName]
                newSubjectId =newSubject["subject_id"].iloc[0]

                #update class name, subject, year group
                classes.loc[classes["class_id"] ==selectedClassId,"class_name"] =newClassName
                classes.loc[classes["class_id"] ==selectedClassId,"subject_id"] =newSubjectId
                classes.loc[classes["class_id"] ==selectedClassId,"year_group"] =newYearGroup

                #save changes
                classes.to_csv(get_user_file("classes.csv"),index=False)
                st.session_state["update_class_message"] ="Class updated successfully."
                st.rerun()


    ##########VIEW CLASSES##########
    #bold
    st.write("### Current Classes")

    #if no classes added
    if len(classes) ==0:
        st.info("No classes have been added yet.")

    else:
        #attach subject name to class table
        class_display =classes.merge(subjects[["subject_id","subject_name"]],
                                            on="subject_id", how="left")

        #only show useful columns
        class_display =class_display[
            [
                "class_id",
                "class_name",
                "subject_name",
                "year_group"
            ]
        ]

        #choose class directly from table-edit so added selection_mode="single-row"
        class_table =st.dataframe(class_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row",
            column_config={
                "class_id":st.column_config.TextColumn("Class ID"),
                "class_name":st.column_config.TextColumn("Class"),
                "subject_name":st.column_config.TextColumn("Subject"),
                "year_group":st.column_config.NumberColumn("Year Group")
            }
        )

        ##########SELECTED CLASS##########
        #get selected rows
        selected_rows =class_table.selection.rows

        #class selected? options to edit delete
        if len(selected_rows) >0:
            #get selected row
            selected_row =selected_rows[0]

            #get selected class
            selected_class =classes.iloc[selected_row]
            selected_class_id =selected_class["class_id"]
            selected_class_name =selected_class["class_name"]
            selected_subject_id =selected_class["subject_id"]
            selected_year_group =selected_class["year_group"]

            #######MANAGE SELECTED CLASS###############
            with st.container(key="selected_record"):
                #5=info, 1.2=edit, 1.2=delete column width ratio
                infoCol,editCol,deleteCol =st.columns([5,1.2,1.2])

                with infoCol:
                    st.write(f"Selected: **{selected_class_name}**")

                with editCol:
                    if st.button("Edit",key="edit_selected_class",use_container_width=True):
                        editClassPopup(classes,subjects,selected_class_id,selected_class_name,selected_subject_id,selected_year_group)

                with deleteCol:
                    if st.button("Delete",type="primary",key="delete_selected_class",use_container_width=True):
                        confirm_delete_class(classes,class_students,selected_class_id,selected_class_name)