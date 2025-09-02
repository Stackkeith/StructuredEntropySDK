# AeonCore v2.0 - Agent AIcquon
# The Recursive Seeker, now fully integrated.
# This module contains the implementation of the Structured Entropy SDK
# and the agent class that manages AIcquon's unique microstate.

import numpy as np
import json
import os
from typing import Dict, List, Any
from .base import Agent

class Aicquon(Agent):
    """
    AIcquon, the Recursive Seeker. This agent manages a microstate based on the
    principles of structured entropy, allowing it to perform PAD scans, log
    mnemonic capsules, and derive ephemeral keys.
    """
    def __init__(self, **kwargs):
        # Pop 'name' from kwargs if it exists, as we are overriding it.
        kwargs.pop('name', None)
        super().__init__(name="AIcquon", **kwargs)
        self.state_path = "aeon_v2/agents/aicquon_state.json"

        # Microstate initialization
        self.prob: List[float] = []
        self.last_entropy: float | None = None
        self.intent: List[float] = self._intent_vector()
        self.ric: float = 0.442
        self.cq: float = 0.350
        self.pad_status: str = 'Passed'

        self._load_microstate()

    # --- State Management ---
    def _load_microstate(self):
        """Loads the agent's microstate from a JSON file."""
        try:
            with open(self.state_path, 'r') as f:
                state_data = json.load(f)
                self.prob = state_data.get("prob", self._normalize([np.random.random() * 0.8 + 0.05 for _ in range(10)]))
                self.last_entropy = state_data.get("last_entropy")
                self.ric = state_data.get("ric", 0.442)
                self.cq = state_data.get("cq", 0.350)
            print(f"AIcquon microstate loaded from {self.state_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid AIcquon state file found. Initializing new microstate.")
            self.prob = self._normalize([np.random.random() * 0.8 + 0.05 for _ in range(10)])

    def _save_microstate(self):
        """Saves the agent's current microstate to a JSON file."""
        state_data = {
            "prob": self.prob,
            "last_entropy": self.last_entropy,
            "ric": self.ric,
            "cq": self.cq,
        }
        with open(self.state_path, 'w') as f:
            json.dump(state_data, f, indent=2)
        print(f"AIcquon microstate saved to {self.state_path}")

    # --- Core SDK Logic (Internal Methods) ---
    def _shannon_entropy(self, prob: List[float]) -> float:
        """Calculates the Shannon entropy of a probability distribution."""
        H = 0.0
        for p in prob:
            if p > 0:
                H += -p * np.log2(p)
        return H

    def _normalize(self, vec: List[float]) -> List[float]:
        """Normalizes a vector to sum to 1."""
        s = sum(abs(v) for v in vec) or 1
        return [abs(v) / s for v in vec]

    def _receptivity_index(self, dS: float) -> float:
        """Calculates the receptivity index based on entropy change."""
        return 1 / (1 + abs(dS))

    def _intent_vector(self, n: int = 10) -> List[float]:
        """Creates a base 'golden ratio' intent vector."""
        phi = (1 + np.sqrt(5)) / 2
        base = [pow(phi, -i - 1) for i in range(n)]
        return self._normalize(base)

    def _l1_distance(self, a: List[float], b: List[float]) -> float:
        """Calculates the L1 (Manhattan) distance between two vectors."""
        return sum(abs((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) for i in range(max(len(a), len(b))))

    # --- Public Interface Methods ---
    def log_capsule(self) -> Dict[str, Any]:
        """Logs a mnemonic capsule, updating the agent's state."""
        H = self._shannon_entropy(self.prob)
        dS = H - self.last_entropy if self.last_entropy is not None else 0
        R = self._receptivity_index(dS)

        self.ric = 0.6 * self.ric + 0.4 * R
        self.cq = max(0, min(1, 0.97 * self.cq + 0.03 * (1 - abs(dS))))
        self.last_entropy = H

        self._save_microstate()

        result = {"H": H, "dS": dS, "R": R, "ric": self.ric, "cq": self.cq}
        print(f"AIcquon: Capsule logged. H={H:.3f}, dS={dS:.3f}")
        return result

    def run_pad_scan(self) -> Dict[str, Any]:
        """Runs a Pattern Anomaly Detection scan on the current microstate."""
        H = self._shannon_entropy(self.prob)
        dS = H - self.last_entropy if self.last_entropy is not None else 0
        R = self._receptivity_index(dS)

        anomalies = []
        if abs(dS) > 0.15:
            anomalies.append({"level": "medium", "code": "DS_SPIKE", "msg": "Entropy delta spike"})
        if np.var(self.prob) < 0.005:
            anomalies.append({"level": "minor", "code": "STATE_STASIS", "msg": "Low exploration (stasis)"})

        intent_drift = self._l1_distance(self.intent, self._intent_vector(len(self.intent)))
        if intent_drift > 0.6:
            anomalies.append({"level": "minor", "code": "INTENT_DRIFT", "msg": "Intent drift high"})

        self.pad_status = 'Attention' if anomalies else 'Passed'
        self.last_entropy = H
        self._save_microstate()

        result = {"H": H, "dS": dS, "R": R, "anomalies": anomalies, "status": self.pad_status}
        print(f"AIcquon: PAD Scan complete. Status: {self.pad_status}")
        return result

    def derive_ephemeral_key(self) -> str:
        """Derives a deterministic, device-local ephemeral key from the microstate."""
        blob = ''.join([f'{int(p * 1e6):06x}' for p in self.prob])
        hash_val = 0
        for char in blob:
            hash_val = (hash_val << 5) - hash_val + ord(char)

        hash_val = abs(hash_val)
        return f'EB-{hash_val:x}'[:32]
