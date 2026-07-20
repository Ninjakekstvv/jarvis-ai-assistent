from typing import Dict
from typing import Dict

from agents.codex_agent import CodexAgent
from agents.codex_agent import CodexAgent
from agents.planner_agent import PlannerAgent

class Orchestrator:

    def __init__(self):
        self.agents: Dict[str, object] = {}

    def register(self, name, agent):
        self.agents[name] = agent

    def run(self, agent_name, task):

        if agent_name not in self.agents:
            raise Exception(f"Agent '{agent_name}' existiert nicht.")

        return self.agents[agent_name].execute(task)

        class Orchestrator:

    def __init__(self):

        self.agents: Dict[str, object] = {}

        self.register(
            "codex",
            CodexAgent()
        )

    def register(self, name, agent):

        self.agents[name] = agent

    def run(self, agent_name, task):

        if agent_name not in self.agents:
            raise Exception(f"Agent '{agent_name}' existiert nicht.")

        return self.agents[agent_name].execute(task)

        from typing import Dict

class Orchestrator:

    def __init__(self):

        self.agents: Dict[str, object] = {}

        self.register(
            "planner",
            PlannerAgent()
        )

        self.register(
            "codex",
            CodexAgent()
        )

    def register(self, name, agent):
        self.agents[name] = agent

    def run(self, agent_name, task):

        if agent_name not in self.agents:
            raise Exception(f"Agent '{agent_name}' existiert nicht.")

        return self.agents[agent_name].execute(task)