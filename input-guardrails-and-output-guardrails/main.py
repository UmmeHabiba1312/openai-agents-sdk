import asyncio
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

from dotenv import load_dotenv
import os
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it to your Gemini API key.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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

# Guardrail 
# class MathHomeworkOutput(BaseModel):
#     is_math_homework: bool
#     reasoning: str
#     answer: str

# guardrail_agent = Agent(
#     name="Guardrail check",
#     instructions="Check if the user is asking you to do their math homework.",
#     output_type=MathHomeworkOutput,
#     model=model,
# )

# # respose = Runner.run_sync(
# #     guardrail_agent,
# #     "What is the capital of pakistan ?"

# # )

# # print("is_math_homework : ", respose.final_output.is_math_homework)
# # print("Reasoning :",respose.final_output.reasoning)
# # print("Answer : ",respose.final_output.answer)

# # output
# # is_math_homework :  False
# # Reasoning : The question is about geography, not mathematics.
# # Answer :  Islamabad


# # input guardrail
# @input_guardrail
# async def math_guardrail(
#     ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config = config)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         # tripwire_triggered=False #result.final_output.is_math_homework,
#         tripwire_triggered=result.final_output.is_math_homework,
#     )

# agent = Agent(
#     name="Customer support agent",
#     instructions="You are a customer support agent. You help customers with their questions.",
#     input_guardrails=[math_guardrail],
#     model=model,
# )

# # This should trip the guardrail

# async def main():
#     try:
#         result = await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?", run_config=config)
#         print("Guardrail didn't trip - this is unexpected")
#         print(result.final_output)

#     except InputGuardrailTripwireTriggered:
#         print("Math homework guardrail tripped")

#     try:
#         result = await Runner.run(agent, "Hello", run_config=config)
#         print(result.final_output)

#     except InputGuardrailTripwireTriggered:
#         print("Math homework guardrail tripped")

#     try:
#         result = await Runner.run(agent, "can you solve 2+3 for me", run_config=config)
#         print(result.final_output)

#     except InputGuardrailTripwireTriggered:
#         print("Math homework guardrail tripped")

# if __name__ == "__main__":
#     asyncio.run(main())





# output_guardrail
class MessageOutput(BaseModel):
    response: str

class MathOutput(BaseModel):
    is_math: bool
    reasoning: str
    answer: str

guardrail_agent2 = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail2(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent2, output.response, context=ctx.context, run_config = config)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent2 = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail2],
    output_type=MessageOutput,
    model=model,
)

async def main2():
    # This should trip the guardrail
    try:
        result =await Runner.run(agent2, "Hello, can you help me solve for x: 2x + 3 = 11?", run_config = config)
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main2())