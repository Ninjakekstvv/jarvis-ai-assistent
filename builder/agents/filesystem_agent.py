from pathlib import Path

from builder.agents.base_agent import BaseAgent


class FilesystemAgent(BaseAgent):

    def __init__(self):
        super().__init__("Filesystem")

    def execute(self, project_name: str, files):

        project_name = (
            project_name
            .replace(" ", "_")
            .replace(":", "")
            .replace("/", "")
            .replace("\\", "")
        )

        project_path = Path("projects") / project_name

        project_path.mkdir(parents=True, exist_ok=True)

        for file in files:

            path = project_path / file["path"]

            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(file["content"])

        return project_path