from builder.agents.base_agent import BaseAgent
from builder.utils.openai_client import OpenAIClient
from builder.utils.prompt_loader import PromptLoader


class TesterAgent(BaseAgent):

    def __init__(self):

        super().__init__("Tester")

        self.ai = OpenAIClient()

        self.prompts = PromptLoader()

    def execute(self, context):

        file = context.plan.files[-1]

        prompt = self.prompts.load(

            "tester",

            path=file["path"],

            code=file["content"]

        )

        result = self.ai.ask(prompt)

        context.current_task.review = result

        context.log(f"✔ Test {file['path']}")

        return context