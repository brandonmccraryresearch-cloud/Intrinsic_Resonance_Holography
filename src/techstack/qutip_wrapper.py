"""
QuTiP Integration Wrapper.

Provides unified interface to QuTiP for quantum state manipulation
and VWP (Vortex Wave Pattern) dynamics.

References
----------
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - QuTiP patterns
IRH v21.4 Manuscript, Appendix D.2 - VWP fermionic defects
"""

from typing import Optional, List
import numpy as np

# Optional import
try:
    import qutip as qt
    QUTIP_AVAILABLE = True
except ImportError:
    QUTIP_AVAILABLE = False


class QuantumState:
    """
    Wrapper for quantum state manipulation using QuTiP.
    
    Encodes group elements as quantum states |g⟩ and simulates
    VWP (Vortex Wave Pattern) dynamics.
    
    References
    ----------
    IRH v21.4 Manuscript, Appendix D.2 - Vortex Wave Patterns
    
    Examples
    --------
    >>> qstate = QuantumState(n_levels=4)
    >>> if qstate.available:
    ...     psi = qstate.create_superposition([0, 1])
    ...     evolved = qstate.evolve(psi, time=1.0)
    """
    
    def __init__(self, n_levels: int = 4):
        """
        Initialize quantum state handler.
        
        Parameters
        ----------
        n_levels : int
            Number of quantum levels (dimension of Hilbert space).
        
    References
    ----------
    .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Tech stack integration
    """
        self.n_levels = n_levels
        self.available = QUTIP_AVAILABLE
    
    def create_basis_state(self, level: int) -> Optional[object]:
        """
        Create basis state |n⟩.
        
        Parameters
        ----------
        level : int
            Which basis state to create.
            
        Returns
        -------
        Qobj or None
            QuTiP quantum object or None if QuTiP unavailable.
        
    References
    ----------
    .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Tech stack integration
    """
        if not self.available:
            return None
        
        return qt.basis(self.n_levels, level)
    
    def create_superposition(
        self,
        levels: List[int],
        coefficients: Optional[List[complex]] = None
    ) -> Optional[object]:
        """
        Create superposition state.
        
        Parameters
        ----------
        levels : List[int]
            Which basis states to include.
        coefficients : List[complex], optional
            Superposition coefficients. If None, equal superposition.
            
        Returns
        -------
        Qobj or None
            Superposition state or None if QuTiP unavailable.
        
    References
    ----------
    .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Tech stack integration
    """
        if not self.available:
            return None
        
        if coefficients is None:
            coefficients = [1.0 / np.sqrt(len(levels))] * len(levels)
        
        state = sum(c * qt.basis(self.n_levels, l) 
                   for c, l in zip(coefficients, levels))
        return state.unit()
    
    def evolve(
        self,
        state: object,
        time: float,
        hamiltonian: Optional[object] = None
    ) -> Optional[object]:
        """
        Evolve quantum state under Hamiltonian.
        
        Parameters
        ----------
        state : Qobj
            Initial state.
        time : float
            Evolution time.
        hamiltonian : Qobj, optional
            Hamiltonian operator. If None, uses SU(2) generators.
            
        Returns
        -------
        Qobj or None
            Evolved state or None if QuTiP unavailable.
        
    References
    ----------
    .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Tech stack integration
    """
        if not self.available:
            return None
        
        if hamiltonian is None:
            # Default: use SU(2) generators (Pauli matrices)
            hamiltonian = qt.sigmax() + qt.sigmay() + qt.sigmaz()
        
        # Schrodinger equation evolution
        result = qt.sesolve(hamiltonian, state, [0, time])
        return result.states[-1]
    
    def compute_resonant_proximity(
        self,
        state1: object,
        state2: object
    ) -> float:
        """
        Compute Resonant Proximity via quantum fidelity.
        
        Parameters
        ----------
        state1, state2 : Qobj
            Quantum states to compare.
            
        Returns
        -------
        float
            Fidelity between 0 and 1, or -1 if QuTiP unavailable.
            
        References
        ----------
        IRH v21.4 Manuscript, Appendix A.2 - Resonant Proximity
        """
        if not self.available:
            return -1.0
        
        return qt.fidelity(state1, state2)


class VortexWavePattern:
    """
    Wrapper for VWP (Vortex Wave Pattern) dynamics.
    
    Models stable topological defects that correspond to fermions.
    
    References
    ----------
    IRH v21.4 Manuscript, Appendix D.2 - VWP fermionic defects
    """
    
    def __init__(self, topological_complexity: int = 1):
        """
        Initialize VWP handler.
        
        Parameters
        ----------
        topological_complexity : int
            K_f value (1 for electron, ~207 for muon, ~3477 for tau).
        
    References
    ----------
    .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Tech stack integration
    """
        self.K_f = topological_complexity
        self.available = QUTIP_AVAILABLE
    
    def create_vwp_state(self, n_levels: int = 10) -> Optional[object]:
        """
        Create VWP quantum state.
        
        **Note:** This is a simplified placeholder using a coherent state.
        The actual VWP has complex topological structure (see Appendix D.2)
        and should use the full implementation in src/topology/vortex_wave_patterns.py
        for production computations.
        
        Parameters
        ----------
        n_levels : int
            Hilbert space dimension.
            
        Returns
        -------
        Qobj or None
            Simplified VWP state or None if QuTiP unavailable.
            
        References
        ----------
        IRH v21.4 Manuscript, Appendix D.2 - VWP fermionic defects
        """
        if not self.available:
            return None
        
        # Simplified coherent state approximation
        # TODO: Replace with proper topological VWP structure from src/topology/
        state = qt.coherent(n_levels, np.sqrt(self.K_f))
        return state
    
    def compute_mass_ratio(self, K_f_reference: int = 1) -> float:
        """
        Compute simplified mass ratio from topological complexity.
        
        **Warning:** This is an oversimplified approximation. The full fermion
        mass formula (Eq. 3.6) includes Yukawa RG running factors (R_Y) and
        other corrections. For production use, see src/standard_model/fermion_masses.py
        which implements the complete formula.
        
        Parameters
        ----------
        K_f_reference : int
            Reference K_f value (typically 1 for electron).
            
        Returns
        -------
        float
            Simplified mass ratio m/m_e (not including RG corrections).
            
        References
        ----------
        IRH v21.4 Manuscript, Equation 3.6 - Fermion mass formula (full version)
        """
        # Simplified ratio without RG running factors
        # Full formula: m_f = (K_f / K_e) * R_Y * m_e * (additional corrections)
        return self.K_f / K_f_reference


def is_available() -> bool:
    """Check if QuTiP is available."""
    return QUTIP_AVAILABLE


def get_version() -> Optional[str]:
    """Get QuTiP version if available."""
    if QUTIP_AVAILABLE:
        try:
            return qt.__version__
        except Exception:
            return "unknown"
    return None
