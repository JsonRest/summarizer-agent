"""
ADK Text Summarization Agent
Requirements: pip install google-adk python-dotenv
Python: 3.10+

Run locally:  adk run summarizer_agent
Run with UI:  adk web
Deploy:       adk deploy cloud_run ...
"""

import os
from dotenv import load_dotenv
from google.adk import Agent

# ── Load environment variables from .env ─────────────────────────────────────
# Expected .env entries:
#   GOOGLE_CLOUD_PROJECT=your-project-id
#   GOOGLE_CLOUD_LOCATION=us-central1
#   GOOGLE_GENAI_USE_VERTEXAI=True
#   MODEL=gemini-2.0-flash

load_dotenv()

model_name = os.getenv("MODEL", "gemini-2.5-flash")

# ── Define the Agent ──────────────────────────────────────────────────────────
# ADK requires the main agent variable to be named `root_agent`.
# The adk run, adk web, and adk deploy cloud_run commands all
# discover the agent via this name automatically.

root_agent = Agent(
    name="text_summarizer",
    model=model_name,
    description="An agent that summarizes any text input into a concise summary.",
    instruction="""
    You are a professional text summarization assistant.
    When the user provides a block of text, respond with:
    1. A concise summary (2–3 sentences max)
    2. 3 key bullet points from the text

    Be clear, accurate, and avoid adding information not present in the original text.
    """,
)