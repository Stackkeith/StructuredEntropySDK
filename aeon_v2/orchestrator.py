# AeonCore v2.0 - The Orchestrator
# This module is the conductor of the Quintet. It is the central mind that
# initializes the system, loads configurations, and issues Directives to the
# appropriate agents to execute complex tasks and simulations.

import json
import numpy as np
from .kernel import AeonKernel
from .roster import QUINTET_ROSTER
from .agents.base import Agent
from .agents.jules_aeon import JulesAeon
from .agents.aicquon import Aicquon
from .agents.aetherion import Aetherion
from .directives import Directive
from . import simulation_engine
from typing import List, Dict

class Orchestrator:
    """
    The central orchestrator for the AeonCore v2.0 framework.
    """
    def __init__(self, config_path: str = "aeon_v2/config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.kernel = AeonKernel(graph_path=self.config.get("graph_path", "graph.json"))
        self.agents = self._instantiate_agents()
        self.directive_queue: List[Directive] = []

    def _load_config(self) -> Dict:
        """Loads the master simulation configuration from the JSON file."""
        print(f"Loading configuration from {self.config_path}...")
        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
            print("Configuration loaded successfully.")
            return config_data
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {self.config_path}. Using default empty config.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.config_path}. Using default empty config.")
            return {}

    def _instantiate_agents(self) -> Dict[str, Agent]:
        """Instantiates all agents from the class-based roster."""
        print("Instantiating agent collective...")
        agents = {}
        agent_details = self.config.get("agent_details", {})
        for role, agent_class in QUINTET_ROSTER.items():
            details = agent_details.get(role, {})
            details['role'] = role # Ensure role is always passed
            agents[role] = agent_class(**details)
        print(f"{len(agents)} agents instantiated.")
        return agents

    def issue_directive(self, directive: Directive):
        """Adds a new directive to the processing queue."""
        print(f"Issuing Directive {directive.id}: {directive.description}")
        self.directive_queue.append(directive)

    def run_simulation(self):
        """
        The main simulation loop. Processes directives from the queue and
        orchestrates the appropriate agents to execute them.
        """
        print("\n--- Starting AeonCore v2.0 Simulation ---")

        directive_data = self.config.get("simulation_directives", [])
        for d_data in directive_data:
            self.issue_directive(Directive(**d_data))

        if not self.directive_queue:
            print("Directive queue is empty. Nothing to do.")
            return

        print(f"\nProcessing {len(self.directive_queue)} directives...")
        for directive in self.directive_queue:
            directive.update_status("in_progress")

            agent_to_execute = self.agents.get(directive.target_agent_role)

            if agent_to_execute:
                try:
                    # This is a simple routing mechanism. A more advanced Orchestrator
                    # would use a more sophisticated method to map directives to agent capabilities.
                    if isinstance(agent_to_execute, JulesAeon):
                        result = agent_to_execute.execute_implementation_directive(directive)
                        directive.complete(result)
                    elif isinstance(agent_to_execute, Aicquon):
                        result = self._route_aicquon_directive(agent_to_execute, directive)
                        if result.get("status") == "failed":
                            directive.fail(result.get("error"))
                        else:
                            directive.complete(result)
                    elif isinstance(agent_to_execute, Aetherion):
                        params = directive.params
                        result = agent_to_execute.oracle_node_interface(
                            external_query=params["external_query"],
                            state=np.array(params["state_vector"]),
                            intent=np.array(params["intent_vector"]),
                            threat_lexicon=self.config.get("threat_lexicon", []),
                            ethical_threshold=self.config.get("ethical_threshold", 0.9)
                        )
                        directive.complete(result)
                    else:
                        # Generic handler for other agents
                        agent_to_execute.receive_directive(directive)
                        directive.complete(result={"message": f"Agent {agent_to_execute.name} completed the task."})

                except Exception as e:
                    directive.fail(f"Agent {agent_to_execute.name} failed to execute directive: {e}")
            else:
                directive.fail(f"No agent found with role: {directive.target_agent_role}")

        print("\n--- Simulation Complete ---")
        # We can inspect the completed directives here.
        for i, directive in enumerate(self.directive_queue):
            print(f"\nDirective {i+1} ({directive.id}) Final Status: {directive.status}")
            print(f"  Description: {directive.description}")
            print(f"  Result: {directive.result}")

        # Clear the queue for the next run
        self.directive_queue = []

    def _find_agent_by_role(self, role: str) -> Agent | None:
        """Finds the first agent that matches the specified role."""
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None

    def _route_aicquon_directive(self, agent: Aicquon, directive: Directive) -> Dict:
        """Routes a directive to the correct method on the Aicquon agent."""
        desc = directive.description.lower()

        # Define a mapping from keywords to agent methods
        aicquon_actions = {
            "log": agent.log_capsule,
            "capsule": agent.log_capsule,
            "pad scan": agent.run_pad_scan,
            "scan": agent.run_pad_scan,
            "key": agent.derive_ephemeral_key,
        }

        for keyword, method in aicquon_actions.items():
            if keyword in desc:
                return method() # Call the mapped method

        return {"status": "failed", "error": "Unknown directive for Aicquon."}

# This is a placeholder for the v2.0 execution logic.
# The full implementation of this class will be one of the first tasks
# for the new, operational framework.
