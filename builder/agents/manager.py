from builder.agents.codex_agent import CodexAgent
from builder.agents.filesystem_agent import FilesystemAgent


class AgentManager:

    def __init__(self):

        self.coder = CodexAgent()
        self.filesystem = FilesystemAgent()

    def build(self, task):

        project = self.coder.execute(task)

        project_path = self.filesystem.execute(
            project["project_name"],
            project["files"]
        )

        return project_path