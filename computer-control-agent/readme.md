# 🔍 YouTube AI Video Recommender using Gemini + LangChain

This project uses **LangChain**, **Gemini 2.0 (Flash)**, and a custom agent to **search YouTube** and recommend the **best video** based on relevance, views, and content quality — all without playing the video.

---

## 📌 Task Description

> **"Search YouTube for videos on the OpenAI Agents SDK, and recommend the best one based on relevance, views, and quality. Provide the video’s title, channel, URL, and a 100-word summary of its content, highlighting key points and why it’s the best. Do not play any video."**

---

## 🚀 Features

- ✅ Uses **Gemini 2.0 Flash** via Google Generative AI
- ✅ Powered by **LangChain** for LLM orchestration
- ✅ Custom **`Agent` class** for browser-based YouTube search
- ✅ Summarizes and ranks YouTube videos
- ✅ Returns **title**, **channel**, **URL**, and a **100-word summary**

---

## 🧠 Tech Stack

- `langchain_google_genai` – Gemini LLM integration
- `dotenv` – Securely loads API keys from `.env`
- `asyncio` – Async agent execution
- `custom Agent` – Handles search logic and output formatting

---

## 📂 Project Structure

.
├── main.py # Core logic with LLM and agent
├── browser_use.py # Custom Agent logic (YouTube search, scraping, etc.)
├── .env # Contains GEMINI_API_KEY
├── README.md # Project documentation

---

## 🛠️ Setup

1. **Clone the repo**
   git clone https://github.com/your-username/yt-gemini-agent.git

2. **Install Dependencies**
   cd yt-gemini-agent
   Install dependencies

`pip install -r requirements.txt`
### Create a .env file

`GEMINI_API_KEY=your_google_gemini_api_key_here`


 ### Run the agent
python main.py
