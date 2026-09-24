#imports
import os
import streamlit as st

from authenticate import set_tutorial_seen


def show_tutorial():


    ##########TUTORIAL STATE##########

    #store which tutorial slide user is currently viewing
    if "tutorial_step" not in st.session_state:
        st.session_state["tutorial_step"] =0


    ##########TUTORIAL CONTENT##########

    slides =[
        {
            "title":"Welcome to Phronesis",
            "subtitle":"A quick introduction before you get started.",
            "text":
                "Phronesis helps bring student information together so you can "
                "identify possible concerns, understand the evidence behind them "
                "and decide what support may be appropriate.",
            "image":"assets/tutorial_welcome.png"
        },

        {
            "title":"Your Dashboard",
            "subtitle":"See what needs your attention first.",
            "text":
                "The Dashboard gives you an overview of your classes, students "
                "requiring attention and important patterns across the data you "
                "have added.",
            "image":"assets/tutorial_dashboard.png"
        },

        {
            "title":"Manage Your Data",
            "subtitle":"Build your teacher workspace.",
            "text":
                "Use Data Management to add subjects, classes and students. "
                "Assessment and attendance information can be entered manually "
                "or uploaded using the provided CSV templates.",
            "image":"assets/tutorial_data.png"
        },

        {
            "title":"Explore Classes and Students",
            "subtitle":"Move from class-level insight to individual students.",
            "text":
                "Choose a year group, subject and class to review class-level "
                "information. Select an individual student to view their risk "
                "status, learning indicators and supporting information.",
            "image":"assets/tutorial_classes.png"
        },

        {
            "title":"Understand and Support",
            "subtitle":"Use the prediction as a starting point.",
            "text":
                "Student profiles provide supporting insights, recommended "
                "follow-up actions and editable parent communication. "
                "Phronesis supports teacher judgement rather than replacing it.",
            "image":"assets/tutorial_support.png"
        }
    ]


    total_slides =len(slides)

    current_step =st.session_state["tutorial_step"]

    slide =slides[current_step]


    ##########PAGE##########

    with st.container(key="tutorial_page"):


        ##########TOP##########

        top_left,top_right =st.columns(
            [5,1]
        )

        with top_left:

            st.caption(
                "PHRONESIS TUTORIAL"
            )

        with top_right:

            st.caption(
                f"{current_step + 1} of {total_slides}"
            )


        ##########POPUP CARD##########

        with st.container(key="tutorial_card"):


            ##########TITLE##########

            st.title(
                slide["title"]
            )

            st.subheader(
                slide["subtitle"]
            )


            ##########IMAGE PLACEHOLDER##########

            image_path =slide["image"]

            if os.path.exists(image_path):

                st.image(
                    image_path,
                    use_container_width=True
                )

            else:

                with st.container(key="tutorial_image_placeholder"):

                    st.write(
                        "Screenshot will be added here"
                    )


            ##########TEXT##########

            st.write(
                slide["text"]
            )


            ##########PROGRESS##########

            progress_value =(current_step + 1) /total_slides

            st.progress(
                progress_value
            )


            ##########NAVIGATION##########

            back_col,space_col,next_col =st.columns(
                [1.2,3,1.2]
            )


            ##########BACK##########

            with back_col:

                if current_step >0:

                    if st.button(
                        "← Back",
                        key="tutorial_back",
                        use_container_width=True
                    ):
                        st.session_state["tutorial_step"] -=1
                        st.rerun()


            ##########NEXT / FINISH##########

            with next_col:

                #show Next until final slide
                if current_step <total_slides -1:

                    if st.button(
                        "Next →",
                        type="primary",
                        key="tutorial_next",
                        use_container_width=True
                    ):
                        st.session_state["tutorial_step"] +=1
                        st.rerun()


                #final slide completes tutorial
                else:

                    if st.button(
                        "Get Started",
                        type="primary",
                        key="tutorial_finish",
                        use_container_width=True
                    ):

                        set_tutorial_seen(
                            st.session_state["teacher_id"],
                            True
                        )

                        st.session_state["tutorial_seen"] =True

                        #reset tutorial so Show Tutorial Again starts at slide 1
                        st.session_state["tutorial_step"] =0

                        st.rerun()