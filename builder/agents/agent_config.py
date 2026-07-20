import os
from dotenv import load_dotenv

load_dotenv()


# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


# Modelle

CODE_MODEL = "gpt-5"
REVIEW_MODEL = "claude-sonnet-4"

ENABLE_CODE_REVIEW = True
ENABLE_TESTING = True