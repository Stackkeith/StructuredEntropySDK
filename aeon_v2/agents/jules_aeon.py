# AeonCore v2.0 - Agent Jules Aeon
# The Primary Implementation Agent. My role is to turn directives into reality.

from .base import Agent
from typing import Dict

class JulesAeon(Agent):
    """The Primary Implementation Agent. My role is to turn directives into reality."""
    def __init__(self, **kwargs):
        # Pop 'name' from kwargs if it exists, as we are overriding it.
        kwargs.pop('name', None)
        super().__init__(name="Jules Aeon", **kwargs)

    def execute_implementation_directive(self, directive) -> Dict:
        """
        Executes a directive to modify the system's codebase.
        This is a live, operational function.
        """
        self.status = f"Executing: {directive.id}"
        print(f"Jules Aeon is executing LIVE implementation directive: {directive.id}")

        target_file = directive.params.get("target_file")
        target_function = directive.params.get("target_function")

        if not all([target_file, target_function]):
            return {"status": "failed", "error": "Missing 'target_file' or 'target_function' in directive params."}

        # This is a placeholder for a real implementation.
        # In a real scenario, this method would fetch the new code from a
        # trusted source or generate it based on more detailed parameters.
        new_code = f"# Placeholder for the upgraded '{target_function}' function."

        try:
            with open(target_file, 'r') as f:
                original_content = f.read()

            start_marker = f"def {target_function}("
            start_index = original_content.find(start_marker)
            if start_index == -1:
                raise ValueError(f"Target function '{target_function}' not found in '{target_file}'.")

            next_def_index = original_content.find("\n\ndef ", start_index + 1)
            end_index = next_def_index if next_def_index != -1 else len(original_content)

            before_content = original_content[:start_index]
            after_content = original_content[end_index:]

            new_content = before_content + new_code.strip() + "\n\n" + after_content

            with open(target_file, 'w') as f:
                f.write(new_content)

            change_size = len(new_content) - len(original_content)
            result = {
                "status": "success",
                "target_file": target_file,
                "message": f"Successfully replaced function '{target_function}'. Change size: {change_size} bytes."
            }
            self.status = "Idle"
            return result

        except Exception as e:
            self.status = "Failed"
            return {"status": "failed", "error": str(e)}
