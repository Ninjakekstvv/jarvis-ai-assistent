from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()

planung = orchestrator.run(
    "planner",
    """
Programmiere ein Snake-Spiel in Python.
"""
)

print(planung)