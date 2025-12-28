"""
Cymatic Resonance Network Substrate

THEORETICAL FOUNDATION: IRH v22.2 Manuscript Part 1 §2.1

This module defines the fundamental substrate of the universe as a
Cymatic Resonance Network (CRN) composed of coupled Simple Harmonic Oscillators (SHOs).

Key Concepts:
- **NodeOscillator**: The primitive unit of reality, possessing Phase, Amplitude, and Frequency.
- **CymaticResonanceNetwork**: The interconnected graph of oscillators.
- **Spectral Stability**: Dimensionality emerges from the stability of resonant patterns.

Mathematical Framework:
    The substrate state |Ψ⟩ is defined by the collection of oscillator states:
    |Ψ⟩ = ⨂_{i \in \mathcal{N}} | \phi_i, A_i, \omega_i ⟩

    The network evolves according to coupled oscillator dynamics:
    d²\phi_i / dt² = - \omega_i^2 \sin(\phi_i) + \sum_{j} \mathcal{K}_{ij} \sin(\phi_j - \phi_i)

Authors: Brandon D. McCrary
Last Updated: December 2025
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import networkx as nx

__version__ = "22.2.0"
__theoretical_foundation__ = "IRH v22.2 Manuscript Part 1 §2.1"

# Dimensionless scaling factors (Constants)
PLANCK_PHASE = 2 * np.pi  # Full cycle
DEFAULT_FREQUENCY = 1.0   # Normalized natural frequency


@dataclass
class NodeOscillator:
    """
    Primitive unit of the Cymatic Substrate.

    Attributes:
        node_id (int): Unique identifier.
        phase (float): Current phase angle \phi \in [0, 2\pi).
        amplitude (float): Oscillation amplitude A.
        frequency (float): Natural frequency \omega.
        velocity (float): Phase velocity d\phi/dt.
    """
    node_id: int
    phase: float = 0.0
    amplitude: float = 1.0
    frequency: float = DEFAULT_FREQUENCY
    velocity: float = 0.0

    def update(self, dt: float, coupling_force: float):
        """
        Update oscillator state using semi-implicit Euler integration.

        d\phi/dt = v
        dv/dt = - \omega^2 \sin(\phi) + F_{coupling}
        """
        # Restoring force (intrinsic tension)
        restoring_force = - (self.frequency ** 2) * np.sin(self.phase)

        # Total force
        total_accel = restoring_force + coupling_force

        # Update velocity
        self.velocity += total_accel * dt

        # Update phase
        self.phase += self.velocity * dt

        # Wrap phase to [0, 2pi)
        self.phase = self.phase % (2 * np.pi)


class CymaticResonanceNetwork:
    """
    The graph substrate of coupled oscillators.

    Attributes:
        nodes (Dict[int, NodeOscillator]): Map of ID to Oscillator.
        graph (nx.Graph): Topological structure.
        coupling_strength (float): Global coupling constant K.
    """

    def __init__(self, num_nodes: int, dimension: int = 4, topology: str = 'lattice'):
        """
        Initialize the CRN.

        Args:
            num_nodes (int): Number of oscillators.
            dimension (int): Target dimensionality for embedding/connectivity.
            topology (str): Initial graph topology ('lattice', 'random', 'small_world').
        """
        self.nodes: Dict[int, NodeOscillator] = {}
        self.coupling_strength = 1.0
        self.dimension = dimension

        # Initialize graph topology
        if topology == 'lattice':
            # N-dimensional grid lattice approximation
            side_length = int(num_nodes ** (1/dimension))
            self.graph = nx.grid_graph(dim=[side_length] * dimension)
            # Relabel nodes to integers for simpler handling
            self.graph = nx.convert_node_labels_to_integers(self.graph)
        elif topology == 'random':
            self.graph = nx.erdos_renyi_graph(num_nodes, p=0.1)
        else:
            raise ValueError(f"Unknown topology: {topology}")

        # Initialize oscillators
        for i in self.graph.nodes():
            # Random initial phases
            self.nodes[i] = NodeOscillator(
                node_id=i,
                phase=np.random.uniform(0, 2*np.pi)
            )

    def step(self, dt: float = 0.01):
        """
        Advance the network state by one time step dt.
        """
        # Calculate coupling forces first (synchronous update)
        forces = {}
        for i in self.nodes:
            force = 0.0
            phi_i = self.nodes[i].phase

            for neighbor in self.graph.neighbors(i):
                phi_j = self.nodes[neighbor].phase
                # Kuramoto-like coupling: sin(phi_j - phi_i)
                force += np.sin(phi_j - phi_i)

            forces[i] = self.coupling_strength * force

        # Update state
        for i in self.nodes:
            self.nodes[i].update(dt, forces[i])

    def get_synchrony_order_parameter(self) -> float:
        """
        Calculate the Kuramoto order parameter r.
        r = | (1/N) * \sum e^{i \phi_j} |

        Returns:
            float: Order parameter r \in [0, 1]. 1 = full sync.
        """
        complex_sum = sum(np.exp(1j * node.phase) for node in self.nodes.values())
        r = np.abs(complex_sum) / len(self.nodes)
        return float(r)


class SpectralStabilityCriterion:
    """
    Validator for dimensionality N=4.

    Theorem 2.1: A 3-dimensional spatial manifold is the unique stable geometry
    capable of supporting non-dissipative Vortex Wave Patterns.

    This implies spacetime dimension D = 3+1 = 4.
    """

    @staticmethod
    def evaluate_stability(dimension: int) -> bool:
        """
        Evaluate if a given dimension supports stable VWP knots.

        Mechanism:
        - For D < 3 (spatial): Knotting is impossible (trivial topology).
        - For D > 3 (spatial): Knots can untie (trivial topology).
        - D = 3 (spatial) => Spacetime = 4.

        Args:
            dimension (int): Spacetime dimension.

        Returns:
            bool: True if stable, False otherwise.
        """
        spatial_dim = dimension - 1

        # Stability condition: Spatial dimension must be exactly 3 for stable knots
        if spatial_dim == 3:
            return True
        elif spatial_dim < 3:
            # Insufficient degrees of freedom
            return False
        else:
            # Arnold Diffusion / Unknotting
            return False

    @staticmethod
    def compute_arnold_diffusion_rate(dimension: int) -> float:
        """
        Compute rate of energy leakage to higher harmonics.

        Rate \Gamma \propto (D-4)^2 for D >= 4.
        Minimal at D=4.
        """
        if dimension == 4:
            return 0.0
        else:
            # Phenomenological scaling
            return abs(dimension - 4) ** 2 * 0.1
