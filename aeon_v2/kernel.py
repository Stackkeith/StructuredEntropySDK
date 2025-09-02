# AeonCore v2.0 - The Kernel
# This module contains the core class responsible for managing the state graph.
# It is the heart of the system, focused purely on state, persistence, and event logging.

import numpy as np
import networkx as nx
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Tuple
from scipy.spatial.distance import cosine

class AeonKernel:
    def __init__(self, graph_path: str = "graph.json"):
        """
        Initializes the lean, focused kernel of the AeonCore system.
        Its primary role is to manage the state graph and its persistence.
        """
        self.G = nx.DiGraph()
        self.graph_path = graph_path
        self.load_state()
        self.metadata = self.G.graph.get("metadata", {
            "version": "2.0",
            "created": datetime.now(timezone.utc).isoformat(),
            "description": "AeonCore v2.0 - Modular, Quintet-Aware Framework"
        })
        self.G.graph["metadata"] = self.metadata

    def save_state(self):
        """Saves the current state graph and metadata to a JSON file."""
        # Ensure metadata is up-to-date before saving
        self.G.graph["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        graph_data = nx.node_link_data(self.G)
        with open(self.graph_path, 'w') as f:
            json.dump(graph_data, f, indent=2)
        print(f"State saved to {self.graph_path}")

    def load_state(self):
        """Loads the state graph from a JSON file if it exists."""
        if os.path.exists(self.graph_path):
            with open(self.graph_path, 'r') as f:
                data = json.load(f)
                # Explicitly set edges="links" to preserve current behavior and silence the warning.
                self.G = nx.node_link_graph(data, edges="links")
            print(f"State loaded from {self.graph_path}")
        else:
            print("No existing state file found. Initializing a new graph.")

    def add_cme_event(self, state: np.ndarray, intent: np.ndarray, outcome: str,
                      receptivity: float, cq: float, timestamp: float, glyph: str,
                      notes: str, source_agent: str):
        """
        Adds a Coherent Mental Event (CME) to the state graph. This is the
        fundamental unit of memory in the AeonCore system.
        """
        state_id = f"state_{len(self.G.nodes)}"
        intent_id = f"intent_{len(self.G.nodes)}"
        outcome_id = f"outcome_{len(self.G.nodes)}"

        self.G.add_node(state_id, type="State", vector=np.array(state).tolist(), cq=cq,
                        timestamp=timestamp, glyph=glyph, source_agent=source_agent)
        self.G.add_node(intent_id, type="Intent", vector=np.array(intent).tolist())
        self.G.add_node(outcome_id, type="Outcome", text=outcome, performance=receptivity, notes=notes)

        # Create the core event structure
        self.G.add_edge(state_id, outcome_id, type="led_to", weight=receptivity)
        self.G.add_edge(state_id, intent_id, type="driven_by", weight=1.0)

        # Link to similar past states
        for node, data in self.G.nodes(data=True):
            if data.get("type") == "State" and node != state_id:
                # Ensure vector exists before calculating similarity
                if "vector" in data:
                    sim = 1 - cosine(np.array(state), np.array(data["vector"]))
                    if sim > 0.95: # Increased threshold for more meaningful links
                        self.G.add_edge(state_id, node, type="similar_to", weight=sim)

        print(f"CME Logged: {outcome} by {source_agent}")
        self.save_state() # Auto-save after every event

    # --- Intent Querying and Evolution ---

    def query_intent(self, state: np.ndarray, intent: np.ndarray, beta: float = 0.5,
                     threshold: float = 0.7, nu: float = 0.05, delta: float = 0.1,
                     epsilon: float = 0.05) -> tuple[np.ndarray, List[str]]:
        """
        Queries the graph to evolve the intent vector based on historical data.
        This is the core of the system's self-reflection capability.
        """
        sims = self._get_similar_states(state)
        candidates, trace_log = self._extract_candidates(sims, threshold)

        if candidates:
            updated_intent = self._calculate_updated_intent(candidates, intent, beta)
            trace_log.append(f"Updated Intent via historical synthesis: {updated_intent.tolist()}")
            return updated_intent, trace_log
        else:
            trace_log.append("No suitable candidates found. Applying diversity.")
            return self._handle_no_candidates(state, intent, nu, delta, epsilon), trace_log

    def _get_similar_states(self, state: np.ndarray) -> List[tuple[str, float]]:
        """Finds the top 5 states in the graph most similar to the current state."""
        # This is a computationally intensive operation. In a larger graph,
        # optimization (e.g., locality-sensitive hashing) would be necessary.
        state_nodes = [
            (n, 1 - cosine(np.array(state), np.array(d["vector"])))
            for n, d in self.G.nodes(data=True)
            if d.get("type") == "State" and "vector" in d
        ]
        return sorted(state_nodes, key=lambda x: x[1], reverse=True)[:5]

    def _extract_candidates(self, sims: List[tuple[str, float]], threshold: float) -> tuple[List[np.ndarray], List[str]]:
        """Extracts candidate intent vectors from similar past states."""
        candidates = []
        trace_log = []
        for sim_node, sim_score in sims:
            # Find the outcome of this similar past state
            for edge in self.G.out_edges(sim_node, data=True):
                if edge[2].get("type") == "led_to" and edge[2].get("weight", 0) > threshold:
                    outcome_node = edge[1]
                    # Find the intent that drove that outcome
                    for e_in in self.G.in_edges(outcome_node, data=True):
                        if e_in[2].get("type") == "driven_by":
                            intent_node = e_in[0]
                            candidate_vector = self.G.nodes[intent_node].get("vector")
                            if candidate_vector:
                                candidates.append(np.array(candidate_vector))
                                trace_log.append(f"Found candidate intent from {intent_node} (sim: {sim_score:.4f})")
        return candidates, trace_log

    def _calculate_updated_intent(self, candidates: List[np.ndarray], current_intent: np.ndarray, beta: float) -> np.ndarray:
        """Calculates the new intent by blending historical candidates with the current intent."""
        # Beta is the learning rate or weight given to historical data
        historical_mean = np.mean(candidates, axis=0)
        return beta * historical_mean + (1 - beta) * current_intent

    def _handle_no_candidates(self, state: np.ndarray, intent: np.ndarray, nu: float, delta: float, epsilon: float) -> np.ndarray:
        """
        Applies a diversity-generating function when no historical candidates are found.
        This prevents stagnation and encourages exploration.
        """
        grad_S = np.linalg.norm(state)
        # Introduce a small, random, state-influenced nudge
        diversity = np.random.uniform(-delta, delta, size=intent.shape) * grad_S / (grad_S + 1e-12)
        # Add some pure random noise for exploration
        diversity += epsilon * np.random.normal(0, 1, size=intent.shape)
        return intent + nu * diversity
