import chainlit as cl
from agents import Agent, Runner, trace, set_default_openai_client, set_default_openai_api, set_trace_processors
from agents.tracing.processor_interface import TracingProcessor
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import agentops

load_dotenv()


client = AsyncOpenAI(
    base_url=os.getenv("EXAMPLE_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)

set_default_openai_client(client=client, use_for_tracing=True)
set_default_openai_api("chat_completions")


#  Tracing
class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace):
        self.traces.append(trace)
        print(f"Trace started: {trace.trace_id}")

    def on_trace_end(self, trace):
        print("Trace ended:")
        print(trace.export())

    def on_span_start(self, span):
        print(f"Span started: {span.span_id}")
        print(span.export())

    def on_span_end(self, span):
        print(f"Span ended: {span.span_id}")
        print(span.export())

    def force_flush(self):
        print("Flushing trace data")

    def shutdown(self):
        print("Shutting down trace processor")

# Set processor
set_trace_processors([LocalTraceProcessor()])

# AgentOps
agentops.init(os.getenv("AGENTOPS_API_KEY"))

@cl.on_message
async def handle_message(message: cl.Message):
    agent = Agent(
        name="Assistant",
        instructions="You are a helpfull assistant",
        model=os.getenv("EXAMPLE_MODEL_NAME") or "gemini-2.0-flash"
    )

    await cl.Message(content="🧠 Thinking...").send()

    
    with trace(workflow_name="Chainlit-assistant"):
        response = await Runner.run(agent, message.content)
        await cl.Message(content=f" Result: {response.final_output}").send()

        






















# import chainlit as cl
# from collections import defaultdict


# user_sessions = defaultdict(dict)

# @cl.on_chat_start
# async def start():
#     await cl.Message(content="✈️ Welcome to TravelAgent AI! I will help you book your flights step by step.").send()
#     await cl.Message(content="Where are you traveling from?").send()


# @cl.on_message
# async def handle_message(message: cl.Message):
#     user_id = getattr(getattr(message, 'author', None), 'id', None) or str(message.author)
#     session = user_sessions[user_id]
#     msg = message.content.strip().lower()


#     if "from" not in session:
#         session["from"] = msg
#         await cl.Message(content="Great! Where do you want to go?").send()
#         return


#     if "to" not in session:
#         session["to"] = msg
#         await cl.Message(content="Nice! What are your travel dates? (e.g., 23 May to 30 May)").send()
#         return


#     if "dates" not in session:
#         session["dates"] = msg
#         await cl.Message(content="What is your maximum budget for the flight? (in PKR)").send()
#         return


#     if "budget" not in session:
#         session["budget"] = msg
#         await cl.Message(content="Thank you! Finding the best flight for you...").send()
#         await suggest_flight(session, user_id)
#         user_sessions.pop(user_id, None)  
#         return


# async def suggest_flight(session, user_id):
#     flight_info = (
#         f"✈️ **Flight Suggestion:**\n"
#         f"From: {session['from'].title()}\n"
#         f"To: {session['to'].title()}\n"
#         f"Dates: {session['dates']}\n"
#         f"Budget: PKR {session['budget']}\n\n"
#         f" Recommended Flight: Serene Air\n"
#         f" Departure: {session['dates'].split(' to ')[0]} — Return: {session['dates'].split(' to ')[1]}\n"
#         f" Fare: PKR 28,500\n"
#         f" Duration: 1h 45m"
#     )

#     await cl.Message(content=flight_info).send()

#     # Optionally make a PDF summary
#     from fpdf import FPDF
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)
#     for line in flight_info.split('\n'):
#         pdf.multi_cell(0, 10, line)
#     filename = f"flight_summary_{user_id}.pdf"
#     pdf.output(filename)

#     await cl.Message(
#         content="📄 Your travel itinerary is ready:",
#         attachments=[cl.File(path=filename, name="flight_summary.pdf")]
#     ).send()





















