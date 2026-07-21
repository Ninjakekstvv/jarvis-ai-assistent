import json

from builder.agents.base_agent import BaseAgent
from builder.utils.openai_client import OpenAIClient
from builder.utils.prompt_loader import PromptLoader


class UIAgent(BaseAgent):

    def __init__(self):

        super().__init__("UI")

        self.ai = OpenAIClient()

        self.prompts = PromptLoader()

    def execute(self, context):

        task = context.current_task

        file = task.files[0]

        prompt = self.prompts.load(

            "ui",

            project=json.dumps(
                context.plan.project,
                indent=4,
                ensure_ascii=False
            ),

            tech=json.dumps(
                context.plan.tech,
                indent=4,
                ensure_ascii=False
            ),

            path=file.path,

            description=file.description

        )

        code = self.ai.ask(prompt)

        file.complete(code)

        context.plan.files.append({

            "path": file.path,

            "content": code

        })

        context.log(f"✔ {file.path}")

        return context