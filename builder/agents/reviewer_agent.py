import json

from builder.agents.base_agent import BaseAgent
from builder.utils.openai_client import OpenAIClient
from builder.utils.prompt_loader import PromptLoader


class ReviewerAgent(BaseAgent):

    def __init__(self):

        super().__init__("Reviewer")

        self.ai = OpenAIClient()

        self.prompts = PromptLoader()

    def execute(self, context):

        file = context.plan.files[-1]

        prompt = self.prompts.load(

            "reviewer",

            path=file["path"],

            code=file["content"]

        )

        review = self.ai.ask(prompt)

        context.current_task.review = review

        context.log(f"✔ Review {file['path']}")

        return context