#imports
import streamlit as st

from style_loader import load_styles
from authenticate import update_teacher_name
from authenticate import change_password
from authenticate import set_tutorial_seen

#extra styling
load_styles("settings.css")

##########UPDATE NAME POPUP##############
@st.dialog("Update Name")
def update_name_popup():
    st.write("Edit the name shown on your Phronesis account.")
    new_name =st.text_input("Name",value=st.session_state["teacher_name"])

    #2 options-cancel,savename
    button_left,button_right =st.columns(2)

    with button_left:
        if st.button("Cancel",key="cancel_name",use_container_width=True):
            st.rerun()

    with button_right:
        if st.button("Save Name",type="primary",key="save_name",use_container_width=True):
            updated =update_teacher_name(st.session_state["teacher_id"],new_name)

            #make sure new name not empty
            if updated:
                st.session_state["teacher_name"] =" ".join(new_name.split())
                st.success("Name updated successfully.")
                st.rerun()
            else:
                st.error("Name cannot be empty.")


##############ACCESSIBILITY POPUP##########
@st.dialog("Accessibility Settings")
def accessibility_popup():
    st.write("Adjust how Phronesis is displayed to make information  easier to read.")

    ##########READABLE FONT##########
    dyslexia_font =st.toggle("Use dyslexia-friendly font",value=st.session_state.get("dyslexia_font",False))
    st.caption("A clear font that may make text easier to read.")

    #############TEXT SIZE##########
    font_options =["Small","Medium","Large","Extra Large"]
    current_font_size =st.session_state.get("font_size","Medium")
    font_size =st.selectbox("Text Size",font_options,index=font_options.index(current_font_size))

    ##########DISPLAY MODE##########
    #improvement- yet to implement
    display_options =["Light","Dark"]
    current_display_mode =st.session_state.get("display_mode","Light")
    display_mode =st.selectbox("Display Mode",display_options,index=display_options.index(current_display_mode))

    ##########BUTTONS##########
    button_left,button_right =st.columns(2)

    with button_left:
        if st.button("Cancel",key="cancel_accessibility",use_container_width=True):
            st.rerun()

    with button_right:
        if st.button("Apply Settings",type="primary",key="apply_accessibility",use_container_width=True):
            st.session_state["dyslexia_font"] =dyslexia_font
            st.session_state["font_size"] =font_size
            st.session_state["display_mode"] =display_mode
            st.rerun()


#############CHANGE PASSWORD POPUP##########
@st.dialog("Change Password")
def change_password_popup():
    st.write("Please input your current password before choosing a new one.")

    current_password =st.text_input("Current Password",type="password")
    new_password =st.text_input("New Password",type="password")
    confirm_password =st.text_input("Confirm New Password",type="password")

    #2 options-cancel,save password
    button_left,button_right =st.columns(2)

    with button_left:
        if st.button("Cancel",key="cancel_password",use_container_width=True):
            st.rerun()

    with button_right:
        if st.button("Save Password",type="primary",key="save_password",use_container_width=True):
            if new_password !=confirm_password:
                st.error("New passwords do not match.")
            else:
                success,message =change_password(st.session_state["teacher_id"],current_password,new_password)

                if success:
                    st.success(message)
                else:
                    st.error(message)


#############TUTORIAL POPUP##########
#fix!-allows tutorial to be restarted
@st.dialog("Show Tutorial Again")
def tutorial_popup():
    st.write("Would you like to restart the Phronesis introduction tutorial?")
    st.caption(
        "This will take you through the tutorial slides again. "
        "Your account and student data will not be changed."
    )

    #2 options-cancel,restart tutorial
    button_left,button_right =st.columns(2)

    with button_left:
        if st.button("Cancel",key="cancel_tutorial",use_container_width=True):
            st.rerun()

    with button_right:
        if st.button("Restart Tutorial",type="primary",key="restart_tutorial",use_container_width=True):
            set_tutorial_seen(st.session_state["teacher_id"],False)
            st.session_state["tutorial_seen"] =False
            st.session_state["tutorial_step"] =0
            st.rerun()


##########LOG OUT POPUP##########
@st.dialog("Log Out")
def log_out_popup():
    st.write("Are you sure you want to log out of Phronesis?")
    st.caption("Your saved student information will remain in your workspace.")

    #2 options-stay logged in,log out
    button_left,button_right =st.columns(2)

    with button_left:
        if st.button("Stay Logged In",key="cancel_logout",use_container_width=True):
            st.rerun()

    with button_right:
        if st.button("Log Out",type="primary",key="confirm_logout",use_container_width=True):
            #clear session state (key means every session variable)
            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()


##########SETTINGS PAGE##########
with st.container(key="settings_page"):
    st.title("Settings")
    st.write("Manage your Phronesis account and preferences.")

    ##########PROFILE##########
    with st.container(key="settings_profile"):
        st.caption("ACCOUNT")
        st.write("## Profile")
        st.write("Manage the basic details connected to your Phronesis account.")
        st.write(f"**Email:** {st.session_state['teacher_email']}")
        st.write(f"**Name:** {st.session_state['teacher_name']}")

        if st.button("Update Name",key="open_name"):
            update_name_popup()

    ##########ACCESSIBILITY##########
    with st.container(key="settings_accessibility"):
        st.caption("DISPLAY")
        st.write("## Accessibility")
        st.write("Adjust how Phronesis looks and make information easier to read.")

        current_font =st.session_state.get("font_size","Medium")
        current_mode =st.session_state.get("display_mode","Light")
        readable_font =st.session_state.get("dyslexia_font",False)

        #on/off label for readable font
        if readable_font:
            readable_text ="On"
        else:
            readable_text ="Off"

        #current accessibility settings
        st.caption(f"Text size: {current_font}  |  " f"Display: {current_mode}  |  " f"Readable font: {readable_text}")

        if st.button("Accessibility Settings",key="open_accessibility"):
            accessibility_popup()

    ##########SECURITY##########
    with st.container(key="settings_security"):
        st.caption("SECURITY")
        st.write("## Password")
        st.write("Change the password used to sign in to your account.")

        if st.button("Change Password",key="open_password"):
            change_password_popup()

    ##########HELP##########
    with st.container(key="settings_help"):
        st.caption("HELP")
        st.write("## Tutorial")
        st.write("Here's the tutorial whenever you need a reminder!")

        if st.button("Show Tutorial Again",key="open_tutorial"):
            tutorial_popup()

    ##########ACCOUNT##########
    with st.container(key="settings_account"):
        st.caption("SESSION")
        st.write("## Account")
        st.write("Finish your current Phronesis session.")

        if st.button("Log Out",key="open_logout"):
            log_out_popup()