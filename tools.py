import pandas as pd
from crewai.tools import tool


# ---------------------------------------------------------
# Load welding database
# ---------------------------------------------------------

def load_database():
    return pd.read_csv("welding_database.csv")


# ---------------------------------------------------------
# TOOL 1: Search Welding Database
# ---------------------------------------------------------

@tool("search_welding_database")
def search_welding_database(
    material: str,
    process: str,
    thickness_mm: float
) -> str:
    """
    Search the welding database for suitable welding
    process and parameter information.
    """

    df = load_database()

    results = df[
        (df["material"].str.lower() == material.lower()) &
        (df["process"].str.lower() == process.lower()) &
        (df["thickness_min_mm"] <= thickness_mm) &
        (df["thickness_max_mm"] >= thickness_mm)
    ]

    if results.empty:
        return "No matching welding data was found in the database."

    row = results.iloc[0]

    return f"""
Material: {row['material']}
Process: {row['process']}

Thickness range:
{row['thickness_min_mm']} - {row['thickness_max_mm']} mm

Joint types:
{row['joint_types']}

Positions:
{row['positions']}

Filler category:
{row['filler_category']}

Shielding gas:
{row['shielding_gas']}

Polarity:
{row['polarity']}

Current:
{row['current_min_a']} - {row['current_max_a']} A

Voltage:
{row['voltage_min_v']} - {row['voltage_max_v']} V

Notes:
{row['notes']}
"""


# ---------------------------------------------------------
# TOOL 2: Heat Input Calculator
# ---------------------------------------------------------

@tool("calculate_heat_input")
def calculate_heat_input(
    voltage: float,
    current: float,
    travel_speed_mm_min: float,
    efficiency: float
) -> str:
    """
    Calculate approximate welding heat input.

    Result is returned in kJ/mm.
    """

    if travel_speed_mm_min <= 0:
        return "Travel speed must be greater than zero."

    heat_input = (
        voltage * current * 60 * efficiency
    ) / (1000 * travel_speed_mm_min)

    return f"Approximate heat input: {heat_input:.3f} kJ/mm"


# ---------------------------------------------------------
# TOOL 3: Thickness Check
# ---------------------------------------------------------

@tool("check_process_thickness")
def check_process_thickness(
    material: str,
    process: str,
    thickness_mm: float
) -> str:
    """
    Check whether the requested material, process and
    thickness exist in the current welding database.
    """

    df = load_database()

    results = df[
        (df["material"].str.lower() == material.lower()) &
        (df["process"].str.lower() == process.lower()) &
        (df["thickness_min_mm"] <= thickness_mm) &
        (df["thickness_max_mm"] >= thickness_mm)
    ]

    if results.empty:
        return (
            "The requested material/process/thickness combination "
            "was not found in the database. Do not assume suitability."
        )

    return (
        "The material, process and thickness combination "
        "exists in the current reference database."
    )


# ---------------------------------------------------------
# TOOL 4: Professional Review Check
# ---------------------------------------------------------

@tool("check_professional_review")
def check_professional_review(
    application: str
) -> str:
    """
    Determine whether the application should receive
    professional/code review.
    """

    application_lower = application.lower()

    critical_terms = [
        "pressure vessel",
        "boiler",
        "pipeline",
        "lifting",
        "crane",
        "structural",
        "bridge",
        "critical",
        "pressure"
    ]

    for term in critical_terms:
        if term in application_lower:
            return (
                "PROFESSIONAL REVIEW REQUIRED: "
                "This application may involve safety-critical "
                "requirements. Verify the procedure against the "
                "applicable code, qualified WPS/PQR/WPQ and "
                "qualified welding personnel."
            )

    return (
        "Basic preliminary guidance may be provided, but the "
        "final welding procedure should still be verified "
        "against applicable requirements."
    )
