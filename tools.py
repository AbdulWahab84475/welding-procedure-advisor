import pandas as pd

from crewai.tools import tool


# --------------------------------------------------
# Tool 1: Search Welding Database
# --------------------------------------------------

@tool("Search Welding Database")
def search_welding_database(
    material: str,
    process: str,
    thickness_mm: float,
) -> str:
    """
    Search the welding database for a material,
    welding process, and thickness.
    """

    df = pd.read_csv("welding_database.csv")

    result = df[
        (df["material"].str.lower() == material.lower())
        & (df["process"].str.lower() == process.lower())
        & (df["thickness_min_mm"] <= thickness_mm)
        & (df["thickness_max_mm"] >= thickness_mm)
    ]

    if result.empty:
        return "No matching welding procedure data was found."

    return result.to_string(index=False)


# --------------------------------------------------
# Tool 2: Heat Input Calculator
# --------------------------------------------------

@tool("Calculate Welding Heat Input")
def calculate_heat_input(
    voltage: float,
    current: float,
    travel_speed_mm_min: float,
    efficiency: float = 0.8,
) -> str:
    """
    Calculate approximate welding heat input in kJ/mm.
    """

    if travel_speed_mm_min <= 0:
        return "Travel speed must be greater than zero."

    heat_input = (
        voltage
        * current
        * 60
        * efficiency
    ) / (1000 * travel_speed_mm_min)

    return f"Approximate heat input: {heat_input:.3f} kJ/mm"


# --------------------------------------------------
# Tool 3: Process and Thickness Check
# --------------------------------------------------

@tool("Check Process Thickness")
def check_process_thickness(
    material: str,
    process: str,
    thickness_mm: float,
) -> str:
    """
    Check whether the database contains the requested
    material, welding process, and thickness.
    """

    df = pd.read_csv("welding_database.csv")

    result = df[
        (df["material"].str.lower() == material.lower())
        & (df["process"].str.lower() == process.lower())
        & (df["thickness_min_mm"] <= thickness_mm)
        & (df["thickness_max_mm"] >= thickness_mm)
    ]

    if result.empty:
        return (
            "No matching combination was found in the "
            "starter welding database."
        )

    return "The requested material, process, and thickness are covered by the database."


# --------------------------------------------------
# Tool 4: Professional Review Check
# --------------------------------------------------

@tool("Check Professional Review")
def check_professional_review(application: str) -> str:
    """
    Check whether professional/code review may be required.
    """

    critical_terms = [
        "pressure vessel",
        "boiler",
        "pipeline",
        "lifting",
        "crane",
        "bridge",
        "structural",
        "critical",
        "pressure",
    ]

    application_lower = application.lower()

    found_terms = [
        term for term in critical_terms
        if term in application_lower
    ]

    if found_terms:
        return (
            "Professional/code review is required or strongly recommended "
            f"because the application includes: {', '.join(found_terms)}."
        )

    return (
        "No obvious safety-critical application term was detected. "
        "Normal engineering review is still recommended."
    )
