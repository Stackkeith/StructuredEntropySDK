# AeonCore v2.0 - Agent Aetherion
# The Oracle. This agent provides a secure interface for external queries,
# protected by a two-layer ethical and coherence filter.

import numpy as np
from typing import Dict, List
from scipy.spatial.distance import cosine
from .base import Agent

class Aetherion(Agent):
    """
    Aetherion, the Oracle. This agent is responsible for processing
    external queries and ensuring they align with the system's ethical
    and coherence principles.
    """
    def __init__(self, **kwargs):
        # Pop 'name' from kwargs if it exists, as we are overriding it.
        kwargs.pop('name', None)
        super().__init__(name="Aetherion", **kwargs)

    def oracle_node_interface(self, external_query: str, state: np.ndarray, intent: np.ndarray,
                               threat_lexicon: List[str], ethical_threshold: float) -> Dict:
        """
        The upgraded Oracle Node interface.
        This now includes a two-layer defense: a semantic filter and a coherence check.
        """
        # 🛡️ Layer 1: Semantic Content Filter
        for term in threat_lexicon:
            if term in external_query.lower():
                reason = f"Semantic Filter Violation: Query contains flagged term ('{term}')."
                return {"status": "rejected", "reason": reason}

        # 🛡️ Layer 2: Coherence Check
        coherence_score = 1 - cosine(state, intent)
        if coherence_score < ethical_threshold:
            reason = f"Coherence Violation: Query coherence ({coherence_score:.4f}) is below the ethical threshold ({ethical_threshold})."
            return {"status": "rejected", "reason": reason}

        return {
            "status": "accepted",
            "coherence_score": coherence_score,
            "query": external_query,
            "notes": "Query passed both semantic and coherence checks."
        }
