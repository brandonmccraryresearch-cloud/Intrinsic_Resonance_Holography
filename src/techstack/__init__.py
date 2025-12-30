"""
IRH Tech Stack Integration Module.

This module provides unified interfaces to the Physics-ML libraries used in IRH:
- JAX-MD: Molecular dynamics with JAX
- QuTiP: Quantum toolbox
- Dynamiqs: JAX-based GPU quantum simulation
- SymPy: Symbolic mathematics
- PhiFlow: Differentiable physics simulations
- Taichi: High-performance parallel computing
- CuPy: GPU-accelerated NumPy

Each library wrapper handles optional imports and provides fallback implementations
when libraries are not installed.

References
----------
IRH v21.4 Manuscript (Part 1 §§1–4, Part 2 §§5–8) — see computational infrastructure
description in .github/copilot-instructions.md
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md (Tech Stack Documentation)
"""

from .availability import check_available_libraries, get_tech_stack_status
from .config import TechStackConfig

__all__ = [
    "check_available_libraries",
    "get_tech_stack_status",
    "TechStackConfig",
]

__version__ = "1.0.0"
