#!/usr/bin/env python
"""
IRH Tech Stack Integration Example

Demonstrates the use of Physics-ML libraries in IRH computations.

This script showcases:
1. Library availability checking
2. Backend configuration
3. Symbolic beta function derivation
4. Quaternionic algebra
5. GPU-accelerated computations (if available)

References
----------
TECH_STACK_INTEGRATION.md - Complete documentation
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - IRH-Copilot specification
"""

import sys
import numpy as np
from src.techstack import check_available_libraries, get_tech_stack_status
from src.techstack.config import TechStackConfig, apply_config
from src.techstack.gpu_backend import GPUBackend
from src.techstack.sympy_helpers import SymbolicBetaFunctions, QuaternionicAlgebra
from src.techstack.jax_md_wrapper import SubstrateDynamics
from src.techstack.qutip_wrapper import QuantumState, VortexWavePattern


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def demo_availability():
    """Demonstrate library availability checking."""
    print_section("Library Availability Check")
    
    print(get_tech_stack_status())


def demo_symbolic_derivations():
    """Demonstrate symbolic mathematics with SymPy."""
    print_section("Symbolic Beta Functions (SymPy)")
    
    beta_sym = SymbolicBetaFunctions()
    
    if not beta_sym.available:
        print("⚠ SymPy not available")
        return
    
    print("\nRG Flow Beta Functions (Eq. 1.13):")
    print(f"  β_λ = {beta_sym.beta_lambda_expr()}")
    print(f"  β_γ = {beta_sym.beta_gamma_expr()}")
    print(f"  β_μ = {beta_sym.beta_mu_expr()}")
    
    # Fixed point
    fp = beta_sym.find_fixed_point_symbolic()
    print(f"\nFixed Point (one-loop approximation):")
    print(f"  λ* = {fp['lambda_star']}")
    print(f"  Note: {fp['note']}")


def demo_quaternionic_algebra():
    """Demonstrate quaternionic algebra."""
    print_section("Quaternionic Field Operations (SymPy)")
    
    quat = QuaternionicAlgebra()
    
    if not quat.available:
        print("⚠ SymPy not available")
        return
    
    # Create quaternions
    q1 = quat.create(1, 2, 3, 4)
    q2 = quat.create(5, 6, 7, 8)
    
    print(f"\nQuaternion 1: {q1}")
    print(f"Quaternion 2: {q2}")
    
    # Operations
    product = quat.multiply(q1, q2)
    print(f"\nq1 * q2 = {product}")
    
    q1_bar = quat.conjugate(q1)
    print(f"q̄1 = {q1_bar}")
    
    norm = quat.norm(q1)
    print(f"|q1| = {norm}")


def demo_gpu_backend():
    """Demonstrate GPU backend."""
    print_section("GPU Backend Abstraction")
    
    backend = GPUBackend()
    print(f"\nUsing backend: {backend.name}")
    print(f"GPU available: {backend.is_gpu}")
    
    # Small matrix multiplication demo
    N = 100
    print(f"\nMatrix multiplication test ({N}×{N}):")
    
    A = backend.zeros((N, N))
    B = backend.ones((N, N))
    
    C = backend.matmul(A, B)
    
    print(f"  Result shape: {C.shape}")
    print(f"  Sum of elements: {np.sum(backend.to_numpy(C)):.1f}")
    print(f"  ✓ Matrix operations working")


def demo_substrate_dynamics():
    """Demonstrate substrate dynamics simulation."""
    print_section("Substrate Dynamics (JAX-MD)")
    
    dynamics = SubstrateDynamics(n_nodes=50, box_size=5.0)
    
    if not dynamics.available:
        print("⚠ JAX-MD not available - using NumPy fallback")
    
    print(f"\nSimulating {dynamics.n_nodes} substrate nodes on G_inf = SU(2) × U(1)")
    
    # Initialize
    positions = dynamics.initialize_substrate(seed=42)
    print(f"Initial positions shape: {positions.shape}")
    
    # Evolve (simplified demonstration)
    print("Evolving substrate dynamics...")
    evolved = dynamics.evolve(positions, n_steps=10, dt=0.01)
    print(f"Final positions shape: {evolved.shape}")
    print("✓ Substrate evolution complete")


def demo_quantum_states():
    """Demonstrate quantum state manipulation."""
    print_section("Quantum States & VWP (QuTiP)")
    
    qstate = QuantumState(n_levels=4)
    
    if not qstate.available:
        print("⚠ QuTiP not available")
        return
    
    print("\nCreating quantum superposition:")
    psi = qstate.create_superposition([0, 1])
    print(f"  |ψ⟩ = (|0⟩ + |1⟩)/√2")
    
    # Evolve
    print("\nEvolving under SU(2) Hamiltonian...")
    evolved = qstate.evolve(psi, time=0.5)
    
    # Compute proximity
    proximity = qstate.compute_resonant_proximity(psi, evolved)
    print(f"  Resonant proximity: {proximity:.6f}")
    
    # VWP demonstration
    print("\nVortex Wave Pattern (VWP):")
    print("  Electron (K_f = 1):")
    vwp_e = VortexWavePattern(topological_complexity=1)
    print(f"    Mass ratio: {vwp_e.compute_mass_ratio():.1f}")
    
    print("  Muon (K_f = 207):")
    vwp_mu = VortexWavePattern(topological_complexity=207)
    print(f"    Mass ratio: {vwp_mu.compute_mass_ratio():.1f}")


def demo_configuration():
    """Demonstrate configuration management."""
    print_section("Configuration Management")
    
    print("\nAvailable configurations:")
    
    configs = {
        "Default (CPU-only)": TechStackConfig.default(),
        "GPU-optimized": TechStackConfig.gpu_optimized(),
        "Symbolic analysis": TechStackConfig.symbolic_analysis(),
        "ML surrogate": TechStackConfig.ml_surrogate(),
    }
    
    for name, config in configs.items():
        print(f"\n{name}:")
        print(f"  GPU backend: {config.gpu_backend.value}")
        print(f"  Quantum backend: {config.quantum_backend.value}")
        print(f"  Precision: {config.precision}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  IRH Tech Stack Integration Demo")
    print("  Demonstrating Physics-ML library integration")
    print("=" * 70)
    
    # Run demonstrations
    demo_availability()
    demo_configuration()
    demo_symbolic_derivations()
    demo_quaternionic_algebra()
    demo_gpu_backend()
    demo_substrate_dynamics()
    demo_quantum_states()
    
    # Summary
    print_section("Summary")
    libs = check_available_libraries()
    available = sum(1 for lib in libs.values() if lib.available)
    total = len(libs)
    
    print(f"\n✅ Demo complete!")
    print(f"Libraries available: {available}/{total}")
    print("\nFor more information, see:")
    print("  - TECH_STACK_INTEGRATION.md")
    print("  - .github/GITHUB_COPILOT_AGENT_IRH_v21.4.md")
    print("  - requirements-techstack.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
