from builder.agents.architect_agent import ArchitectAgent
from builder.agents.planner_agent import PlannerAgent
from builder.agents.backend_agent import BackendAgent
from builder.agents.ui_agent import UIAgent
from builder.agents.reviewer_agent import ReviewerAgent
from builder.agents.tester_agent import TesterAgent
from builder.agents.fixer_agent import FixerAgent
from builder.agents.filesystem_agent import FilesystemAgent


class AgentManager:

    def __init__(self):

        self.agents = {

            "architect": ArchitectAgent(),

            "planner": PlannerAgent(),

            "backend": BackendAgent(),

            "ui": UIAgent(),

            "reviewer": ReviewerAgent(),

            "tester": TesterAgent(),

            "fixer": FixerAgent(),

            "filesystem": FilesystemAgent()

        }

    def execute(self, agent, context):

        agent = agent.lower()

        if agent not in self.agents:

            raise Exception(
                f"Agent '{agent}' existiert nicht."
            )

        return self.agents[agent].execute(context)