import streamlit as st

from agent import run_agent

from memory import (
    initialize_memory,
    save_case,
    get_memory,
    clear_memory
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="Welding Procedure Advisor",

    page_icon="🔧",

    layout="wide"
)


# ============================================================
# MEMORY
# ============================================================

initialize_memory()


# ============================================================
# HEADER
# ============================================================

st.title("🔧 Welding Procedure Advisor")

st.write(
    "AI-assisted welding procedure analysis "
    "for mechanical engineering applications."
)

st.info(
    "This application provides preliminary engineering "
    "guidance. It does not replace a qualified WPS/PQR, "
    "applicable welding code, manufacturer data, or "
    "engineering approval."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Previous Cases")

    cases = get_memory()

    if cases:

        st.write(
            f"Cases in this session: {len(cases)}"
        )

        for index, case in enumerate(
            cases,
            start=1
        ):

            st.write(
                f"{index}. "
                f"{case.get('component', 'Unknown')}"
            )

    else:

        st.write(
            "No previous cases."
        )


    if st.button(
        "Clear Session Memory"
    ):

        clear_memory()

        st.rerun()


# ============================================================
# JOB INFORMATION
# ============================================================

st.header("1. Job Information")

component = st.text_input(

    "Component",

    placeholder="Example: Worm Screw"
)


application = st.text_area(

    "Describe the job",

    placeholder=(
        "Example: Worn worm screw requires weld build-up "
        "to restore the working diameter."
    )
)


# ============================================================
# MATERIALS
# ============================================================

st.header("2. Materials")

col1, col2 = st.columns(2)


with col1:

    material_a = st.selectbox(

        "Material A",

        [
            "Mild Steel",
            "AISI 1045",
            "Stainless Steel 304",
            "Stainless Steel 316",
            "Stainless Steel 316L",
            "Cast Iron",
            "Ductile Iron",
            "Aluminum 6061"
        ]
    )


    thickness_a = st.number_input(

        "Material A Thickness (mm)",

        min_value=0.1,

        max_value=1000.0,

        value=10.0,

        step=0.5
    )


with col2:

    material_b = st.selectbox(

        "Material B",

        [
            "Same as Material A",
            "Mild Steel",
            "AISI 1045",
            "Stainless Steel 304",
            "Stainless Steel 316",
            "Stainless Steel 316L",
            "Cast Iron",
            "Ductile Iron",
            "Aluminum 6061"
        ]
    )


    thickness_b = st.number_input(

        "Material B Thickness (mm)",

        min_value=0.1,

        max_value=1000.0,

        value=10.0,

        step=0.5
    )


if material_b == "Same as Material A":

    material_b = material_a


# ============================================================
# COMPONENT CONDITION
# ============================================================

st.header("3. Component Condition")

cast_condition = st.radio(

    "Is this component cast?",

    [
        "No",
        "Yes",
        "Unknown"
    ],

    horizontal=True
)


condition = st.text_area(

    "Defect / Wear / Existing Condition",

    placeholder=(
        "Example: Worn diameter by approximately 2 mm, "
        "surface requires restoration."
    )
)


# ============================================================
# WELDING PURPOSE
# ============================================================

st.header("4. Welding Purpose")

purpose = st.selectbox(

    "Why is welding required?",

    [
        "Joining two components",
        "Repair a defect",
        "Build-up worn area",
        "Restore original dimension",
        "Increase service life"
    ]
)


# ============================================================
# WELDING PROCESS
# ============================================================

st.header("5. Available Welding Process")

processes = st.multiselect(

    "What welding processes are available?",

    [
        "SMAW",
        "GMAW",
        "GTAW",
        "FCAW"
    ],

    default=["SMAW"]
)


# ============================================================
# CONSUMABLE
# ============================================================

st.header("6. Consumable")

consumable = st.selectbox(

    "Known electrode / filler",

    [
        "Not known",
        "E7018",
        "E316L-16",
        "E316L-17",
        "ER316L"
    ]
)


if consumable == "Not known":

    consumable = ""


# ============================================================
# POSITION
# ============================================================

position = st.selectbox(

    "Welding Position",

    [
        "Flat",
        "Horizontal",
        "Vertical",
        "Overhead",
        "Multiple",
        "Unknown"
    ]
)


# ============================================================
# SERVICE
# ============================================================

service = st.text_area(

    "Service Environment",

    placeholder=(
        "Example: Abrasion, corrosion, temperature, "
        "rotating equipment, impact loading."
    )
)


# ============================================================
# ANALYZE
# ============================================================

st.divider()

analyze = st.button(

    "🔍 Analyze Welding Procedure",

    type="primary",

    use_container_width=True
)


if analyze:

    # --------------------------------------------------------
    # BASIC VALIDATION
    # --------------------------------------------------------

    if not component:

        st.error(
            "Please enter the component name."
        )

        st.stop()


    if not application:

        st.error(
            "Please describe the welding job."
        )

        st.stop()


    if not processes:

        st.error(
            "Please select at least one welding process."
        )

        st.stop()


    # --------------------------------------------------------
    # PREPARE DATA
    # --------------------------------------------------------

    job_data = {

        "component": component,

        "application": application,

        "material_a": material_a,

        "material_b": material_b,

        "thickness_a": thickness_a,

        "thickness_b": thickness_b,

        "cast_condition": cast_condition,

        "condition": condition,

        "purpose": purpose,

        "processes": ", ".join(processes),

        "consumable": consumable,

        "position": position,

        "service": service
    }


    # --------------------------------------------------------
    # RUN AI
    # --------------------------------------------------------

    with st.spinner(
        "Analyzing welding procedure..."
    ):

        try:

            result = run_agent(
                job_data
            )


        except Exception as error:

            st.error(
                "The welding analysis could not be completed."
            )

            st.code(
                str(error)
            )

            st.stop()


    # --------------------------------------------------------
    # SAVE MEMORY
    # --------------------------------------------------------

    save_case({

        "component": component,

        "material_a": material_a,

        "material_b": material_b,

        "purpose": purpose,

        "result": result
    })


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.success(
        "Welding analysis completed."
    )

    st.markdown(result)


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    st.download_button(

        label="⬇️ Download Analysis",

        data=result,

        file_name=(
            f"{component.replace(' ', '_')}"
            "_welding_analysis.txt"
        ),

        mime="text/plain"
    )
