#Add info like students, classes, subjects
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

    #rename
    if "rename_class_message" in st.session_state:
        st.success(st.session_state["rename_class_message"])
        del st.session_state["rename_class_message"]


    ##########ADD CLASS##########

    @st.dialog("Add Class")
    def add_class_dialog(classes,subjects):

        st.write("Enter the new class below.")

        class_name =st.text_input("Class Name")

        #if no subjects exist- teacher must create subject first
        if len(subjects) ==0:
            st.warning("Please add a subject before creating a class.")
            return

        #choose subject
        subject_name =st.selectbox(
            "Subject",
            subjects["subject_name"]
        )

        #choose year group
        year_group =st.number_input(
            "Year Group",
            min_value=1,
            max_value=13,
            step=1
        )


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

                #get subject id from selected subject name
                selected_subject =subjects[
                    subjects["subject_name"] ==subject_name
                ]

                subject_id =selected_subject[
                    "subject_id"
                ].iloc[0]


                #find highest existing class id number
                highest_class_number =0

                #loop through classes to find highest number
                #replace C with empty string,convert to int,compare to highest number
                for class_id in classes["class_id"]:
                    class_number =int(class_id.replace("C",""))

                    #compare to highest number-if higher,set as new highest number
                    if class_number >highest_class_number:
                        highest_class_number =class_number

                #new class id +1
                new_class_number =highest_class_number +1

                #new id-three digits, leading zeros, prefix CLS
                class_id =("CLS"+str(new_class_number).zfill(3))

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


    ##########DELETE CLASS##########

    @st.dialog("Delete Class")
    def confirm_delete_class(classes,selected_class_id,selected_class_name):

        st.warning(f"Are you sure you want to delete {selected_class_name}?")

        #make two columns for yes/no buttons
        col1,col2 =st.columns(2)

        #YES button column
        with col1:

            if st.button(
                "Yes, Delete",
                type="primary",
                use_container_width=True
            ):

                #classes is now dataframe without selected class
                classes =classes[
                    classes["class_id"] !=selected_class_id
                ].copy()

                #save
                classes.to_csv("data/new/classes.csv",index=False)

                st.session_state["delete_class_message"] ="Class deleted successfully!"

                st.rerun()


        #NO
        with col2:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.rerun()


    ##########VIEW CLASSES##########

    #bold
    st.write("### Current Classes")

    #if no classes added
    if len(classes) ==0:
        st.info("No classes have been added yet.")

    else:

        #attach subject name to class table
        class_display =classes.merge(
            subjects[
                ["subject_id","subject_name"]
            ],
            on="subject_id",
            how="left"
        )

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
        class_table =st.dataframe(
            class_display,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )


        ##########SELECTED CLASS##########

        #get selected rows
        selected_rows =class_table.selection.rows

        #if class selected- show options to edit and delete
        if len(selected_rows) >0:

            #get selected row
            selected_row =selected_rows[0]

            #get selected class
            selected_class =classes.iloc[selected_row]

            selected_class_id =selected_class["class_id"]

            selected_class_name =selected_class["class_name"]


            st.write("### Manage Selected Class")

            #bold class
            st.write(
                f"Selected: **{selected_class_name}**"
            )


            ##########RENAME CLASS##########

            #input box- prefill with current name
            new_class_name =st.text_input(
                "Rename Class",
                value=selected_class_name
            )

            #if rename button clicked- remove whitespace,check empty
            if st.button("Rename Class"):

                new_class_name =new_class_name.strip()

                #if empty-flag error
                if new_class_name =="":
                    st.error("Class name is required.")

                #if new name is not same as current & already exists- flag error
                elif(
                    new_class_name.lower()
                    !=selected_class_name.lower()
                    and
                    new_class_name.lower()
                    in classes["class_name"].str.lower().values
                ):

                    st.error("This class already exists.")

                else:

                    #change name- update in dataframe with id
                    classes.loc[
                        classes["class_id"] ==selected_class_id,
                        "class_name"
                    ] =new_class_name

                    #save updated classes
                    classes.to_csv(
                        "data/new/classes.csv",
                        index=False
                    )

                    #save success message
                    st.session_state["rename_class_message"] ="Class renamed successfully."

                    st.rerun()


            ##########DELETE CLASS BUTTON##########

            #delete button only show when class selected
            if st.button(
                "Delete Class",
                type="primary"
            ):

                confirm_delete_class(
                    classes,
                    selected_class_id,
                    selected_class_name
                )