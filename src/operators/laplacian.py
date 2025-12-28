"""
Operator Layer: Laplacian and Symplectic Guard

THEORETICAL FOUNDATION: IRH v22.2 Manuscript Part 1 §3.1

This module implements the Interference Matrix (Graph Laplacian) and the
Symplectic Guard mechanism which enforces destructive interference for non-planar diagrams.

Key Concepts:
- **InterferenceMatrix**: The operator describing wave propagation on the CRN.
- **SymplecticGuard**: A filter ensuring One-Loop Exactness.

Authors: Brandon D. McCrary
Last Updated: December 2025
"""

import numpy as np
import networkx as nx
from typing import Callable, Any, Tuple

__version__ = "22.2.0"
__theoretical_foundation__ = "IRH v22.2 Manuscript Part 1 §3.1"


class InterferenceMatrix:
    """
    The discrete Laplacian operator on the Cymatic Resonance Network.

    L = D - A
    where D is the Degree Matrix and A is the Adjacency Matrix.

    In the continuum limit, this becomes the Laplace-Beltrami operator.
    """

    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.laplacian = nx.laplacian_matrix(graph).toarray()

    def apply(self, field_vector: np.ndarray) -> np.ndarray:
        """
        Apply the Laplacian to a field vector (state of the network).

        Args:
            field_vector (np.ndarray): Vector of node phases/amplitudes.

        Returns:
            np.ndarray: Result of L * psi.
        """
        return self.laplacian @ field_vector

    def get_spectrum(self) -> np.ndarray:
        """
        Compute eigenvalues of the Laplacian (Resonant Frequencies).

        Returns:
            np.ndarray: Sorted eigenvalues.
        """
        eigenvalues = np.linalg.eigvalsh(self.laplacian)
        return np.sort(eigenvalues)


class SymplecticGuard:
    """
    Enforces the Symplectic Cancellation Theorem (Theorem 3.1).

    Mechanism:
    Checks the genus of the interaction diagram. If genus > 0 (non-planar),
    the amplitude is nullified due to destructive quaternionic phase interference.
    """

    @staticmethod
    def filter_amplitude(amplitude: float, genus: int) -> float:
        """
        Apply the Symplectic Guard to a Feynman diagram amplitude.

        Args:
            amplitude (float): Calculated amplitude.
            genus (int): Genus of the diagram (0 = planar/one-loop, >0 = higher-loop).

        Returns:
            float: Filtered amplitude.
        """
        if genus == 0:
            # Planar / One-Loop -> Constructive Interference
            return amplitude
        else:
            # Non-Planar / Higher-Loop -> Destructive Interference
            # Phase shift is exactly pi => factor of -1, but in the sum over all
            # histories, these cancel out against dual diagrams.
            # Effectively, the contribution is zero at the Fixed Point.
            return 0.0

    @staticmethod
    def validate_one_loop_exactness(diagrams: list) -> bool:
        """
        Verify that a set of diagrams satisfies the guard.

        Args:
            diagrams (list): List of dicts {'amplitude': float, 'genus': int}.

        Returns:
            bool: True if only genus-0 diagrams contribute.
        """
        for d in diagrams:
            filtered = SymplecticGuard.filter_amplitude(d['amplitude'], d['genus'])
            if d['genus'] > 0 and filtered != 0.0:
                return False
        return True
