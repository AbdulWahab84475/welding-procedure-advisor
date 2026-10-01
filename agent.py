import os

from crewai import Agent, Crew, Task, LLM

from tools import (
    search_welding_database,
    calculate_heat_input,
    check_process_thickness,
    check_professional_review,
)


# Get Groq API key
api_key = os.environ.get("GROQ_API_KEY")


# Groq LLM
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=api_key,
)


# Create the welding agent
welding_agent = Agent(
    role="Welding Procedure Advisor",
    goal="Provide safe and practical preliminary welding procedure guidance.",
    backstory=(
        "You are a welding engineering assistant. "
        "You help users understand welding process selection, "
        "filler materials, shielding gases, and starting parameters. "
        "You must use the provided tools and must not invent technical data."
    ),
    tools=[
        search_welding_database,
        calculate_heat_input,
        check_process_thickness,
        check_professional_review,
    ],
    llm=llm,
    verbose=True,
)


def run_agent(user_request):

    task = Task(
        description=f"""
        Analyze the following welding request:

        {user_request}

        Use the available welding database and tools.

        Provide:

        1. Recommended welding process
        2. Why this process is suitable
        3. Suitable filler category
        4. Shielding gas
        5. Starting parameter range if available
        6. Joint preparation considerations
        7. Possible welding defects
        8. Important safety or qualification notes

        Do not invent welding parameters.

        Clearly state that the result is preliminary guidance
        and is NOT a certified WPS.
        """,
        expected_output="A clear and beginner-friendly welding procedure recommendation.",
        agent=welding_agent,
    )

    crew = Crew(
        agents=[welding_agent],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()

    return result
