#imports
import streamlit as st

from authenticate import update_teacher_name
from authenticate import change_password
from authenticate import set_tutorial_seen


st.title("Settings")
st.write("Manage your Phronesis account and preferences.")


##########PROFILE##########

st.write("## Profile")

st.write(
    f"**Email:** {st.session_state['teacher_email']}"
)

new_name =st.text_input(
    "Name",
    value=st.session_state["teacher_name"]
)

if st.button("Update Name"):

    updated =update_teacher_name(
        st.session_state["teacher_id"],
        new_name
    )

    if updated:
        st.session_state["teacher_name"] =" ".join(new_name.split())
        st.success("Name updated successfully.")

    else:
        st.error("Name cannot be empty.")


st.markdown("---")

##########ACCESSIBILITY##########

st.write("## Accessibility")

st.write(
    "Adjust how Phronesis is displayed to make information easier to read."
)


##########READABLE FONT##########

if "dyslexia_font" not in st.session_state:
    st.session_state["dyslexia_font"] =False

dyslexia_font =st.toggle(
    "Use a more readable font",
    value=st.session_state["dyslexia_font"]
)

st.caption(
    "Uses a clear, spaced font that may make text easier to read."
)


##########FONT SIZE##########

font_options =[
    "Small",
    "Medium",
    "Large",
    "Extra Large"
]

current_font_size =st.session_state.get(
    "font_size",
    "Medium"
)

font_size =st.selectbox(
    "Text Size",
    font_options,
    index=font_options.index(current_font_size)
)


##########DISPLAY MODE##########

display_options =[
    "Light",
    "Dark"
]

current_display_mode =st.session_state.get(
    "display_mode",
    "Light"
)

display_mode =st.selectbox(
    "Display Mode",
    display_options,
    index=display_options.index(current_display_mode)
)


##########APPLY SETTINGS##########

if st.button("Apply Accessibility Settings"):

    st.session_state["dyslexia_font"] =dyslexia_font
    st.session_state["font_size"] =font_size
    st.session_state["display_mode"] =display_mode

    st.success(
        "Accessibility settings updated."
    )

    st.rerun()


st.markdown("---")


##########CHANGE PASSWORD##########

st.write("## Change Password")

current_password =st.text_input(
    "Current Password",
    type="password"
)

new_password =st.text_input(
    "New Password",
    type="password"
)

confirm_password =st.text_input(
    "Confirm New Password",
    type="password"
)

if st.button("Change Password"):

    if new_password !=confirm_password:
        st.error("New passwords do not match.")

    else:

        success,message =change_password(
            st.session_state["teacher_id"],
            current_password,
            new_password
        )

        if success:
            st.success(message)

        else:
            st.error(message)


st.markdown("---")


##########TUTORIAL##########

st.write("## Help")

st.write(
    "You can show the Phronesis introduction tutorial again at any time."
)

if st.button("Show Tutorial Again"):

    set_tutorial_seen(
        st.session_state["teacher_id"],
        False
    )

    st.session_state["tutorial_seen"] =False

    st.rerun()


st.markdown("---")


##########LOG OUT##########

st.write("## Account")

if st.button(
    "Log Out",
    type="primary"
):

    #clear session
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()