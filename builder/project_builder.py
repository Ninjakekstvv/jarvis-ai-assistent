from builder.agents.manager import AgentManager


class ProjectBuilder:

    def __init__(self):

        self.manager = AgentManager()

    def build(self, task: str):

        print(f"Projekt wird erstellt: {task}")

        return self.manager.build(task)