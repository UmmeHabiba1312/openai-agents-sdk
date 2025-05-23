# without openapi key

from dotenv import load_dotenv
import os
load_dotenv()
from openai import AsyncOpenAI
from agents import Agent, Runner, trace, set_default_openai_api, set_default_openai_client, set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from pprint import pprint


BASE_URL = os.getenv("EXAMPLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/"
API_KEY = os.getenv("GEMINI_API_KEY") 
MODEL_NAME = os.getenv("EXAMPLE_MODEL_NAME") or "gemini-2.0-flash"
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

# Custom trace processor to collect trace data locally
class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started: {trace.trace_id}")

    def on_trace_end(self, trace):
        print(f"Trace ended: {trace.export()}")

    def on_span_start(self, span):
        self.spans.append(span)
        print(f"Span started: {span.span_id}")
        print(f"Span details: ")
        pprint(span.export())

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(f"Span details:")
        pprint(span.export())

    def force_flush(self):
        print("Forcing flush of trace data")

    def shutdown(self):
        print("=======Shutting down trace processor========")
        # Print all collected trace and span data
        print("Collected Traces:")
        for trace in self.traces:
            print(trace.export())
        print("Collected Spans:")
        for span in self.spans:
            print(span.export())


if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code.")

# Create OpenAI client
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# Configure the client
set_default_openai_client(client=client, use_for_tracing=True)
set_default_openai_api("chat_completions")

# Set up the custom trace processor
local_processor = LocalTraceProcessor()
set_trace_processors([local_processor])

# Example function to run an agent and collect traces
import asyncio
key="1bb99a78-22ce-46a8-aa2b-791ab9af5886" 
import agentops
async def main():
    agentops.init(key)
    agent = Agent( name="CareerHelper",
    instructions="You are a professional resume assistant who helps improve resumes and write custom cover letters for job roles.", model=MODEL_NAME)
    first_result = await Runner.run(agent, "Start the task")
    second_result = await Runner.run(agent, f"Rate this result: {first_result.final_output}")
    print(f"Result: {first_result.final_output}")
    print(f"Rating: {second_result.final_output}")

# Run the main function

asyncio.run(main())




# with openapi key 
# from pydantic import BaseModel
# from agents import Agent,Runner,trace,AsyncOpenAI, RunConfig, OpenAIChatCompletionModel
# import asyncio
# from dotenv import load_dotenv
# import os
# load_dotenv()
# api_key=os.getenv("OPENAI_API_KEY")
# model= OpenAIChatCompletionModel(
#         api_key=api_key,
#         model="gpt-3.5-turbo",
# )

# async def main():
#     agent = Agent(
#     name ="Joke generator",
#     description ="This is a joke generator",
#     model = model
# )

#     with trace():
#         first_response = await Runner.run(agent, "tell a joke")
#         second_response = await Runner.run(agent, f"rate this joke {first_response.final_output}")
#         print(f"Joke {first_response.final_output}")
#         print(f"Rating {second_response.final_output}")


# tracing without opanai api key
# local_processor = LocalTraceProcessor()
# set_trace_processors([local_processor])