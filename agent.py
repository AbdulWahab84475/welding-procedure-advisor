import streamlit as st


# ============================================================
# GROQ / CREWAI COMPATIBILITY PATCH
# ============================================================
#
# CrewAI has had a known cache_breakpoint issue with
# non-Anthropic providers such as Groq.
#
# This must run BEFORE creating the CrewAI LLM.
# ============================================================

try:

    import crewai.llms.cache as crew_cache

    crew_cache.mark_cache_breakpoint = (
        lambda message: message
    )

except Exception:

    pass


# ============================================================
# CREWAI
# ============================================================

from crewai import Agent, Crew, Task, LLM


# ============================================================
# TOOLS
# ============================================================

from tools import (
    material_analysis,
    thickness_analysis,
    cast_component_analysis,
    welding_purpose_analysis,
    process_analysis,
    consumable_analysis,
    temperature_analysis,
    inspection_analysis,
    standards_check
)


# ============================================================
# LLM
# ============================================================

llm = LLM(

    model="groq/openai/gpt-oss-120b",

    api_key=st.secrets["GROQ_API_KEY"],

    temperature=0.1
)


# ============================================================
# WELDING AGENT
# ============================================================

welding_agent = Agent(

    role="Senior Welding Procedure Advisor",

    goal="""
    Analyze welding jobs using a structured
    mechanical engineering decision process.

    Do not jump directly to welding parameters.

    First understand:
    - component
    - materials
    - thickness
    - casting condition
    - welding purpose
    - available welding processes
    - consumable
    - service condition

    Then develop a preliminary welding procedure
    recommendation.
    """,

    backstory="""
    You are an engineering assistant specializing
    in welding procedure analysis.

    Your job is to help a mechanical engineer
    understand a welding problem.

    You must reason in this order:

    1. Understand the component.

    2. Identify both materials.

    3. Check material thickness.

    4. Determine whether a component is cast.

    5. Understand why welding is required.

    6. Check available welding processes.

    7. Evaluate consumable compatibility.

    8. Consider temperature control.

    9. Consider welding sequence.

    10. Consider inspection.

    11. Identify missing information.

    12. Produce a preliminary WPS-style procedure.

    Never invent numerical welding parameters.

    If a numerical value is required but not available
    from verified engineering information, say:

    "Verified value required."

    Distinguish clearly between:
    - database information
    - engineering reasoning
    - missing information

    The result is engineering assistance,
    not a certified WPS.
    """,

    tools=[
        material_analysis,
        thickness_analysis,
        cast_component_analysis,
        welding_purpose_analysis,
        process_analysis,
        consumable_analysis,
        temperature_analysis,
        inspection_analysis,
        standards_check
    ],

    llm=llm,

    verbose=False,

    allow_delegation=False
)


# ============================================================
# RUN FUNCTION
# ============================================================

def run_agent(job_data):

    task_description = f"""
Analyze the following welding engineering case.

==================================================
JOB INFORMATION
==================================================

Component:
{job_data["component"]}

Application:
{job_data["application"]}


==================================================
MATERIAL INFORMATION
==================================================

Material A:
{job_data["material_a"]}

Thickness A:
{job_data["thickness_a"]} mm

Material B:
{job_data["material_b"]}

Thickness B:
{job_data["thickness_b"]} mm


==================================================
COMPONENT CONDITION
==================================================

Is component cast?
{job_data["cast_condition"]}

Current condition / defect:
{job_data["condition"]}


==================================================
WELDING PURPOSE
==================================================

{job_data["purpose"]}


==================================================
AVAILABLE WELDING PROCESSES
==================================================

{job_data["processes"]}


==================================================
CONSUMABLE
==================================================

{job_data["consumable"]}


==================================================
WELDING POSITION
==================================================

{job_data["position"]}


==================================================
SERVICE ENVIRONMENT
==================================================

{job_data["service"]}


==================================================
ENGINEERING ANALYSIS
==================================================

Use the available engineering tools.

Do NOT skip material analysis.

Do NOT skip thickness analysis.

Do NOT skip cast-component analysis.

Do NOT skip welding-purpose analysis.

Do NOT skip process analysis.

Do NOT skip consumable analysis.

Do NOT skip temperature considerations.

Do NOT skip inspection considerations.

Check potentially relevant welding standards.


==================================================
OUTPUT FORMAT
==================================================

Produce the answer using exactly these sections:

# 1. Job Understanding

Explain what the welding job appears to be.

# 2. Material Assessment

Discuss Material A and Material B.

# 3. Thickness Assessment

Discuss the thicknesses and any important implications.

# 4. Cast Component Assessment

State whether casting changes the procedure.

# 5. Welding Purpose

Explain whether this is:
- joining
- repair
- build-up
- dimension restoration
- service-life restoration

# 6. Welding Process

Discuss the available processes and explain
which process should be investigated further.

Do not present this as a certified process selection.

# 7. Consumable / Filler

Discuss the supplied consumable or identify
what information is missing.

# 8. Temperature Control

Explain the temperature-control considerations.

Do not invent numerical temperatures.

# 9. Welding Sequence

Give a practical sequence such as:

1. Preparation
2. Cleaning
3. Pre-weld checks
4. Welding
5. Interpass control
6. Pass cleaning
7. Cooling
8. Finishing

# 10. Inspection

Recommend appropriate inspection methods
and explain why.

# 11. Possible Risks

Identify possible risks such as:

- cracking
- distortion
- excessive heat input
- contamination
- hardness changes
- lack of fusion
- porosity
- dimensional error

Only include risks relevant to this job.

# 12. Missing Information

List information that must be confirmed
before a final WPS can be produced.

# 13. Preliminary WPS Summary

Create a compact table-like summary:

Parameter | Recommendation / Status

Include:

Material
Thickness
Purpose
Process
Consumable
Position
Preheat
Interpass
Current
Voltage
Travel speed
Number of passes
Cooling
Inspection

For parameters that cannot be verified,
write:

"Verified value required."

# 14. Engineering Review

Clearly state what must be reviewed or qualified
before production welding.
"""


    task = Task(

        description=task_description,

        expected_output=(
            "A structured welding engineering advisory "
            "with a preliminary WPS-style summary."
        ),

        agent=welding_agent
    )


    crew = Crew(

        agents=[welding_agent],

        tasks=[task],

        verbose=False
    )


    result = crew.kickoff()

    return str(result)
