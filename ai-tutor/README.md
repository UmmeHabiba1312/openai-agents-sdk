# AI Tutor Chatbot

An interactive AI Tutor chatbot built with Chainlit and Google Gemini API.  
It can answer questions on any subject with clear, simple explanations and step-by-step guidance    ideal for students seeking help with math, science, history, programming, and more.


## Create and activate a virtual environment:


python -m venv .venv
source .venv/bin/activate    
#### On Windows: 
`.venv\Scripts\activate`


## Install dependencies:

`pip install -r requirements.txt`

`uv pip install openai-agents`

## Create a .env file in the project root and add  Gemini API key:


GEMINI_API_KEY=your_gemini_api_key_here

## Running the Project
Start the Chainlit app with:

`chainlit run your_script_name.py -w`
