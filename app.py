import streamlit as st

from agent import run_agent


# ---------------------------------------------------------
# Page
# ---------------------------------------------------------

st.set_page_config(
    page_title="Welding Procedure Advisor",
    page_icon="🔧",
    layout="wide"
)


st.title("🔧 Welding Procedure Advisor")

st.write(
    "AI-assisted preliminary welding procedure guidance "
    "for mechanical engineering applications."
)


# ---------------------------------------------------------
# Input Form
# ---------------------------------------------------------

with st.form("welding_form"):

    material = st.selectbox(
        "Base Material",
        [
            "Mild Steel",
            "Stainless Steel 304",
            "Stainless Steel 316",
            "Aluminum 6061"
        ]
    )

    thickness = st.number_input(
        "Material Thickness (mm)",
        min_value=0.5,
        max_value=100.0,
        value=6.0
    )

    joint = st.selectbox(
        "Joint Type",
        [
            "Butt",
            "Fillet",
            "Lap",
            "T-Joint",
            "Corner"
        ]
    )

    position = st.selectbox(
        "Welding Position",
        [
            "1G",
            "2G",
            "3G",
            "4G",
            "1F",
            "2F",
            "3F",
            "4F"
        ]
    )

    process = st.selectbox(
        "Available Welding Process",
        [
            "GMAW",
            "GTAW",
            "SMAW",
            "FCAW",
            "Any"
        ]
    )

    application = st.text_input(
        "Application",
        placeholder="Example: Automotive bracket"
    )

    production = st.selectbox(
        "Production Requirement",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    submitted = st.form_submit_button(
        "Analyze Welding Procedure"
    )


# ---------------------------------------------------------
# Run Agent
# ---------------------------------------------------------

if submitted:

    if not application:
        st.warning("Please enter the application.")
        st.stop()

    user_request = f"""
    Base Material: {material}
    Thickness: {thickness} mm
    Joint Type: {joint}
    Welding Position: {position}
    Available Process: {process}
    Application: {application}
    Production Requirement: {production}
    """

    with st.spinner("Analyzing welding requirements..."):

        try:
            result = run_agent(user_request)

            st.subheader("Welding Procedure Advisory")

            st.markdown(result)

        except Exception as e:

            st.error(
                "Something went wrong while running the agent."
            )

            st.code(str(e))


# ---------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------

st.divider()

st.caption(
    "This application provides preliminary engineering guidance "
    "only. It does not generate a certified or approved WPS. "
    "Verify final procedures against applicable codes, qualified "
    "WPS/PQR/WPQ, manufacturer requirements and qualified "
    "welding personnel."
)
