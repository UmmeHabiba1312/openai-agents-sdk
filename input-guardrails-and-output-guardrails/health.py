from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
    RunConfig,
    RunContextWrapper,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,

)
import asyncio

from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it to your Gemini API key.")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

class PersonalHealth(BaseModel):
    is_math:bool
    reasoning:str
    answer:str

guardrail_agent = Agent(
    name = "Guardrail check",
    instructions = "Check if the output includes math questions.",
    output_type = PersonalHealth,
    model = model,
)

@input_guardrail
async def math_guardrail(
    contxt:RunContextWrapper[None],
    agent:Agent,
    input: str | list[TResponseInputItem],
)-> GuardrailFunctionOutput:
    response = await Runner.run(guardrail_agent,input,context=contxt.context)

    print(f"Response: {response.final_output}")
    return GuardrailFunctionOutput(
        output_info=response.final_output,
        tripwire_triggered=response.final_output.is_math,
    )

@output_guardrail
async def guardrail_output(
    contxt:RunContextWrapper[None],
    agent:Agent,
    input: str | list[TResponseInputItem],
)-> GuardrailFunctionOutput:
    response = await Runner.run(guardrail_agent,input,context=contxt.context)

    print(f"Response: {response.final_output}")
    print(f"Answer: {response.final_output.answer}")
    return GuardrailFunctionOutput(
        output_info=response.final_output,
        tripwire_triggered=response.final_output.is_math is False,
    )

agent = Agent(
    name="Health check",
    instructions="You are a Health check agent. Help if the user is asking you to do their health check.",
    input_guardrails=[math_guardrail],
    output_guardrails=[guardrail_output],
    model=model,
    output_type=str,
)

inputs = input("Enter your health check query: ")

async def main():
    try:
        response = await Runner.run(agent, inputs, run_config=config)
        print("is_health_check : ", response.final_output)

    except InputGuardrailTripwireTriggered:
        print("Health guardrail not tripped")

    except OutputGuardrailTripwireTriggered:
        print("Health guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main())