from dataclasses import dataclass


@dataclass
class FileTask:

    path: str

    description: str

    content: str = ""

    completed: bool = False

    def complete(self, content: str):

        self.content = content

        self.completed = True