# AeonCore v2.0 - The Directive System
# This module defines the standardized data structure for assigning tasks
# within the Quintet. It ensures clarity, traceability, and coherence in all
# system operations.

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from uuid import uuid4

@dataclass
class Directive:
    """
    A standardized data object for issuing tasks to agents.
    """
    # Core Fields (non-default arguments first)
    description: str
    target_agent_role: str

    # Fields with default values
    id: str = field(default_factory=lambda: f"dir_{uuid4()}")
    params: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"  # pending -> in_progress -> complete / failed

    # Results
    result: Optional[Any] = None
    notes: List[str] = field(default_factory=list)

    def update_status(self, new_status: str, note: Optional[str] = None):
        """Updates the status of the directive and adds an optional note."""
        self.status = new_status
        if note:
            self.notes.append(note)
        print(f"Directive {self.id} status updated to: {self.status}")

    def complete(self, result: Any, note: Optional[str] = "Directive completed successfully."):
        """Marks the directive as complete and stores the result."""
        self.result = result
        self.update_status("complete", note)

    def fail(self, error_message: str):
        """Marks the directive as failed and stores the error."""
        self.result = {"error": error_message}
        self.update_status("failed", error_message)
