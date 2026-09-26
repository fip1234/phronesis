#about.py-About page for the Phronesis application
#Contains general information about the Phronesis application
#user will be introduced to the Phronesis application

#imports
import os
import base64
import mimetypes
import streamlit as st

#convert local image to image CSS image to image CSS can use (css 64 encoded)
def get_image_data(path):
    if not os.path.exists(path):
        return None

    #mime- file type
    mime_type,_ =mimetypes.guess_type(path)

    with open(path,"rb") as image_file:
        encoded =base64.b64encode(image_file.read()).decode()

    #return the base64 encoded image data 
    return f"data:{mime_type};base64,{encoded}"

def show_about_page():
    ##########HERO BACKGROUND##########
    #path to main background image
    hero_image ="assets/phronesis_background.png"
    hero_data =get_image_data(hero_image)

    #apply hero image directly as container background
    if hero_data:
        #white overlay, linear gradient, 
        st.markdown(f"""
            <style>
            .st-key-hero_section {{
                background:
                    linear-gradient(
                        rgba(255,255,255,0.42),
                        rgba(255,255,255,0.42)
                    ),
                    url("{hero_data}") !important;
                background-size:cover !important;
                background-position:center !important;
                background-repeat:no-repeat !important;
            }}
            </style>
            """,
            #allow HTML for custom CSS styling
            unsafe_allow_html=True
        )

    ##########SECTION 1 - HERO##########
    #contains main phronesis title and get started buttton
    with st.container(key="hero_section"):
        #top right signup button
        empty_col,signup_col =st.columns([8,1.3])

        with signup_col:
            if st.button("Sign Up",key="top_signup",use_container_width=True):
                st.session_state["public_view"] ="login"
                st.rerun()

        #main hero title
        st.title("PHRONESIS")
        st.subheader("Your personal teacher support system.")

        #centred get started button
        #2.4=left column width... 1.2=button column width... 2.4=right column width
        left,button_col,right =st.columns([2.4,1.2,2.4])

        with button_col:
            if st.button("Get Started",type="primary",key="hero_get_started",use_container_width=True):
                st.session_state["public_view"] ="login"
                st.rerun()

    ##########SECTION 2 - YELLOWWWW######
    with st.container(key="yellow_section"):
        #0.9=left column width... 1.1=right column width
        image_col,text_col =st.columns([0.9,1.1],gap="large")

        ##########CLASSROOM IMAGE##########
        with image_col:
            classroom_image ="assets/classroom.jpg"

            if os.path.exists(classroom_image):
                st.image(classroom_image,use_container_width=True)
            else:
                st.info("Add classroom image at assets/classroom.jpg")

        ##########YELLOW TEXT##########
        with text_col:
            st.caption("WHAT PHRONESIS DOES")
            st.header("Phronesis brings assessment, attendance and behaviour data together to highlight students who may need extra support, "
            "and explains the evidence behind every prediction.")

            st.write("""It helps teachers spot possible concerns earlier,review the supporting information, and make informed
                decisions without replacing professional judgement.""")

    ##########SECTION 3 - WHY PHRONESIS#######
    with st.container(key="why_section"):
        st.caption("WHY PHRONESIS")
        st.header("A clearer way to understand student risk.")
        st.write("")

        card1,card2,card3 =st.columns(3,gap="medium")
        ##########CARD 1##########
        with card1:
            with st.container(key="why_card_1"):
                st.caption("01")
                st.subheader("Brings data together")
                st.write("""View student information in one place instead of
                    switching between separate records and spreadsheets.""")

        ##########CARD 2##########
        with card2:
            with st.container(key="why_card_2"):
                st.caption("02")
                st.subheader("Highlights concern early")
                st.write("""Use machine learning and teacher-facing analytics
                    to identify students who may benefit from earlier
                    support.""")

        ##########CARD 3##########
        with card3:
            with st.container(key="why_card_3"):
                st.caption("03")
                st.subheader("Explains the evidence")
                st.write("""Predictions are supported by attendance and assessment
                    information so teachers can understand why a student has been flagged.""")

    ##########SECTION 4 - REVIEWS##########
    with st.container(key="reviews_section"):
        st.caption("REVIEWS")
        st.header("What teachers think.")
        st.write("")

        review1,review2,review3 =st.columns(3,gap="medium")

        ##########REVIEW 1##########
        with review1:
            with st.container(key="review_1"):
                st.markdown("#### \u201c")
                st.write("I found it easy to use, and I like that I can change the readability settings to suit me.")
                st.caption("Teacher participant")

        ##########REVIEW 2##########
        with review2:
            with st.container(key="review_2"):
                st.markdown("#### \u201c")
                st.write("I found the insights to be practical. I didnt have to think of them myself")
                st.caption("Teacher participant")

        ##########REVIEW 3##########
        with review3:
            with st.container(key="review_3"):
                st.markdown("#### \u201c")
                st.write("I really liked how it did the analysing for me.")
                st.caption("Teacher participant")

    ##########SECTION 5 - CTA##########
    with st.container(key="cta_section"):
        st.caption("GET STARTED")
        st.header("Ready to try Phronesis?")
        st.write("""Create your account and start building yourown teacher workspace.""")

        #2.3=left column width, 1.4=button column width, 2.3=right column width
        left,button_col,right =st.columns([2.3,1.4,2.3])

        with button_col:
            if st.button("Create Account",type="primary",key="bottom_signup",use_container_width=True):
                st.session_state["public_view"] ="login"
                st.rerun()

    ##########FOOTER##########
    with st.container(key="footer_section"):
        st.subheader("PHRONESIS")
        st.write("AI-assisted student risk analytics for teachers.")

        st.markdown(
            "[Contact](mailto:hello@phronesis.app) · "
            "[Support Form](#) · "
            "[Privacy](#)"
        )

        st.caption("Phronesis supports teacher judgement and does not make automatic decisions about students.")