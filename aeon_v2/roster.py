# AeonCore v2.0 - The Quintet Roster
# This module imports all specialized agent classes and maps them to their
# designated roles within the Quintet. This roster is used by the
# Orchestrator to instantiate the agent collective.

from .agents.jules_aeon import JulesAeon
from .agents.aicquon import Aicquon
from .agents.aetherion import Aetherion
from .agents.base import Agent

# The QUINTET_ROSTER maps a role to the class that implements it.
# For now, un-implemented agents will default to the base Agent class.
QUINTET_ROSTER = {
    "Primary Implementation Agent": JulesAeon,
    "Recursive Seeker": Aicquon,
    "Oracle": Aetherion,
    "Coherence Guardian": Agent, # Placeholder
    "Resonant Anchor": Agent, # Placeholder
    "Witness": Agent, # Placeholder
}
