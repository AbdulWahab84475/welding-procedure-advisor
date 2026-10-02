# ============================================================
# WELDING DATA
# Basic engineering classifications and decision rules
# ============================================================


MATERIAL_GROUPS = {
    "Mild Steel": "Carbon steel",

    "AISI 1045": "Medium-carbon steel",

    "Stainless Steel 304": "Austenitic stainless steel",

    "Stainless Steel 316": "Austenitic stainless steel",

    "Stainless Steel 316L": "Austenitic stainless steel",

    "Cast Iron": "Cast iron",

    "Ductile Iron": "Ductile cast iron",

    "Aluminum 6061": "Aluminum alloy"
}


CAST_MATERIALS = [
    "Cast Iron",
    "Ductile Iron"
]


WELDING_PURPOSES = [
    "Joining two components",
    "Repair a defect",
    "Build-up worn area",
    "Restore original dimension",
    "Increase service life"
]


WELDING_PROCESSES = [
    "SMAW",
    "GMAW",
    "GTAW",
    "FCAW"
]


INSPECTION_METHODS = [
    "Visual Inspection",
    "DPT",
    "MT",
    "UT",
    "RT"
]


CRITICAL_APPLICATIONS = [
    "pressure vessel",
    "pipeline",
    "lifting equipment",
    "structural component",
    "safety critical"
]


ENGINEERING_STANDARDS = {

    "AWS D1.1": (
        "Structural welding code for applicable "
        "steel structures."
    ),

    "ASME Section IX": (
        "Qualification framework for welding "
        "and brazing procedures/personnel."
    ),

    "ISO 15614": (
        "Specification and qualification of "
        "welding procedures."
    ),

    "ISO 9606": (
        "Qualification testing of welders."
    ),

    "ISO 17637": (
        "Visual testing of fusion-welded joints."
    )
}


SAFETY_RULES = [

    (
        "Do not treat this application as a "
        "qualified WPS."
    ),

    (
        "Do not invent welding current, voltage, "
        "preheat or interpass values."
    ),

    (
        "Final welding parameters must be supported "
        "by qualified procedure data, applicable "
        "standards, manufacturer information or "
        "engineering approval."
    ),

    (
        "Cast component repairs require additional "
        "assessment."
    )
]


PURPOSE_DESCRIPTIONS = {

    "Joining two components": (
        "Permanent joining of two separate components."
    ),

    "Repair a defect": (
        "Restoration of a damaged or defective area."
    ),

    "Build-up worn area": (
        "Adding weld metal to restore worn material."
    ),

    "Restore original dimension": (
        "Restoring a component to its required "
        "original or specified dimension."
    ),

    "Increase service life": (
        "Welding intended to restore or improve "
        "functional service life."
    )
}
