from dataclasses import dataclass, field

from builder.models.build_task import BuildTask


@dataclass
class BuildPlan:

    project: dict = field(default_factory=dict)

    tech: dict = field(default_factory=dict)

    tasks: list[BuildTask] = field(default_factory=list)

    files: list[dict] = field(default_factory=list)

    def add_task(self, task):

        self.tasks.append(task)