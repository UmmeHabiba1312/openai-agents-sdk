import asyncio
from openai import AsyncOpenAI


from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,function_tool,ItemHelpers,set_default_openai_api,set_default_openai_client,set_tracing_disabled
from agents.run import RunConfig

import os
from dotenv import load_dotenv
load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")


# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)
set_tracing_disabled=True
# os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner
import random
@function_tool
async def how_many_joke()->int:
    return random.randint(1, 10)

async def main():
    agent = Agent(
        name="Joker",
        instructions="first call 'how_many_joke' then tell me that many fresh jokes.",
        tools=[how_many_joke],
        model=model
    )

    result = Runner.run_streamed(agent, input="Hello, tell me jokes")
    # print(type(result),result,"\n\n")
    async for event in result.stream_events():
        # print(event)
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent Updated : {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("Tool was called")
            elif event.item.type == "tool_call_output_item":
                print("Tool call output:", event.item.output)
            elif event.item.type == "message_output_item":
                print("Message output:", ItemHelpers.text_message_output(event.item))
            else:
                pass


asyncio.run(main())