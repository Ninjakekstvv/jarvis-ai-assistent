import json

from openai import OpenAI

from builder.agents.base_agent import BaseAgent
from builder.agents.agent_config import OPENAI_API_KEY, CODE_MODEL


class CodexAgent(BaseAgent):

    def __init__(self):
        super().__init__("Codex")

        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def execute(self, task: str):

        prompt = f"""
Du bist ein professioneller Softwareentwickler.

Erstelle das Projekt.

Antworte ausschließlich als JSON.

Format:

{{
    "project_name": "...",

    "files":[

        {{
            "path":"main.py",
            "content":"..."
        }}

    ]
}}

Keine Erklärungen.

Aufgabe:

{task}
"""

        response = self.client.responses.create(
            model=CODE_MODEL,
            input=prompt
        )

        text = response.output_text

        return json.loads(text)