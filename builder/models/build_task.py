from dataclasses import dataclass, field

from builder.models.file_task import FileTask


@dataclass
class BuildTask:

    title: str

    description: str

    agent: str

    priority: int = 0

    status: str = "pending"

    files: list[FileTask] = field(default_factory=list)

    review: str | None = None

    retry_count: int = 0

    max_retries: int = 3

    def add_file(
        self,
        path: str,
        description: str
    ):

        self.files.append(
            FileTask(
                path,
                description
            )
        )