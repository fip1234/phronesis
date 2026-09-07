#Add info like students, classes, subjects
#imports
import streamlit as st
import pandas as pd

def show_subjects():
    st.subheader("Subjects")
    st.write("Add, view and manage subjects.")

    #read subject data
    subjects =pd.read_csv("data/new/subjects.csv")

    ##########SUCCESS MESSAGES##########
    #add subject
    if "subject_message" in st.session_state:
        st.success(st.session_state["subject_message"])
        del st.session_state["subject_message"]

    #delete
    if "delete_message" in st.session_state:
        st.success(st.session_state["delete_message"])
        del st.session_state["delete_message"]

    #rename
    if "rename_message" in st.session_state:
        st.success(st.session_state["rename_message"])
        del st.session_state["rename_message"]

    #upload
    if "upload_message" in st.session_state:
        st.success(st.session_state["upload_message"])
        del st.session_state["upload_message"]

    ##########ADD SUBJECT##########
    #pop-up window to add subject
    @st.dialog("Add Subject")
    def add_subject_dialog(subjects):
        st.write("Enter the new subject below.")
        subject_name =st.text_input("Subject Name")

        #if add button clicked
        if st.button("Add Subject",type="primary"):
            #remove whitespace
            subject_name =subject_name.strip()

            #empty?-check and flag error
            if subject_name =="":
                st.error("Subject name is required.")

            #subject already exist? check and flag error
            elif subject_name.lower() in subjects["subject_name"].str.lower().values:
                st.error("This subject already exists.")

            else:
                #find highest existing subject id number
                highest_subject_number =0

                #loop through subjects to find highest number
                #replace SUB with empty string,convert to int,compare to highest number
                for subject_id in subjects["subject_id"]:
                    subject_number =int(subject_id.replace("SUB",""))

                    #compare to highest number-if higher,set as new highest number
                    if subject_number >highest_subject_number:
                        highest_subject_number =subject_number

                #new subject id +1
                new_subject_number =highest_subject_number +1

                #new id-three digits, leading zeros, prefix SUB
                subject_id =("SUB"+str(new_subject_number).zfill(3))

                #add new subject to dataframe
                new_subject =pd.DataFrame(
                    {
                        "subject_id":[subject_id],
                        "subject_name":[subject_name]
                    }
                )

                #add subject
                subjects =pd.concat([subjects,new_subject],ignore_index=True)

                #save subjects
                subjects.to_csv("data/new/subjects.csv",index=False)

                #save success message
                st.session_state["subject_message"] ="Subject added successfully!"
                st.rerun()

    #button which opens add subject box
    if st.button("Add Subject"):
        add_subject_dialog(subjects)

    ##########DOWNLOAD SUBJECT TEMPLATE##########
    #empty template with subject csv headers
    subject_template =pd.DataFrame(columns=["subject_name"])

    #turn template into csv
    subject_template_csv =subject_template.to_csv(index=False)

    #download template button
    st.download_button("Download Subject Template",data=subject_template_csv,file_name="subject_template.csv", mime="text/csv")
    
    ##########UPLOAD SUBJECT CSV##########
    #pop-up window to upload subject csv
    @st.dialog("Upload Subject CSV")
    def upload_subject_csv(subjects):
        st.write("Upload a CSV file following the template. The file should contain the following column: subject_name.")

        #must be csv
        uploaded_file =st.file_uploader("Choose Subject CSV",type=["csv"])

        #if file uploaded- read and show preview
        if uploaded_file is not None:
            #read uploaded csv
            uploaded_subjects =pd.read_csv(uploaded_file)

            #show uploaded data
            st.write("### Preview")
            st.dataframe(uploaded_subjects,use_container_width=True,hide_index=True)

            if st.button("Upload Subjects",type="primary"):
                ##########VALIDATE CSV##########
                #columns needed for upload
                required_columns =["subject_name"]

                #missing columns list- if any needed columns missing-flag error
                missing_columns =[]
                for column in required_columns:
                    if column not in uploaded_subjects.columns:
                        missing_columns.append(column)

                #missing columns?-flag error
                if missing_columns:
                    st.error(f"Missing required columns: {missing_columns}")
                    return

                #remove missing subject rows
                uploaded_subjects =uploaded_subjects.dropna(subset=["subject_name"]).copy()

                #remove whitespace subject names - string
                uploaded_subjects["subject_name"] =(uploaded_subjects["subject_name"].astype(str).str.strip())

                #remove empty subject names
                uploaded_subjects =uploaded_subjects[uploaded_subjects["subject_name"] !=""].copy()

                #if no more valid subjects- flag error
                if len(uploaded_subjects) ==0:
                    st.error("No valid subjects were found in the uploaded file.")
                    return

                ##########ADD SUBJECTS##########
                #find highest existing subject id number
                highest_subject_number =0

                #loop through existing subjects- get number from subject_id (remove sub)
                for subject_id in subjects["subject_id"]:
                    subject_number =int( subject_id.replace("SUB",""))

                    #compare to highest number
                    if subject_number >highest_subject_number:
                        highest_subject_number =subject_number

                #store new subjects
                new_subjects =[]

                #go through uploaded subjects
                for subject_name in uploaded_subjects["subject_name"]:

                    #check subject does not already exist
                    subject_exists =(subject_name.lower()in subjects["subject_name"].str.lower().values)

                    #check subject was not already added from same upload
                    uploaded_duplicate =False

                    for new_subject in new_subjects:
                        if(new_subject["subject_name"].lower() ==subject_name.lower()):
                            uploaded_duplicate =True

                    #only add new subject
                    if not subject_exists and not uploaded_duplicate:
                        #next subject id is highest number +1,stored with prefix sub
                        highest_subject_number =(highest_subject_number +1)
                        subject_id =("SUB"+str(highest_subject_number).zfill(3))

                        #store new subject
                        new_subjects.append(
                            {
                                "subject_id":subject_id,
                                "subject_name":subject_name
                            }
                        )

                #if every subject already existed
                if len(new_subjects) ==0:
                    st.warning("No new subjects were added. All subjects already exist.")
                    return

                #turn new subjects into dataframe
                new_subjects =pd.DataFrame(new_subjects)

                #add uploaded subjects
                subjects =pd.concat([subjects,new_subjects],ignore_index=True)

                #####save
                subjects.to_csv("data/new/subjects.csv",index=False)
                #save success message
                st.session_state["subject_upload_message"] =(f"{len(new_subjects)} subjects uploaded successfully!")
                st.rerun()

    #button-upload subject box
    if st.button("Upload Subject CSV"):
        upload_subject_csv(subjects)

    ##########DELETE SUBJECT##########
    #read class data-to check if subject is being used already
    classes =pd.read_csv("data/new/classes.csv")

    #pop-up window to confirm delete subject
    @st.dialog("Delete Subject")
    def confirm_delete_subject(subjects,selected_subject_id,selected_subject_name):
        st.warning(f"Are you sure you want to delete {selected_subject_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column 1
        with col1:
            if st.button("Yes, Delete",type="primary",use_container_width=True):
                #check if subject is being used by a class
                subject_in_use =(classes["subject_id"] ==selected_subject_id).any()

                #if subject is used by a class-dont delete
                if subject_in_use:
                    st.error("This subject cannot be deleted because it is being used by a class.")
                    return

                #subjects is now dataframe without selected subject
                subjects =subjects[subjects["subject_id"] !=selected_subject_id].copy()

                #save
                subjects.to_csv("data/new/subjects.csv",index=False)
                st.session_state["delete_message"] ="Subject deleted successfully!"
                st.rerun()

        #NO button column 2
        with col2:
            if st.button("Cancel",use_container_width=True):
                st.rerun()

    ##########VIEW SUBJECTS##########
    #bold
    st.write("### Current Subjects")

    #if no subjects added
    if len(subjects) ==0:
        st.info("No subjects have been added yet.")

    else:
        #choose subject directly from table
        subject_table =st.dataframe(subjects,use_container_width=True,hide_index=True,on_select="rerun",selection_mode="single-row")

        ##########SELECTED SUBJECT##########
        #get selected rows
        selected_rows =subject_table.selection.rows

        #if subject selected- show options to rename and delete
        if len(selected_rows) >0:
            #get selected row
            selected_row =selected_rows[0]

            #get selected subject
            selected_subject =subjects.iloc[selected_row]
            selected_subject_id =selected_subject["subject_id"]
            selected_subject_name =selected_subject["subject_name"]

            st.write("### Manage Selected Subject")
            #bold subject
            st.write(f"Selected: **{selected_subject_name}**")

            ##########RENAME SUBJECT##########
            #input box-   prefill with current name
            new_subject_name =st.text_input("Rename Subject",value=selected_subject_name)

            #if rename button clicked- remove whitespace,check empty
            if st.button("Rename Subject"):
                new_subject_name =new_subject_name.strip()

                #if empty-flag error
                if new_subject_name =="":
                    st.error("Subject name is required.")

                #if new name is not same as current & already exists- flag error
                elif(new_subject_name.lower()!=selected_subject_name.lower() and new_subject_name.lower()
                    in subjects["subject_name"].str.lower().values):
                    st.error("This subject already exists.")

                else:
                    #change name- update in dataframe with id
                    subjects.loc[subjects["subject_id"]==selected_subject_id,"subject_name"] =new_subject_name

                    #save updated subjects
                    subjects.to_csv("data/new/subjects.csv",index=False)
                    st.session_state["rename_message"] ="Subject renamed successfully."
                    st.rerun()

            ##########DELETE SUBJECT BUTTON##########
            #delete button only show when subject selected
            if st.button("Delete Subject",type="primary"):
                confirm_delete_subject(subjects,selected_subject_id,selected_subject_name)
