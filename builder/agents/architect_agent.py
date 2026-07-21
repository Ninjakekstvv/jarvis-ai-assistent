import json

from builder.agents.base_agent import BaseAgent
from builder.utils.openai_client import OpenAIClient
from builder.utils.prompt_loader import PromptLoader
from builder.models.build_plan import BuildPlan


class ArchitectAgent(BaseAgent):

    def __init__(self):

        super().__init__("Architect")

        self.ai = OpenAIClient()

        self.prompts = PromptLoader()

    def execute(self, context):

        prompt = self.prompts.load(

            "architect",

            task=context.prompt

        )

        result = self.ai.ask_json(prompt)

        plan = BuildPlan()

        plan.project = result["project"]

        plan.tech = result["tech"]

        context.plan = plan

        context.log("✔ Projekt analysiert.")

        return context