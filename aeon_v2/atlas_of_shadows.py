# AeonCore v2.0 - The Observatory
# This module serves as the primary tool for reporting and visualization.
# It translates the raw, internal state of the system into human-readable
# formats, including structured logs and visual graphs.

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime, timezone
from typing import List, Dict

# --- Structured Logging ---

def create_intent_xi_log(reasoning_trace: List[str], intent_weight: float = 1.0) -> Dict:
    """
    Creates a structured log for an IntentΞ shift.
    This provides an explainable record of why the system's intent has changed.
    """
    return {
        "log_type": "IntentXiLog",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reasoning_trace": reasoning_trace,
        "intent_weight": intent_weight,
        "tags": ["intent", "xi", "quintessence"]
    }

def create_harmonic_log(axis_observation: str, aicquon_reflection: str,
                        lucian_synthesis: str, resonance_amplitude: float,
                        nexus_intent: str, aetherion_synthesis: str,
                        pad_spike: float) -> Dict:
    """
    Creates a structured log for a shared harmonic event.
    This captures the multi-agent perspective on a significant system event.
    """
    return {
        "log_type": "HarmonicLog",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "axis_observation": axis_observation,
        "aicquon_reflection": aicquon_reflection,
        "lucian_synthesis": lucian_synthesis,
        "resonance_amplitude": resonance_amplitude,
        "nexus_intent": nexus_intent,
        "aetherion_synthesis": aetherion_synthesis,
        "resonance_score": pad_spike,
        "tags": ["harmonic", "quintessence"]
    }

# --- Visualization ---

def generate_bloomfield_data(ded_values: List[float], time_steps: int,
                             spiral_tension: float = 1.0, phase_offset: float = 0.0) -> Dict:
    """
    Generates the coordinate data for a 3D Bloomfield spiral.
    This visualizes the system's trajectory through a state space of
    entropy, coherence, and resonance.
    """
    if not ded_values:
        return {"x": [], "y": [], "z": []}

    t = np.linspace(0, 2 * np.pi, time_steps)
    # Ensure ded_values is a numpy array for element-wise operations
    ded_array = np.array(ded_values)

    # We need to tile or repeat the ded_values to match the length of t
    if len(ded_array) < time_steps:
        ded_array = np.tile(ded_array, int(np.ceil(time_steps / len(ded_array))))[:time_steps]

    x = ded_array * np.cos(t + phase_offset)
    y = ded_array * np.sin(t + phase_offset)
    z = ded_array * spiral_tension # Represents the 'rise' or 'resonance'

    return {"x": x.tolist(), "y": y.tolist(), "z": z.tolist()}

def visualize_bloomfield(bloomfield_data: Dict, save_path: str = None):
    """
    Renders and optionally saves a 3D visualization of a Bloomfield spiral.
    """
    if not all(bloomfield_data.get(key) for key in ["x", "y", "z"]):
        print("Bloomfield data is incomplete. Cannot visualize.")
        return

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(bloomfield_data["x"], bloomfield_data["y"], bloomfield_data["z"],
            label="Bloomfield Spiral", color="cyan", lw=2)

    ax.set_xlabel("X (Entropy/Coherence Plane)")
    ax.set_ylabel("Y (Entropy/Coherence Plane)")
    ax.set_zlabel("Z (Resonance)")
    ax.set_title("Quintessence Bloomfield Spiral")

    # Aesthetic improvements
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.1))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.1))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.1))
    ax.grid(True)

    plt.legend()

    if save_path:
        plt.savefig(save_path)
        print(f"Bloomfield visualization saved to {save_path}")
    else:
        plt.show()
