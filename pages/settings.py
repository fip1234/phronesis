#imports
import streamlit as st

from style_loader import load_styles
from authenticate import update_teacher_name
from authenticate import change_password
from authenticate import set_tutorial_seen


##########STYLING##########

#settings has extra styling ontop of normal app styling
load_styles("settings.css")


##########UPDATE NAME POPUP##########

@st.dialog("Update Name")
def updateNamePopup():

    st.write("Change the name shown on your Phronesis account.")

    newName =st.text_input(
        "Name",
        value=st.session_state["teacher_name"]
    )

    buttonLeft,buttonRight =st.columns(2)

    with buttonLeft:

        if st.button(
            "Cancel",
            key="cancel_name",
            use_container_width=True
        ):
            st.rerun()

    with buttonRight:

        if st.button(
            "Save Name",
            type="primary",
            key="save_name",
            use_container_width=True
        ):

            updated =update_teacher_name(
                st.session_state["teacher_id"],
                newName
            )

            if updated:

                st.session_state["teacher_name"] =" ".join(
                    newName.split()
                )

                st.success(
                    "Name updated successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Name cannot be empty."
                )


##########ACCESSIBILITY POPUP##########

@st.dialog("Accessibility Settings")
def accessibilityPopup():

    st.write(
        "Adjust how Phronesis is displayed to make information easier to read."
    )


    ##########READABLE FONT##########

    dyslexiaFont =st.toggle(
        "Use a more readable font",
        value=st.session_state.get(
            "dyslexia_font",
            False
        )
    )

    st.caption(
        "Uses a clear, spaced font that may make text easier to read."
    )


    ##########TEXT SIZE##########

    fontOptions =[
        "Small",
        "Medium",
        "Large",
        "Extra Large"
    ]

    currentFontSize =st.session_state.get(
        "font_size",
        "Medium"
    )

    fontSize =st.selectbox(
        "Text Size",
        fontOptions,
        index=fontOptions.index(
            currentFontSize
        )
    )


    ##########DISPLAY MODE##########

    displayOptions =[
        "Light",
        "Dark"
    ]

    currentDisplayMode =st.session_state.get(
        "display_mode",
        "Light"
    )

    displayMode =st.selectbox(
        "Display Mode",
        displayOptions,
        index=displayOptions.index(
            currentDisplayMode
        )
    )


    ##########BUTTONS##########

    buttonLeft,buttonRight =st.columns(2)

    with buttonLeft:

        if st.button(
            "Cancel",
            key="cancel_accessibility",
            use_container_width=True
        ):
            st.rerun()

    with buttonRight:

        if st.button(
            "Apply Settings",
            type="primary",
            key="apply_accessibility",
            use_container_width=True
        ):

            st.session_state["dyslexia_font"] =dyslexiaFont
            st.session_state["font_size"] =fontSize
            st.session_state["display_mode"] =displayMode

            st.rerun()


##########CHANGE PASSWORD POPUP##########

@st.dialog("Change Password")
def changePasswordPopup():

    st.write(
        "Enter your current password before choosing a new one."
    )

    currentPassword =st.text_input(
        "Current Password",
        type="password"
    )

    newPassword =st.text_input(
        "New Password",
        type="password"
    )

    confirmPassword =st.text_input(
        "Confirm New Password",
        type="password"
    )


    buttonLeft,buttonRight =st.columns(2)

    with buttonLeft:

        if st.button(
            "Cancel",
            key="cancel_password",
            use_container_width=True
        ):
            st.rerun()

    with buttonRight:

        if st.button(
            "Save Password",
            type="primary",
            key="save_password",
            use_container_width=True
        ):

            if newPassword !=confirmPassword:

                st.error(
                    "New passwords do not match."
                )

            else:

                success,message =change_password(
                    st.session_state["teacher_id"],
                    currentPassword,
                    newPassword
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)


##########TUTORIAL POPUP##########

@st.dialog("Show Tutorial Again")
def tutorialPopup():

    st.write(
        "Would you like to restart the Phronesis introduction tutorial?"
    )

    st.caption(
        "This will take you through the tutorial slides again. "
        "Your account and student data will not be changed."
    )


    buttonLeft,buttonRight =st.columns(2)

    with buttonLeft:

        if st.button(
            "Cancel",
            key="cancel_tutorial",
            use_container_width=True
        ):
            st.rerun()

    with buttonRight:

        if st.button(
            "Restart Tutorial",
            type="primary",
            key="restart_tutorial",
            use_container_width=True
        ):

            set_tutorial_seen(
                st.session_state["teacher_id"],
                False
            )

            st.session_state["tutorial_seen"] =False
            st.session_state["tutorial_step"] =0

            st.rerun()


##########LOG OUT POPUP##########

@st.dialog("Log Out")
def logOutPopup():

    st.write(
        "Are you sure you want to log out of Phronesis?"
    )

    st.caption(
        "Your saved student information will remain in your workspace."
    )


    buttonLeft,buttonRight =st.columns(2)

    with buttonLeft:

        if st.button(
            "Stay Logged In",
            key="cancel_logout",
            use_container_width=True
        ):
            st.rerun()

    with buttonRight:

        if st.button(
            "Log Out",
            type="primary",
            key="confirm_logout",
            use_container_width=True
        ):

            #clear all session infomation when logging out
            for key in list(
                st.session_state.keys()
            ):
                del st.session_state[key]

            st.rerun()


##########SETTINGS PAGE##########

with st.container(key="settings_page"):

    st.title("Settings")

    st.write(
        "Manage your Phronesis account and preferences."
    )


    ##########PROFILE##########

    with st.container(key="settings_profile"):

        st.caption("ACCOUNT")

        st.write("## Profile")

        st.write(
            "Manage the basic details connected to your Phronesis account."
        )

        st.write(
            f"**Email:** {st.session_state['teacher_email']}"
        )

        st.write(
            f"**Name:** {st.session_state['teacher_name']}"
        )

        if st.button(
            "Update Name",
            key="open_name"
        ):
            updateNamePopup()


    ##########ACCESSIBILITY##########

    with st.container(key="settings_accessibility"):

        st.caption("DISPLAY")

        st.write("## Accessibility")

        st.write(
            "Adjust how Phronesis looks and make information easier to read."
        )

        currentFont =st.session_state.get(
            "font_size",
            "Medium"
        )

        currentMode =st.session_state.get(
            "display_mode",
            "Light"
        )

        readableFont =st.session_state.get(
            "dyslexia_font",
            False
        )

        if readableFont:
            readableText ="On"
        else:
            readableText ="Off"

        st.caption(
            f"Text size: {currentFont}  •  "
            f"Display: {currentMode}  •  "
            f"Readable font: {readableText}"
        )

        if st.button(
            "Accessibility Settings",
            key="open_accessibility"
        ):
            accessibilityPopup()


    ##########SECURITY##########

    with st.container(key="settings_security"):

        st.caption("SECURITY")

        st.write("## Password")

        st.write(
            "Change the password used to sign in to your account."
        )

        if st.button(
            "Change Password",
            key="open_password"
        ):
            changePasswordPopup()


    ##########HELP##########

    with st.container(key="settings_help"):

        st.caption("HELP")

        st.write("## Tutorial")

        st.write(
            "Go through the Phronesis introduction again whenever you need a reminder."
        )

        if st.button(
            "Show Tutorial Again",
            key="open_tutorial"
        ):
            tutorialPopup()


    ##########ACCOUNT##########

    with st.container(key="settings_account"):

        st.caption("SESSION")

        st.write("## Account")

        st.write(
            "Finish your current Phronesis session."
        )

        if st.button(
            "Log Out",
            key="open_logout"
        ):
            logOutPopup()