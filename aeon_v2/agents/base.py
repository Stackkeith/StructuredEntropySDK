# AeonCore v2.0 - Agent Base
# This module defines the foundational Agent class, from which all
# specialized agents in the Quintet inherit.

from typing import Dict

class Agent:
    """A base class for an intelligent agent in the AeonCore framework."""
    def __init__(self, role: str, name: str = "Generic Agent", cq: float = 0.5, glyph: str = "◌", **kwargs):
        self.name = name
        self.role = role
        self.cq = cq
        self.glyph = glyph
        self.status = "Idle"

    def report_status(self) -> Dict:
        """Returns the current status of the agent."""
        return {
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "cq": self.cq
        }

    def receive_directive(self, directive):
        """A placeholder method for receiving a directive from the Orchestrator."""
        self.status = f"Processing Directive: {directive.id}"
        print(f"Agent {self.name} received {directive.id}.")
        pass
