from crewai.tools import tool

from database import (
    get_material,
    get_process,
    get_consumable,
    get_inspection,
    get_rules,
    get_standards
)

from welding_data import (
    CAST_MATERIALS,
    CRITICAL_APPLICATIONS,
    PURPOSE_DESCRIPTIONS
)


@tool("material_analysis")
def material_analysis(
    material_a: str,
    material_b: str
) -> str:
    """
    Analyze the two materials involved in the welding job.
    """

    data_a = get_material(material_a)
    data_b = get_material(material_b)

    result = f"""
MATERIAL ANALYSIS

Material A:
{material_a}

Group:
{data_a.get("group", "Unknown")}

Weldability:
{data_a.get("general_weldability", "Unknown")}

Important checks:
{data_a.get("important_checks", [])}

Material B:
{material_b}

Group:
{data_b.get("group", "Unknown")}

Weldability:
{data_b.get("general_weldability", "Unknown")}

Important checks:
{data_b.get("important_checks", [])}
"""

    return result


@tool("thickness_analysis")
def thickness_analysis(
    thickness_a: float,
    thickness_b: float
) -> str:
    """
    Analyze thickness information.
    """

    difference = abs(
        thickness_a - thickness_b
    )

    return f"""
THICKNESS ANALYSIS

Material A thickness:
{thickness_a} mm

Material B thickness:
{thickness_b} mm

Thickness difference:
{difference:.2f} mm

Engineering considerations:
- Joint design may depend on thickness.
- Welding heat input may be affected.
- Number of passes may depend on joint design.
- Distortion and thermal effects should be considered.
- Final parameters must come from qualified procedure data.
"""


@tool("cast_component_analysis")
def cast_component_analysis(
    material_a: str,
    material_b: str,
    cast_condition: str
) -> str:
    """
    Analyze whether a casting requires special consideration.
    """

    cast_material_detected = (
        material_a in CAST_MATERIALS
        or material_b in CAST_MATERIALS
    )

    if cast_condition == "Yes" or cast_material_detected:

        rules = get_rules("cast_component")

        return """
CAST COMPONENT DETECTED

Special attention is required.

Recommended assessment:

""" + "\n".join(
            f"- {rule}"
            for rule in rules
        )

    if cast_condition == "Unknown":

        return """
CAST CONDITION UNKNOWN

The engineer/user should confirm whether
the component is cast before finalizing
the welding procedure.
"""

    return """
No casting has been identified from the supplied information.
"""


@tool("welding_purpose_analysis")
def welding_purpose_analysis(
    purpose: str
) -> str:
    """
    Analyze why welding is required.
    """

    description = PURPOSE_DESCRIPTIONS.get(
        purpose,
        "Purpose not recognized."
    )

    if "Repair" in purpose:

        rules = get_rules("repair")

    elif (
        "Build-up" in purpose
        or "dimension" in purpose.lower()
        or "service life" in purpose.lower()
    ):

        rules = get_rules("build_up")

    else:

        rules = [
            "Confirm joint configuration.",
            "Confirm required joint properties.",
            "Select compatible welding process.",
            "Select compatible consumable.",
            "Define inspection requirements."
        ]

    return f"""
WELDING PURPOSE

Purpose:
{purpose}

Description:
{description}

Engineering workflow:

""" + "\n".join(
        f"- {rule}"
        for rule in rules
    )


@tool("process_analysis")
def process_analysis(
    available_processes: str
) -> str:
    """
    Analyze available welding processes.
    """

    processes = [
        process.strip()
        for process in available_processes.split(",")
    ]

    results = []

    for process in processes:

        data = get_process(process)

        if not data:

            results.append(
                f"{process}: No database information."
            )

            continue

        results.append(
            f"""
{process}

Typical use:
{data.get("typical_use", [])}

Advantages:
{data.get("advantages", [])}

Limitations:
{data.get("limitations", [])}
"""
        )

    return "\n".join(results)


@tool("consumable_analysis")
def consumable_analysis(
    consumable: str
) -> str:
    """
    Check welding consumable information.
    """

    if not consumable:

        return """
No consumable was supplied.

The agent should identify the required
filler/consumable information that is missing.
"""

    data = get_consumable(consumable)

    if not data:

        return f"""
Consumable:
{consumable}

This consumable is not currently available
in the internal database.

Verify it using the manufacturer datasheet
or qualified welding documentation.
"""

    return f"""
CONSUMABLE ANALYSIS

Consumable:
{consumable}

Process:
{data.get("process", "Unknown")}

Material group:
{data.get("material_group", "Unknown")}

Note:
{data.get("note", "")}
"""


@tool("temperature_analysis")
def temperature_analysis(
    material_a: str,
    material_b: str,
    cast_condition: str,
    thickness_a: float,
    thickness_b: float
) -> str:
    """
    Determine whether temperature control requires attention.
    """

    casting = (
        cast_condition == "Yes"
        or material_a in CAST_MATERIALS
        or material_b in CAST_MATERIALS
    )

    if casting:

        return """
TEMPERATURE CONTROL

Casting is involved.

Do not automatically assign a numerical
preheat or interpass temperature.

Check:
- Qualified WPS/PQR
- Exact casting grade
- Thickness
- Manufacturer information
- Applicable code
- Engineering approval
- Controlled cooling requirements
"""

    return f"""
TEMPERATURE CONTROL

Material A:
{material_a}

Material B:
{material_b}

Thickness:
{thickness_a} mm / {thickness_b} mm

No universal numerical temperature has been
assigned by this tool.

The final value should be supported by:
- Qualified WPS/PQR
- Applicable code
- Material specification
- Manufacturer data
- Engineering review
"""


@tool("inspection_analysis")
def inspection_analysis(
    material_a: str,
    material_b: str,
    purpose: str,
    cast_condition: str
) -> str:
    """
    Recommend possible inspection methods.
    """

    methods = [
        "Visual Inspection"
    ]

    if (
        "Repair" in purpose
        or cast_condition == "Yes"
    ):

        methods.append("DPT or MT where applicable")

    methods.append(
        "UT where volumetric examination is required"
    )

    methods.append(
        "RT where specifically required"
    )

    return """
INSPECTION CONSIDERATIONS

Possible methods:

""" + "\n".join(
        f"- {method}"
        for method in methods
    )


@tool("standards_check")
def standards_check(
    application: str
) -> str:
    """
    Identify potentially relevant welding standards.
    """

    application_lower = application.lower()

    results = []

    for name, description in get_standards().items():

        results.append(
            f"- {name}: {description}"
        )

    critical = any(
        item in application_lower
        for item in CRITICAL_APPLICATIONS
    )

    result = """
POTENTIALLY RELEVANT STANDARDS

""" + "\n".join(results)

    if critical:

        result += """

IMPORTANT:
The application appears potentially safety-critical.
Applicable code requirements and qualified welding
procedures must be confirmed before use.
"""

    return result
