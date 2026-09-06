import streamlit as st


def show_dashboard(df):

    st.header("Student Risk Dashboard")

    #count students in each prediction group
    at_risk_count = (
        df["risk_prediction"] == "At Risk"
    ).sum()

    not_at_risk_count = (
        df["risk_prediction"] == "Not At Risk"
    ).sum()

    insufficient_count = (
        df["prediction_status"] == "Insufficient data"
    ).sum()


    ##########Dashboard summary cards##########

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "At Risk",
            at_risk_count
        )

    with col2:
        st.metric(
            "Not At Risk",
            not_at_risk_count
        )

    with col3:
        st.metric(
            "Insufficient Data",
            insufficient_count
        )


    ##########Student table##########

    st.subheader("Student Overview")

    #copy data so original dataframe not changed
    display_df = df.copy()

    #make missing subject clearer
    display_df["subject"] = (
        display_df["subject"]
        .fillna("No assessment data")
    )

    #set order for risk results
    risk_order = {
        "At Risk": 1,
        "Not At Risk": 2,
        "Insufficient data": 3
    }

    #temporary column used for sorting
    display_df["sort_order"] = (
        display_df["risk_prediction"]
        .map(risk_order)
    )

    #sort higher priority students first
    display_df = display_df.sort_values(
        by="sort_order"
    )

    #only display useful teacher information
    display_df = display_df[
        [
            "student_id",
            "name",
            "subject",
            "attendance_percentage",
            "prediction_status",
            "risk_prediction"
        ]
    ]

    #replace remaining missing display values
    display_df = display_df.fillna(
        "Data Missing"
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )