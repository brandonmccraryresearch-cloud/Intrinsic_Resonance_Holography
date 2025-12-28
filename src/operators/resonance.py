"""
Operator Layer: Adaptive Resonance Optimization

THEORETICAL FOUNDATION: IRH v22.2 Manuscript Part 1 §4.1

This module implements the core solver for the Cymatic Universe:
Adaptive Resonance Optimization (ARO).

Key Concepts:
- **ARO**: Replaces Stochastic Gradient Descent. Minimizes Dissonance Functional.
- **Dissonance Functional**: Measure of phase decoherence.

Authors: Brandon D. McCrary
Last Updated: December 2025
"""

import numpy as np
from src.substrate.manifold import CymaticResonanceNetwork

__version__ = "22.2.0"
__theoretical_foundation__ = "IRH v22.2 Manuscript Part 1 §4.1"


class AdaptiveResonanceOptimization:
    """
    Solver that evolves the CRN towards a phase-locked state.
    """

    def __init__(self, network: CymaticResonanceNetwork, learning_rate: float = 0.01):
        self.network = network
        self.learning_rate = learning_rate

    def dissonance_functional(self) -> float:
        """
        Compute the global Dissonance \Gamma.

        \Gamma = \sum_{<i,j>} (1 - \cos(\phi_j - \phi_i))

        Zero dissonance = perfect phase locking.
        """
        dissonance = 0.0
        for i, j in self.network.graph.edges():
            phi_i = self.network.nodes[i].phase
            phi_j = self.network.nodes[j].phase
            dissonance += (1.0 - np.cos(phi_j - phi_i))
        return dissonance

    def optimize_step(self) -> float:
        """
        Perform one optimization step adjusting frequencies to minimize dissonance.

        Returns:
            float: Current dissonance value.
        """
        # This is a meta-optimization on top of the physical dynamics.
        # It represents the "tuning" of the universe's constants (frequencies).

        current_dissonance = self.dissonance_functional()

        # Gradient descent on dissonance with respect to node phases
        # d\Gamma / d\phi_i = \sum_{j \in N(i)} \sin(\phi_j - \phi_i)

        phase_updates = {}
        for i in self.network.nodes:
            grad = 0.0
            phi_i = self.network.nodes[i].phase
            for neighbor in self.network.graph.neighbors(i):
                phi_j = self.network.nodes[neighbor].phase
                grad += np.sin(phi_j - phi_i) # This matches the coupling force!

            # Update phase to reduce dissonance
            # In physical time, this is the coupling force.
            # In "optimization time", we can step directly.
            phase_updates[i] = self.learning_rate * grad

        for i, delta in phase_updates.items():
            self.network.nodes[i].phase += delta

        return current_dissonance

    def run_until_convergence(self, tolerance: float = 1e-6, max_steps: int = 1000) -> bool:
        """
        Run optimization until dissonance minimizes.
        """
        for _ in range(max_steps):
            d = self.optimize_step()
            if d < tolerance:
                return True
        return False
