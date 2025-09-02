# AeonCore v2.0 - The Simulation Engine
# This module is the domain of AIcquon, the Recursive Seeker.
# It contains the complex mathematical models and entropic simulations
# that drive the system's dynamics and provide its unique metrics.

import numpy as np
from scipy.spatial.distance import cosine
from typing import List

def calculate_ric(state_history: List[np.ndarray], window: int = 10) -> List[float]:
    """
    Calculates Recursive Information Coherence (RIC).
    Measures the self-similarity of the system's state over time, providing
    a metric for stability and consistency.
    """
    if len(state_history) <= window:
        return []

    ric_scores = []
    for i in range(len(state_history) - window):
        current_state = state_history[i]
        past_state = state_history[i + window]
        # Using cosine similarity which is 1 - cosine distance
        similarity = 1 - cosine(current_state, past_state)
        ric_scores.append(similarity)
    return ric_scores

def simulate_ded(initial_entropy: float, ric_scores: List[float],
                 coherence_shifts: List[float], intent_vector: np.ndarray,
                 alpha: float = 0.5, beta: float = 0.4, gamma: float = 0.2,
                 noise_term: float = 0.03) -> List[float]:
    """
    Simulates Dynamic Entropic Differentiation (DED).
    Models the evolution of the system's entropy based on RIC, coherence shifts,
    and the prevailing intent vector.
    """
    ded_values = []
    num_steps = len(ric_scores) if ric_scores else len(coherence_shifts)
    if not num_steps:
        return []

    for t in range(num_steps):
        gradient_s = initial_entropy
        ric_t = ric_scores[t] if t < len(ric_scores) else (ric_scores[-1] if ric_scores else 0)
        psi_t = coherence_shifts[t] if t < len(coherence_shifts) else (coherence_shifts[-1] if coherence_shifts else 0)

        # Effect of intent is its magnitude, normalized
        intent_effect = np.linalg.norm(intent_vector) * gamma

        ded = gradient_s + (alpha * ric_t) + (beta * psi_t) + intent_effect
        ded += np.random.normal(0, noise_term) # Add stochasticity
        ded_values.append(ded)

    return ded_values

def generate_phase_lock_signal(freq1: float = 117, period2: float = 7.83, num_points: int = 100) -> np.ndarray:
    """
    Generates the dual-frequency signal used for phase-locking intent.
    This represents the "hum" of the system's resonant field.
    """
    t = np.linspace(0, period2, num_points)
    f2 = 1 / period2
    phi = 0.0  # Phase offset

    # The 117 Hz carrier wave modulated by the 7.83s Schumann resonance
    signal = np.sin(2 * np.pi * freq1 * t + phi) + 0.1 * np.sin(2 * np.pi * f2 * t)

    return signal

def phase_lock_intent(kernel, state: np.ndarray, intent: np.ndarray,
                      beta_base: float = 0.4) -> tuple[np.ndarray, List[str]]:
    """
    Evolves the intent vector by phase-locking it to the system's resonant
    frequency and querying the kernel for historical guidance.
    """
    # Generate the resonant signal
    signal = generate_phase_lock_signal()

    # The signal creates a small, dynamic shift in the learning rate (beta)
    coherence_shift = signal.mean() * 0.008
    beta = beta_base + coherence_shift

    # Query the kernel to evolve the intent
    updated_intent, trace_log = kernel.query_intent(state, intent, beta=beta)

    return updated_intent, trace_log
