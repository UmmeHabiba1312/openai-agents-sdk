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

    buffer = ""  # buffer for accumulating tokens
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            buffer += event.data.delta
            # Check if buffer contains newline(s)
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                # Here, you can execute the line or send it to the frontend
                await msg.stream_token(line + "\n")

    # send any remaining buffered content
    if buffer:
        await msg.stream_token(buffer)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)










# x² - 5x + 6 = 0




















# import os
# import chainlit as cl

# from agents import Agent , RunConfig , AsyncOpenAI, OpenAIChatCompletionsModel , Runner
# from dotenv import load_dotenv , find_dotenv
# from openai.types.responses import ResponseTextDeltaEvent

# load_dotenv(find_dotenv())
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# # for streaming

# #step-1 providor
# # same for 3 ( sync, async, streaming)
# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# #step-2 model
# model = OpenAIChatCompletionsModel(
#     # update model for streaming
#     model="gemini-2.0-flash",
#     # model="gemini-2.0-flash",
#     openai_client=provider,
#     )

# # step-3 config = define  at run level
# run_config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True,
#     )

# # step 4 agent
# agent1 = Agent(
#     instructions="You are a helpfull assisstant taht can answer the quetsions",
#     name="Support agent"
# )



# # step-5 run synchronously
# # result = Runner.run_sync(
# #     agent1,
# #     input="What is the capital of France?",
# #     run_config=run_config,   
# # )

# # print(result.final_output)


# @cl.on_chat_start
# async def handle_chat_start():
#     cl.user_session.set("history", [])
#     await cl.Message(content="Welcome to Ummehabia Support Agent !").send()


# # run asynchronously
# # @cl.on_message
# # async def main(message: cl.Message):
# #     history = cl.user_session.get("history")
# #     history.append({"role":"user", "content":message.content})
# #     result = await Runner.run(
# #         agent1,
# #         input=history,
# #         run_config=run_config,   
# #     )
# #     history.append({"role":"assistant", "content":result.final_output})
# #     cl.user_session.set("history", history)
# #     await cl.Message(content=result.final_output).send()




#     # run streaming
# @cl.on_message
# async def main(message: cl.Message):

#     msg = cl.Message(content="")
#     await message.send()



#     history = cl.user_session.get("history")
#     history.append({"role":"user", "content":message.content})
#     result =Runner.run_streamed(
#         agent1,
#         input=history,
#         run_config=run_config,   

#     )
#     async for event in result.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
#             await msg.stream_token(event.data.delta)
#     history.append({"role":"assistant", "content":result.final_output})
#     cl.user_session.set("history", history)
#     # await cl.Message(content=result.final_output).send()


# # uv run python 
# # -m chainlit run hello.py -w