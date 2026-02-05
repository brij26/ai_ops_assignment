from llm.llm import get_llm
from langchain_core.prompts import PromptTemplate
from agents.schemas import Plan
from langchain_core.output_parsers import PydanticOutputParser

def planner_agent(user_task: str) -> Plan:
    """
    Generates an execution plan based on the user's task.

    Args:
        user_task (str): The task description provided by the user.

    Returns:
        Plan: The generated plan containing steps to execute.
    """
    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object=Plan)

    prompt = PromptTemplate(
        template="""
You are a planner agent.
Create a step-by-step execution plan.

Available tools:
- weather(city)
- air_quality(city)

{format_instructions}

User task:
{task}
""",
        input_variables=["task"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    response = llm.invoke(prompt.format(task=user_task))
    return parser.parse(response.content)
