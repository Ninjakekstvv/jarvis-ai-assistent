from pathlib import Path

from builder.agents.base_agent import BaseAgent


class FilesystemAgent(BaseAgent):

    def __init__(self):

        super().__init__("Filesystem")

    def execute(self, context):

        project_name = context.plan.project["name"]

        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        root.mkdir(
            parents=True,
            exist_ok=True
        )

        for file in context.plan.files:

            target = root / file["path"]

            target.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            target.write_text(
                file["content"],
                encoding="utf-8"
            )

            print("Gespeichert:", target)

        context.project_path = root

        return context