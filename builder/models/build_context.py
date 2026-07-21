from dataclasses import dataclass

from builder.models.build_plan import BuildPlan


@dataclass
class BuildContext:

    prompt: str

    plan: BuildPlan | None = None

    current_task = None

    project_path = None

    def log(self, message):

        print(message)