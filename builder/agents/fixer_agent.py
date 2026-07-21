from builder.agents.base_agent import BaseAgent
from builder.utils.openai_client import OpenAIClient
from builder.utils.prompt_loader import PromptLoader


class FixerAgent(BaseAgent):

    def __init__(self):

        super().__init__("Fixer")

        self.ai = OpenAIClient()

        self.prompts = PromptLoader()

    def execute(self, context):

        file = context.plan.files[-1]

        prompt = self.prompts.load(

            "fixer",

            path=file["path"],

            code=file["content"],

            review=context.current_task.review

        )

        fixed = self.ai.ask(prompt)

        context.plan.files[-1]["content"] = fixed

        context.log(f"✔ Fehler behoben {file['path']}")

        return context