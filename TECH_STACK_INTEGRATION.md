# IRH Tech Stack Integration Guide

**Version:** 1.0.0  
**Date:** December 2025  
**Status:** Complete

This document describes the integrated Physics-ML library stack for the IRH v21.4 computational framework.

## Table of Contents

1. [Overview](#overview)
2. [Library Stack](#library-stack)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The IRH Tech Stack provides unified interfaces to advanced Physics-ML libraries, enabling:

- **GPU Acceleration**: JAX and CuPy for high-performance computing
- **Quantum Simulation**: QuTiP and Dynamiqs for quantum state manipulation
- **Symbolic Mathematics**: SymPy for analytical derivations
- **Differentiable Physics**: JAX-MD and PhiFlow for physics simulations
- **Parallel Computing**: Taichi for custom GPU kernels

All libraries are **optional** - the core IRH framework works with NumPy/SciPy alone. The tech stack gracefully falls back to NumPy implementations when optional libraries are unavailable.

### References

- **Primary**: `.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md` - IRH-Copilot agent specification
- **Theory**: `Intrinsic-Resonance-Holography-21.4-Part1.md` - Computational infrastructure (§1.6)

---

## Library Stack

### Core Dependencies (Always Required)

| Library | Version | Purpose |
|---------|---------|---------|
| NumPy | ≥1.24.0 | Numerical computing |
| SciPy | ≥1.10.0 | Scientific computing |
| SymPy | ≥1.12 | Symbolic mathematics |

### Optional Enhancement Libraries

| Library | Version | Purpose | IRH Application |
|---------|---------|---------|-----------------|
| **JAX** | ≥0.4.0 | Autodiff + GPU | RG flow optimization |
| **JAX-MD** | ≥0.2.0 | Molecular dynamics | G_inf substrate simulation |
| **QuTiP** | ≥5.0.0 | Quantum toolbox | VWP dynamics, quantum states |
| **Dynamiqs** | ≥0.1.0 | GPU quantum sim | Parallel fixed-point search |
| **PhiFlow** | ≥2.5.0 | Differentiable physics | cGFT field evolution |
| **Taichi** | ≥1.6.0 | GPU kernels | Custom QNCD computations |
| **CuPy** | ≥12.0.0 | GPU arrays | Alternative to JAX |
| **NVIDIA Modulus** | ≥0.1.0 | Neural operators | ML surrogates |

---

## Installation

### Minimal Installation (NumPy/SciPy only)

```bash
pip install -r requirements.txt
```

### Full Tech Stack Installation

```bash
# Install core requirements first
pip install -r requirements.txt

# Install Physics-ML enhancement libraries
pip install -r requirements-techstack.txt
```

### Selective Installation

Install only the libraries you need:

```bash
# GPU acceleration with JAX
pip install jax jaxlib jax-md

# Quantum simulation
pip install qutip

# Symbolic math (included in core requirements)
pip install sympy

# High-performance computing
pip install taichi

# Differentiable physics
pip install phiflow
```

### GPU Support

**For CUDA 11.x:**
```bash
pip install cupy-cuda11x
```

**For CUDA 12.x:**
```bash
pip install cupy-cuda12x
```

**For JAX GPU:**
```bash
pip install jax[cuda11_pip] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

---

## Quick Start

### Check Available Libraries

```python
from src.techstack import check_available_libraries, get_tech_stack_status

# Get detailed status
libs = check_available_libraries()
for name, status in libs.items():
    print(f"{status.name}: {'✓' if status.available else '✗'}")

# Or get formatted report
print(get_tech_stack_status())
```

### Configure Backend Preferences

```python
from src.techstack.config import TechStackConfig, apply_config

# Default (CPU-only with NumPy fallback)
config = TechStackConfig.default()

# GPU-optimized
config = TechStackConfig.gpu_optimized()

# Apply configuration
apply_config(config)
```

### Use GPU Backend

```python
from src.techstack.gpu_backend import GPUBackend

backend = GPUBackend()  # Auto-selects best available
print(f"Using backend: {backend.name}")

# Create GPU arrays
arr = backend.zeros((1000, 1000))
result = backend.matmul(arr, arr)

# Convert back to NumPy
numpy_arr = backend.to_numpy(result)
```

---

## Usage Examples

### Example 1: Substrate Dynamics with JAX-MD

```python
from src.techstack.jax_md_wrapper import SubstrateDynamics

# Initialize substrate simulator
dynamics = SubstrateDynamics(n_nodes=100, box_size=10.0, temperature=1.0)

if dynamics.available:
    # Initialize substrate on G_inf = SU(2) × U(1)
    positions = dynamics.initialize_substrate(seed=42)
    
    # Evolve dynamics
    evolved = dynamics.evolve(positions, n_steps=1000, dt=0.001)
    print(f"Final positions shape: {evolved.shape}")
else:
    print("JAX-MD not available, using NumPy fallback")
```

### Example 2: Quantum States with QuTiP

```python
from src.techstack.qutip_wrapper import QuantumState, VortexWavePattern

# Create quantum state handler
qstate = QuantumState(n_levels=4)

if qstate.available:
    # Create superposition
    psi = qstate.create_superposition([0, 1], [0.6, 0.8])
    
    # Evolve under Hamiltonian
    evolved = qstate.evolve(psi, time=1.0)
    
    # Compute resonant proximity
    proximity = qstate.compute_resonant_proximity(psi, evolved)
    print(f"Resonant proximity: {proximity:.6f}")
else:
    print("QuTiP not available")

# Model fermion as VWP
vwp = VortexWavePattern(topological_complexity=207)  # Muon
mass_ratio = vwp.compute_mass_ratio()  # m_μ / m_e
print(f"Predicted mass ratio: {mass_ratio:.1f}")
```

### Example 3: Symbolic Beta Functions

```python
from src.techstack.sympy_helpers import SymbolicBetaFunctions

beta_sym = SymbolicBetaFunctions()

if beta_sym.available:
    # Get symbolic expressions
    beta_lambda = beta_sym.beta_lambda_expr()
    print(f"β_λ = {beta_lambda}")
    
    # Find fixed point
    fp = beta_sym.find_fixed_point_symbolic()
    print(f"Fixed point (one-loop): {fp}")
    
    # Generate LaTeX
    from src.techstack.sympy_helpers import SymbolicDerivations
    deriv = SymbolicDerivations()
    latex = deriv.generate_latex(beta_lambda)
    print(f"LaTeX: {latex}")
```

### Example 4: Quaternionic Field Operations

```python
from src.techstack.sympy_helpers import QuaternionicAlgebra

quat = QuaternionicAlgebra()

if quat.available:
    # Create quaternions
    q1 = quat.create(1, 2, 3, 4)
    q2 = quat.create(5, 6, 7, 8)
    
    # Multiply (non-commutative!)
    product = quat.multiply(q1, q2)
    print(f"q1 * q2 = {product}")
    
    # Conjugate
    q1_bar = quat.conjugate(q1)
    print(f"q̄1 = {q1_bar}")
    
    # Norm
    norm = quat.norm(q1)
    print(f"|q1| = {norm}")
```

### Example 5: GPU-Accelerated Computations

```python
from src.techstack.gpu_backend import GPUBackend, is_gpu_available

if is_gpu_available():
    backend = GPUBackend()
    print(f"Using {backend.name} backend")
    
    # Large matrix multiplication
    N = 5000
    A = backend.array(np.random.rand(N, N))
    B = backend.array(np.random.rand(N, N))
    
    import time
    start = time.time()
    C = backend.matmul(A, B)
    elapsed = time.time() - start
    
    print(f"Matrix multiplication ({N}×{N}): {elapsed:.3f}s")
    
    # Convert to NumPy for analysis
    C_numpy = backend.to_numpy(C)
else:
    print("No GPU backend available, using NumPy")
```

---

## API Reference

### Core Modules

#### `src.techstack.availability`

- `check_available_libraries() -> Dict[str, LibraryStatus]` - Check all libraries
- `get_tech_stack_status() -> str` - Get formatted status report
- `get_required_libraries() -> List[str]` - Get required library names
- `get_optional_libraries() -> List[str]` - Get optional library names
- `check_gpu_available() -> bool` - Check GPU availability

#### `src.techstack.config`

- `TechStackConfig` - Configuration dataclass
  - `TechStackConfig.default()` - CPU-only configuration
  - `TechStackConfig.gpu_optimized()` - GPU-optimized configuration
  - `TechStackConfig.symbolic_analysis()` - Symbolic analysis configuration
  - `TechStackConfig.ml_surrogate()` - ML surrogate configuration
- `get_config() -> TechStackConfig` - Get global configuration
- `set_config(config)` - Set global configuration
- `apply_config(config)` - Apply configuration to all libraries

#### `src.techstack.gpu_backend`

- `GPUBackend` - Unified GPU interface
  - `zeros(shape)` - Create zeros array
  - `ones(shape)` - Create ones array
  - `matmul(a, b)` - Matrix multiplication
  - `to_numpy(arr)` - Convert to NumPy
- `get_default_backend() -> GPUBackend` - Get default backend
- `is_gpu_available() -> bool` - Check GPU availability

#### `src.techstack.jax_md_wrapper`

- `SubstrateDynamics` - JAX-MD substrate simulator
  - `initialize_substrate(seed)` - Initialize positions
  - `evolve(positions, n_steps, dt)` - Evolve dynamics
- `is_available() -> bool` - Check JAX-MD availability

#### `src.techstack.qutip_wrapper`

- `QuantumState` - QuTiP quantum state handler
  - `create_basis_state(level)` - Create |n⟩
  - `create_superposition(levels, coefficients)` - Create superposition
  - `evolve(state, time, hamiltonian)` - Evolve state
  - `compute_resonant_proximity(state1, state2)` - Compute fidelity
- `VortexWavePattern` - VWP handler
  - `create_vwp_state(n_levels)` - Create VWP state
  - `compute_mass_ratio(K_f_reference)` - Compute mass from K_f

#### `src.techstack.sympy_helpers`

- `SymbolicBetaFunctions` - Symbolic RG flow
  - `beta_lambda_expr()` - Get β_λ expression
  - `beta_gamma_expr()` - Get β_γ expression
  - `beta_mu_expr()` - Get β_μ expression
  - `find_fixed_point_symbolic()` - Solve β=0
- `QuaternionicAlgebra` - Quaternion operations
  - `create(w, x, y, z)` - Create quaternion
  - `multiply(q1, q2)` - Quaternion product
  - `conjugate(q)` - Conjugate q̄
  - `norm(q)` - Compute |q|
- `SymbolicDerivations` - Symbolic helpers
  - `verify_commutator(A, B)` - Compute [A,B]
  - `generate_latex(expr)` - Generate LaTeX

---

## Testing

### Run Tech Stack Tests

```bash
# Run all tech stack tests
pytest tests/techstack/ -v

# Run specific library tests
pytest tests/techstack/test_availability.py -v
pytest tests/techstack/test_gpu_backend.py -v

# Run with coverage
pytest tests/techstack/ --cov=src.techstack --cov-report=html
```

### Test Individual Components

```python
# Test availability checker
python -c "from src.techstack import get_tech_stack_status; print(get_tech_stack_status())"

# Test GPU backend
python -c "from src.techstack.gpu_backend import GPUBackend; b = GPUBackend(); print(b.name)"

# Test SymPy helpers
python -c "from src.techstack.sympy_helpers import SymbolicBetaFunctions; s = SymbolicBetaFunctions(); print(s.beta_lambda_expr())"
```

---

## Troubleshooting

### Common Issues

#### "Module not found" errors

**Solution:** The library is optional. Either install it with `pip install <library>` or the code will use NumPy fallback automatically.

#### JAX GPU not detected

```python
import jax
print(jax.devices())  # Should show GPU devices
```

**Solution:** Ensure CUDA is installed and JAX GPU version is installed:
```bash
pip install jax[cuda11_pip] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
```

#### CuPy CUDA version mismatch

**Solution:** Install CuPy matching your CUDA version:
```bash
# Check CUDA version
nvcc --version

# Install matching CuPy
pip install cupy-cuda11x  # for CUDA 11.x
pip install cupy-cuda12x  # for CUDA 12.x
```

#### Taichi initialization errors

```python
import taichi as ti
ti.init(arch=ti.cpu)  # Force CPU if GPU fails
```

#### PhiFlow import errors

**Solution:** PhiFlow requires specific TensorFlow/PyTorch versions. Install compatible version:
```bash
pip install phiflow[jax]  # For JAX backend
```

### Performance Tips

1. **Use GPU for large computations** (N > 1000)
2. **JIT compile with JAX** for repeated operations
3. **Batch operations** when possible
4. **Profile with** `time` or `cProfile` to identify bottlenecks

### Getting Help

- **Issues**: Open issue on GitHub with `tech-stack` label
- **Documentation**: See `.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md`
- **Theory**: Consult IRH v21.4 Manuscript sections

---

## Integration Checklist

✅ **Core modules created:**
- [x] `src/techstack/__init__.py`
- [x] `src/techstack/availability.py`
- [x] `src/techstack/config.py`
- [x] `src/techstack/gpu_backend.py`
- [x] `src/techstack/jax_md_wrapper.py`
- [x] `src/techstack/qutip_wrapper.py`
- [x] `src/techstack/sympy_helpers.py`

✅ **Requirements files:**
- [x] `requirements-techstack.txt` created
- [x] `requirements.txt` updated with references

✅ **Documentation:**
- [x] `TECH_STACK_INTEGRATION.md` created
- [x] Usage examples included
- [x] API reference complete

✅ **Testing:**
- [ ] Unit tests for all wrappers (next step)
- [ ] Integration tests with IRH modules (next step)
- [ ] Performance benchmarks (next step)

---

**Version History:**

- **1.0.0** (December 2025): Initial tech stack integration

**Related Documents:**

- `.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md` - IRH-Copilot specification
- `.github/copilot-instructions.md` - Repository instructions
- `README.md` - Main project documentation
