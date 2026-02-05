from agents.schemas import Plan, ExecutionResult
from tools.weather_tool import WeatherTool
from tools.air_quality_tool import AirQualityTool

weather = WeatherTool()
air = AirQualityTool()

def executor_agent(plan: Plan):
    """
    Executes the steps outlined in the plan using available tools.

    Args:
        plan (Plan): The plan to execute.

    Returns:
        list[ExecutionResult]: A list of results from executing each step.
    """
    results = []

    for step in plan.steps:
        if step.tool == "weather":
            output = weather.get_weather(step.input)
        elif step.tool == "air_quality":
            output = air.get_air_quality(step.input)

        results.append(
            ExecutionResult(
                step=step.description,
                output=output
            )
        )

    return results
