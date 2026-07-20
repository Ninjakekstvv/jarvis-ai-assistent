from builder.agents.base_agent import BaseAgent
from builder.agents.agent_config import OPENAI_API_KEY, CODE_MODEL


class PlannerAgent(BaseAgent):

    def __init__(self):
        super().__init__("Planner")

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def execute(self, task: str):

        prompt = f"""
Du bist der Projektplaner von Jarvis.

Deine Aufgabe:

Zerlege die folgende Aufgabe in einzelne Schritte.

Antworte ausschließlich als nummerierte Liste.

Aufgabe:

{task}
"""

        response = self.client.responses.create(
            model=CODE_MODEL,
            input=prompt
        )

        return response.output_text