import streamlit as st


def initialize_memory():

    if "welding_memory" not in st.session_state:

        st.session_state.welding_memory = []


def save_case(case):

    initialize_memory()

    st.session_state.welding_memory.append(
        case
    )

    # Keep only the latest 5 cases
    st.session_state.welding_memory = (
        st.session_state.welding_memory[-5:]
    )


def get_memory():

    initialize_memory()

    return st.session_state.welding_memory


def clear_memory():

    st.session_state.welding_memory = []


def get_memory_summary():

    cases = get_memory()

    if not cases:

        return "No previous welding cases."

    summary = []

    for number, case in enumerate(
        cases,
        start=1
    ):

        summary.append(
            f"""
Case {number}

Component:
{case.get("component", "Unknown")}

Material A:
{case.get("material_a", "Unknown")}

Material B:
{case.get("material_b", "Unknown")}

Purpose:
{case.get("purpose", "Unknown")}

Result:
{case.get("result", "No result")}
"""
        )

    return "\n".join(summary)
