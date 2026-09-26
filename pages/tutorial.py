#tutorial.py- contains code for displaying the Phronesis introduction tutorial
 #imports
import os
import streamlit as st

from authenticate import set_tutorial_seen


def show_tutorial():
    #store tutorial slide currently being viewed
    if "tutorial_step" not in st.session_state:
        st.session_state["tutorial_step"] =0

    ########TUTORIAL CONTENT#############
    slide_list =[{
            "title":"Welcome to Phronesis",
            "subtitle":"A quick introduction before you get started!",
            "text":
                "Phronesis helps bring student information together so you can "
                "identify possible concerns, understand the evidence behind them "
                "and decide what support may be appropriate.",
            "image":"assets/tutInsights.png"
        },{
            "title":"Your Dashboard",
            "subtitle":"See what needs your attention first.",
            "text":
                "The Dashboard gives you a quick overview of all the classes and students "
                "requiring attention and important patterns across the data you "
                "have added.",
            "image":"assets/tutDashboard.png"
        },{
            "title":"Manage Your Data",
            "subtitle":"Build your teacher workspace.",
            "text":
                "Use Data Management to add subjects, classes and students. "
                "Assessment and attendance information can be entered manually "
                "or uploaded using the provided CSV templates."
                "Simply download the templates, fill them out in the correct columns and upload them back into Phronesis.",
            "image":"assets/tutUpload.png"
        },{
            "title":"Explore Classes and Students",
            "subtitle":"Explore individual students.",
            "text":
                "Choose a year group, subject and class to review class-level "
                "information. Select an individual student to view their risk "
                "status, learning indicators and supporting information.",
            "image":"assets/tutClass.png"
        },{
            "title":"Understand and Support",
            "subtitle":"Use the prediction as a starting point.",
            "text":
                "Student profiles provide supporting insights, recommended "
                "follow-up actions and editable parent communication. "
                "Please note:Phronesis supports teacher judgement rather than replaces it.",
            "image":"assets/tutStudent.png"
        }
    ]

    slide_count =len(slide_list)
    step_now =st.session_state["tutorial_step"]
    current_slide =slide_list[step_now]

    ################PAGE##########
    with st.container(key="tutorial_page"):
        top_left,top_right =st.columns([5,1])

        with top_left:
            st.caption("PHRONESIS TUTORIAL")

        #top section of the tutorial page with title and progress
        with top_right:
            st.caption(f"{step_now + 1} of {slide_count}")

        ##########POPUP CARD##########
        with st.container(key="tutorial_card"):
            st.title(current_slide["title"])
            st.subheader(current_slide["subtitle"])

            #placeholder for all images
            img_path =current_slide["image"]

            if os.path.exists(img_path):
                st.image(img_path,use_container_width=True)
            else:
                with st.container(key="tutorial_image_placeholder"):
                    #before final screenshots were made
                    st.write("Screenshot  will be added here")

            #current slide info
            st.write(current_slide["text"])
            progress_amount =(step_now +1) / slide_count
            st.progress(progress_amount)

            #navigation buttons
            back_col,space_col,next_col =st.columns([1.2,3,1.2])

            #go back to the previous slide button
            with back_col:
                if step_now >0:
                    if st.button("← Back",key="tutorial_back",use_container_width=True):
                        st.session_state["tutorial_step"] -=1
                        st.rerun()

            #NEXT/FINISH 
            with next_col:
                #show next until final slide
                if step_now <slide_count -1:
                    if st.button("Next →",type="primary",key="tutorial_next",use_container_width=True):
                        st.session_state["tutorial_step"] +=1
                        st.rerun()
                #final slide completes tutorial
                else:
                    if st.button("Get Started",type="primary",key="tutorial_finish",use_container_width=True):
                        set_tutorial_seen(st.session_state["teacher_id"],True)
                        st.session_state["tutorial_seen"] =True

                        #reset tutorial so show tut again starts at slide 1
                        st.session_state["tutorial_step"] =0

                        st.rerun()