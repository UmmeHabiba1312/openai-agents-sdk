import os
import chainlit as cl

from agents import Agent, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv, find_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

agent1 = Agent(
    instructions=(
        "You are an AI tutor who can explain concepts in simple, clear language. "
        "Answer questions about any subject (math, science, history, programming, etc.). "
        "Provide examples or step-by-step explanations when needed."
    ),
    name="AI Tutor"
)


@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(content="Welcome to your AI Tutor. Ask anything, learn instantly!").send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await message.send()

    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    prompt_with_context = [
        {"role": "system", "content": "You are a helpful AI tutor who explains topics clearly and patiently."},
    ] + history

    result = Runner.run_streamed(
        agent1,
        input=prompt_with_context,
        run_config=run_config,
    )

    buffer = ""
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            buffer += event.data.delta
            
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                
                await msg.stream_token(line + "\n")


    if buffer:
        await msg.stream_token(buffer)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)



