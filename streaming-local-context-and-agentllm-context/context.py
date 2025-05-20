# local context

# from pydantic import BaseModel
# from agents import Agent,Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig, function_tool,set_default_openai_client,set_tracing_disabled
# import asyncio
# from dataclasses import dataclass
# from dotenv import load_dotenv
# load_dotenv()
# import os

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# # set_default_openai_client(external_client)
# set_tracing_disabled=True

# @dataclass
# class UserInfo:
#     name: str
#     age: int
#     location:str =  "Pakistan"

# @function_tool
# async def fetch_user_age(wrapper: RunContextWrapper[UserInfo])->str:
#     '''Returns the age of the user'''
#     print(f"[->Tool]  {wrapper} \n\n")
#     return f"User {wrapper.context.name} age is 20 years old."

# @function_tool
# async def fetch_user_location(wrapper: RunContextWrapper[UserInfo])->str:
#     '''Returns the location of the user'''
#     print(f"[->Tool]  {wrapper} \n\n")
#     return f"User {wrapper.context.name} lives in {wrapper.context.location}."

# async def main():
#     user_info = UserInfo(name="Habiba", age=20)

#     agent = Agent[UserInfo](
#         name='Assistant',
#         instructions="You are a helpful assistant. Answer the user's questions.",
#         tools=[fetch_user_age, fetch_user_location],
#         model=model,
#     )

#     response = await Runner.run(
#         agent,
#         input="What is my age of the user? also tell me the location of the user.",
#         context=user_info,
#     )

#     print(response.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())

# llm/agent context


from pydantic import BaseModel
from agents import Agent,Runner, RunContextWrapper, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig, function_tool,set_default_openai_client,set_tracing_disabled
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# set_default_openai_client(external_client)
set_tracing_disabled=True

@dataclass
class UserInfo:
    name: str
    age: int
    location:str =  "Pakistan"

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo])->str:
    '''Returns the age of the user'''
    print(f"[->Tool]  {wrapper} \n\n")
    return f"User {wrapper.context.name} age is 20 years old."

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo])->str:
    '''Returns the location of the user'''
    print(f"[->Tool]  {wrapper} \n\n")


    return f"User {wrapper.context.name} lives in {wrapper.context.location}."

@function_tool
async def greet_user(wrapper: RunContextWrapper[UserInfo])->str:
    '''Returns a greeting message for the user'''
    print(f"[->Tool]  {wrapper} \n\n")
    return f"Hello {wrapper.context.name}, "

async def main():
    user_info = UserInfo(input("Enter your name: "), int(input("Enter your age: ")))
    dynamic_instructions=f"Hello {user_info.name}, welcome to Pnaversity. How can I assist you today?"

    agent = Agent[UserInfo](
        name='Assistant',
        instructions=dynamic_instructions,
        tools=[fetch_user_age, fetch_user_location],
        model=model,
    )

    response = await Runner.run(
        agent,
        input="Hello",
        context=user_info,
    )

    print(response.final_output)


if __name__ == "__main__":
    asyncio.run(main())