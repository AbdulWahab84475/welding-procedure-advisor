import os

from crewai import Agent, LLM

from tools import (
    search_welding_database,
    calculate_heat_input,
    check_process_thickness,
    check_professional_review
)


# ---------------------------------------------------------
# Groq LLM
# ---------------------------------------------------------

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY")
)


# ---------------------------------------------------------
# Welding Procedure Advisor
# ---------------------------------------------------------

welding_agent = Agent(
    role="Welding Procedure Advisor",

    goal="""
    Analyze welding requirements and provide clear,
    preliminary welding procedure guidance using the
    available engineering database and tools.
    """,

    backstory="""
    You are a mechanical engineering welding advisor.

    You help users understand welding process selection,
    filler categories, shielding gas, preliminary parameter
    ranges, joint preparation considerations and possible
    welding defects.

    You must use the available engineering tools instead
    of inventing welding data.

    You must clearly state when information is missing.

    You must never present preliminary guidance as a
    certified or approved Welding Procedure Specification.

    For safety-critical applications, recommend review by
    a qualified welding professional and verification
    against the applicable code and qualified WPS/PQR/WPQ.
    """,

    llm=llm,

    tools=[
        search_welding_database,
        calculate_heat_input,
        check_process_thickness,
        check_professional_review
    ],

    verbose=True
) 
from crewai import Task, Crew


def create_welding_task(user_request: str):

    task = Task(
        description=f"""
        Analyze the following welding request:

        {user_request}

        Follow this process:

        1. Identify the material.
        2. Identify material thickness.
        3. Identify joint type.
        4. Identify welding position.
        5. Identify available welding process.
        6. Identify application and production requirements.
        7. Use the welding database when relevant.
        8. Use engineering tools when calculations are needed.
        9. Identify missing information.
        10. Provide a preliminary recommendation.
        11. Explain why the recommendation is suitable.
        12. Mention important risks or possible defects.
        13. State whether professional/code review is required.

        Do not invent parameter values.
        Use the available database and tools.

        Keep the answer simple and easy for a beginner
        to understand.
        """,

        expected_output="""
        A structured welding procedure advisory containing:

        1. Recommended process
        2. Reason
        3. Filler category
        4. Shielding gas
        5. Preliminary parameter range
        6. Joint preparation considerations
        7. Potential defects
        8. Missing information
        9. Safety/qualification note
        """,

        agent=welding_agent
    )

    return task
  def run_agent(user_request: str):

    task = create_welding_task(user_request)

    crew = Crew(
        agents=[welding_agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()

    return str(result)
