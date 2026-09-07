#Add class data
#imports
import streamlit as st
import pandas as pd

def show_classes():
    st.subheader("Classes")
    st.write("Add, view and manage classes.")

    #read class and subject data
    classes =pd.read_csv("data/new/classes.csv")
    subjects =pd.read_csv("data/new/subjects.csv")

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
            #remove whitespace
            class_name =class_name.strip()

            #empty?-check and flag error
            if class_name =="":
                st.error("Class name is required.")

            #class already exist? check and flag error
            elif class_name.lower() in classes["class_name"].str.lower().values:
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
                classes.to_csv("data/new/classes.csv",index=False)

                #save success message
                st.session_state["class_message"] ="Class added successfully!"
                st.rerun()

    #button which opens add class box
    if st.button("Add Class"):
        add_class_dialog(classes,subjects)

    ##########DOWNLOAD CLASS TEMPLATE##########
    #empty template with subject csv headers
    class_template =pd.DataFrame(columns=["class_name","subject_name","year_group"])

    #turn template into csv
    class_template_csv =class_template.to_csv(index=False)

    #download template button
    st.download_button("Download Class Template",data=class_template_csv,file_name="class_template.csv", mime="text/csv")

    ##########UPLOAD CLASS CSV##########
    @st.dialog("Upload Class CSV")
    def upload_class_csv(classes,subjects):
        st.write("Upload a CSV file following the template. The file should contain the following columns: class_name, subject_name, year_group.")

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

                #go through uploaded classes to add to existing classes 
                for index,class_row in uploaded_classes.iterrows():
                    class_name =class_row["class_name"]
                    subject_name =class_row["subject_name"]
                    year_group =int(class_row["year_group"])

                    #check class does not already exist
                    class_exists =(class_name.lower()in classes["class_name"].str.lower().values)

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
                classes.to_csv("data/new/classes.csv",index=False)
                #save success message
                st.session_state["class_upload_message"] =(f"{len(new_classes)}  classes uploaded successfully!")

                st.rerun()


    #button-upload class box
    if st.button("Upload Class CSV"):
        upload_class_csv(classes,subjects)

    ##########DELETE CLASS##########
    #pop-up window to confirm delete subject
    @st.dialog("Delete Class")
    def confirm_delete_class(classes,selected_class_id,selected_class_name):
        st.warning(f"Are you sure you want to delete {selected_class_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #classes is now dataframe without selected class
                classes =classes[classes["class_id"] !=selected_class_id].copy()

                #save
                classes.to_csv("data/new/classes.csv",index=False)
                st.session_state["delete_class_message"] ="Class deleted successfully!"
                st.rerun()


        #NO button column 2
        with col2:
            if st.button("Cancel", use_container_width=True):
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

        #choose class directly from table
        class_table =st.dataframe(class_display,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row")

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

            #get current subject
            selected_subject =subjects[subjects["subject_id"] ==selected_subject_id]

            #FIX!! current subject no exist-error
            if len(selected_subject) ==0:
                st.warning("The subject linked to this class no longer exists. Please choose a new subject.")
                selected_subject_name =None

            else:
                #get current subject name
                selected_subject_name =selected_subject["subject_name"].iloc[0]

            st.write("### Manage Selected Class")
            #bold class
            st.write(f"Selected: **{selected_class_name}**")

            ##########EDIT CLASS##########
            #input box-   prefill with current name
            new_class_name =st.text_input("Class Name",value=selected_class_name)

            #get list of subject names
            subject_names =subjects["subject_name"].tolist()

            #if current subject still exists
            if selected_subject_name is not None:
                #find current subject position
                current_subject_index =subject_names.index(selected_subject_name)

            else:
                #default to first available subject
                current_subject_index =0

            #choose subject-prefill with current subject
            new_subject_name =st.selectbox("Subject",subject_names,index=current_subject_index)

            #choose year group-prefill with current year group
            new_year_group =st.number_input("Year Group",min_value=1,max_value=13,value=int(selected_year_group),step=1)

            #if update button clicked-remove whitespace,check empty
            if st.button("Update Class"):
                new_class_name =new_class_name.strip()

                #if empty-flag error
                if new_class_name =="":
                    st.error("Class name is required.")

                #if new name not same as current & already exists-flag error
                elif(new_class_name.lower()!=selected_class_name.lower() and new_class_name.lower()
                    in classes["class_name"].str.lower().values):
                    st.error("This class already exists.")
                else:
                    #get subject id from selected subject name
                    new_subject =subjects[subjects["subject_name"] ==new_subject_name]

                    new_subject_id =new_subject["subject_id"].iloc[0]

                    #change name-update in dataframe with id
                    classes.loc[classes["class_id"] ==selected_class_id,"class_name"] =new_class_name

                    #change subject-update in dataframe with id
                    classes.loc[classes["class_id"] ==selected_class_id,"subject_id"] =new_subject_id

                    #change year-update in dataframe with id
                    classes.loc[classes["class_id"] ==selected_class_id,"year_group"] =new_year_group

                    #save updated classes
                    classes.to_csv("data/new/classes.csv",index=False)
                    st.session_state["update_class_message"] ="Class updated successfully."
                    st.rerun()

            ##########DELETE CLASS BUTTON##########
            #delete button only show when class selected
            if st.button("Delete Class",type="primary"):
                confirm_delete_class(classes,selected_class_id,selected_class_name)