from llm.llm import get_llm
from langchain_core.prompts import PromptTemplate
from agents.schemas import FinalAnswer
from langchain_core.output_parsers import PydanticOutputParser

def verifier_agent(task, execution_result):
    """
    Verifies the execution results and synthesizes a final answer.

    Args:
        task (str): The original user task.
        execution_result (list): The results from the executor agent.

    Returns:
        FinalAnswer: The final answer structured according to the schema.
    """
    llm = get_llm()

    parser = PydanticOutputParser(pydantic_object=FinalAnswer)

    prompt = PromptTemplate(
        template="""
You are a verifier agent.
Validate and consolidate results into final answer.

{format_instructions}

Task:
{task}

Execution result:
{result}
""",
        input_variables=["task", "result"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )

    response = llm.invoke(
        prompt.format(
            task=task,
            result=str(execution_result)
        )
    )

    return parser.parse(response.content)
