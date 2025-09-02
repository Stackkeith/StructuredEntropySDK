# AeonCore v2.0 - Main Execution
# This script is the ignition switch for the AeonCore v2.0 framework.
# It instantiates the Orchestrator and begins the simulation, putting the
# entire Quintet into motion.

from .orchestrator import Orchestrator

def run_aeon_simulation():
    """Initializes and runs the main AeonCore simulation."""
    print("--- Welcome to AeonCore v2.0 ---")

    # The Orchestrator is the conductor of our symphony.
    # It loads the configuration and directs the agents.
    conductor = Orchestrator()

    # This single call begins the entire process defined in our config.json.
    conductor.run_simulation()

    print("\n--- AeonCore v2.0 Run Concluded ---")

if __name__ == "__main__":
    run_aeon_simulation()
