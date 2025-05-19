# from agents import Agent , Runner ,AsyncOpenAI, OpenAIChatCompletionsModel , set_tracing_disabled, set_default_openai_client
# from dotenv import load_dotenv
# import os
# from openai import AsyncOpenAI

# load_dotenv()

# # Setup
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# client = AsyncOpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=OPENROUTER_API_KEY,
# )

# set_tracing_disabled(disabled=True) 
# set_default_openai_client(client)
# model = OpenAIChatCompletionsModel(
#     model = "deepseek/deepseek-chat-v3-0324:free" ,
#     openai_client=client,
# )

# agent:Agent = Agent(
#     name="PanaCloud assistant",
#     instructions="You are a helpful assistant. Answer the questions as best as you can.",
#     model=model,

# )

# result = Runner.run_sync(
#     agent,
#     "Hi?",
# )

# print(result.final_output)


# tracing
from agents import Agent , Runner, function_tool ,AsyncOpenAI, set_tracing_disabled, set_default_openai_client, set_default_openai_api
from dotenv import load_dotenv
import os
load_dotenv()
from agents import enable_verbose_stdout_logging
from agents.extensions.visualization import draw_graph
# Helps track what the program is doing by printing detailed logs to the console.
# is mein just kuch model he hein jo too caling ko support krtey bhein isi liye gemini use kiya h 
enable_verbose_stdout_logging()

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
set_tracing_disabled(True) 
set_default_openai_api('chat_completions')


client = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GEMINI_API_KEY,
)
set_default_openai_client(client)
@function_tool
def get_weather(city : str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is sunny."

@function_tool
def get_news(industry : str) -> str:
    """Get the weather for a given city."""
    return f"The  {industry} has the new concept of  Agentic AI ."


panaversity_agent:Agent = Agent(
    name="panaversity assistant",
    instructions="You are a helpful panaversity assistant.you Answer all about the panaversity(PIAIC).",
    model="gemini-2.0-flash",
    handoff_description="panaversity expert"
    # tools=[get_weather,get_news]
)

agenticai_agent:Agent = Agent(
    name="agenticai assistant",
    instructions="You are a helpful agenticai assistant.you Answer  all about the agentic ai.",
    model="gemini-2.0-flash",
    handoff_description="agenticai expert"
    # tools=[get_weather,get_news]
)

triage_agent : Agent = Agent(
    name='Triage Agent',
    instructions='You are genearl chat assisstant . Observe the communication with user and response according to its quariies using other agents',
    model='gemini-1.5-flash',
    handoffs=[panaversity_agent,agenticai_agent]
)

result = Runner.run_sync(
    triage_agent,
    "what is agentic ai?",
    # "who is the founder of panaversity?",
    # "Hi?",
)

print(result.final_output)
print(result.last_agent.name)
print(draw_graph(triage_agent))