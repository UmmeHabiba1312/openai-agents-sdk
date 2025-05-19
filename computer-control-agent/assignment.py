from dotenv import load_dotenv
import os
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel


load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


set_tracing_disabled(disabled=True)


MODEL = "openai/gpt-3.5-turbo"



web_development_agent = Agent(
    name="Web Development Assistant",
    instructions="You are strictly a frontend web development expert. Only answer questions specifically about HTML, CSS, JavaScript, React, or Next.js. Do not respond to mobile, DevOps, or AI agent-related queries.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    handoff_description="Handles all web development-related queries.",
)

mobile_development_agent = Agent(
    name="Mobile Development Assistant",
    instructions="You are strictly a mobile development expert. Only answer questions about React Native or Flutter mobile apps. Do not respond to web, DevOps, or AI agent-related questions.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    handoff_description="Handles all mobile app development queries.",
)

openai_agent = Agent(
    name="OpenAI Agent SDK Expert",
    instructions="You are an expert in the OpenAI Agents SDK. Only answer questions about building custom agents, tools, or agent-based workflows using OpenAI's SDK. Ignore questions outside this scope.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)

devops_agent = Agent(
    name="DevOps Expert",
    instructions="You are an expert in DevOps. Only answer questions specifically about CI/CD, Docker, Kubernetes, GitHub Actions, infrastructure as code, or cloud deployments. Do not respond to unrelated topics.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
)



openai_tool = openai_agent.as_tool(
    tool_name="openai_sdk_helper",
    tool_description="Provides guidance on using the OpenAI Agents SDK effectively."
)

devops_tool = devops_agent.as_tool(
    tool_name="devops_expert",
    tool_description="Provides help on DevOps topics."
)

agentic_ai_agent = Agent(
    name="Agentic AI Assistant",
    instructions="""
        You are an expert in Agentic AI architectures. 
        If a question is specifically about DevOps, CI/CD, cloud infrastructure, etc., use the `devops_expert` tool.
        If the question is about OpenAI Agents SDK or how to build tools/agents, use the `openai_sdk_helper` tool.
        Do NOT answer these questions yourself — delegate them to the appropriate tool.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    handoff_description="Handles questions related to agent-based AI systems.",
    tools=[openai_tool, devops_tool],
)


panacloud_agent = Agent(
    name="Panacloud Assistant",
    instructions="You are the main assistant for the Panacloud platform. Route queries strictly to the correct assistant: web, mobile, or agentic AI. Never answer directly yourself.",
    model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    handoffs=[web_development_agent, mobile_development_agent, agentic_ai_agent],
)


result = Runner.run_sync(panacloud_agent, "tell me about the openai-agents sdk")

print("Response:", result.final_output)
print("Handled by:", result.last_agent.name)

