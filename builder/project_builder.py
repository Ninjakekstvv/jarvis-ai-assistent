from builder.models.build_context import BuildContext

from builder.agents.architect_agent import ArchitectAgent
from builder.agents.planner_agent import PlannerAgent

from builder.agents.backend_agent import BackendAgent
from builder.agents.ui_agent import UIAgent

from builder.agents.reviewer_agent import ReviewerAgent
from builder.agents.tester_agent import TesterAgent
from builder.agents.fixer_agent import FixerAgent

from builder.agents.filesystem_agent import FilesystemAgent


class ProjectBuilder:

    def __init__(self):

        self.architect = ArchitectAgent()
        self.planner = PlannerAgent()

        self.backend = BackendAgent()
        self.ui = UIAgent()

        self.reviewer = ReviewerAgent()
        self.tester = TesterAgent()
        self.fixer = FixerAgent()

        self.filesystem = FilesystemAgent()

    def build(self, prompt: str):

        print("=" * 60)
        print("JARVIS BUILDER")
        print("=" * 60)

        context = BuildContext(prompt)

        print("\n========== ARCHITECT ==========")

        self.architect.execute(context)

        print("Projekt:")
        print(context.plan.project)

        print("\nTech:")
        print(context.plan.tech)

        print("\n========== PLANNER ==========")

        self.planner.execute(context)

        print(f"Aufgaben: {len(context.plan.tasks)}")

        for task in context.plan.tasks:
            print(f"- {task.title} ({task.agent})")

        for task in context.plan.tasks:

            context.current_task = task

            print(f"\n========== {task.title} ==========")

            if task.agent == "backend":

                self.backend.execute(context)

            elif task.agent == "ui":

                self.ui.execute(context)

            else:

                raise Exception(
                    f"Unbekannter Agent: {task.agent}"
                )

            print("Review...")

            self.reviewer.execute(context)

            print(context.current_task.review)

            print("Tester...")

            self.tester.execute(context)

            print(context.current_task.review)

            if context.current_task.review != "OK":

                print("Fixer...")

                self.fixer.execute(context)

                self.tester.execute(context)

        print("\n========== FILESYSTEM ==========")

        self.filesystem.execute(context)

        print("\nProjekt erfolgreich abgeschlossen.")

        return context