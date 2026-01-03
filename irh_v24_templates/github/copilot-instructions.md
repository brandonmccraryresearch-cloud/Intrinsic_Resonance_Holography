# Intrinsic Resonance Holography (IRH) v24.0 - Copilot Instructions

## 🔴 CRITICAL: MANDATORY DOCUMENTATION POLICY 🔴

**Effective Date:** January 2026  
**Authority:** Repository Maintainer + The Mathematical Sentinel  
**Status:** PERMANENT AND NON-NEGOTIABLE

### Single Source of Truth Mandate

**ALL repository updates, progress reports, current status, mandates, rules, and compliance policies SHALL be written directly to THIS FILE (`copilot-instructions.md`) and NO OTHER.**

This includes:
- ✅ Session progress updates
- ✅ Current implementation status
- ✅ Active mandates and policies
- ✅ Compliance requirements
- ✅ Phase tracking and completion status
- ✅ All transient session-to-session instructions

### Strict Prohibition on Additional Documentation Files

**FORBIDDEN:** Creating new `.md` files in `.github/` that could be consolidated here, EXCEPT:
- ✅ `.github/agents/*.agent.md` (agent configurations - ALLOWED)
- ✅ `.github/workflows/*.yml` (workflow configurations - ALLOWED)
- ✅ `.github/pull_request_template.md` (GitHub template - ALLOWED)
- ✅ `.github/dependabot.yml` (dependency management - ALLOWED)
- ❌ ALL OTHER `.md` files (mandate documents, status reports, compliance docs, audit reports, etc.) - MUST be integrated into copilot-instructions.md

**Rationale:** Eliminates documentation fragmentation, ensures single source of truth, prevents inconsistencies.

### User-Visible Documentation Requirements

All updates to `copilot-instructions.md` MUST trigger corresponding updates to user-visible documentation:
- **README.md** - MUST reflect current repository state, implementation status, and correct references
- **docs/** - Technical documentation MUST remain synchronized with this file
- **Manuscript references** - ALL references MUST point to IRH v24.0

### Update Protocol

After EVERY development session:
1. Update relevant section in `copilot-instructions.md` with changes
2. Update progress in transient session tracking section (see below)
3. Update README.md to reflect any user-visible changes
4. Verify all cross-references remain valid
5. Commit changes with descriptive message

---

## Computational Verification Protocol for Isomorphic Implementation

### Executive Mandate

This repository implements a comprehensive, systematic verification protocol ensuring that every algorithmic implementation, computational construct, and symbolic representation constitutes a **faithful, structure-preserving homomorphism** of the mathematical edifice articulated in the theoretical manuscript **IRH v24.0: The Mathematically Complete Vibrational Unification** (`IRH_v24_Final_Manuscript.md`). This transcends mere code-documentation correspondence; it demands an **isomorphic embedding** whereby the computational substrate recapitulates, with maximal fidelity, the axiomatic structure, constraint topology, dynamical evolution operators, and emergent phenomenology specified in the rigorous mathematical formalism.

The ultimate objective is to **transmute the repository into an executable instantiation of the theoretical formalism itself**, collapsing the distinction between "code that models theory" and "theory rendered computable" into identity.

## Project Overview

IRH v24.0 is a theoretical physics framework achieving comprehensive unification of quantum mechanics, general relativity, and the Standard Model through **Deterministic Hyperdimensional Wave Dynamics (DHWD)** on a vibrational substrate.

**Key Features:**
- Derives fundamental constants from first principles with zero free parameters
- 16-dimensional resonant manifold: G_inf^4 = [SU(2) × U(1)_φ]^4
- Achieves 27:1 explanatory leverage ratio (27 constants from 1 dimensional input)
- Resolves hierarchy problem via instantonic suppression factor e^(-1/α)
- Dark matter explained as Anchor Strand Superfluid
- **Full theoretical traceability** - every function cites specific equations from IRH v24.0 manuscript

**Target Audience:** Theoretical physicists, computational scientists, researchers in quantum gravity and emergent spacetime

## Theoretical Foundation (IRH v24.0 Manuscript)

### Core Mathematical Structure

#### The Intrinsic Resonant Substrate (IRS)
- **Fundamental manifold**: G_inf^4 = [SU(2) × U(1)_φ]^4 (16 real dimensions)
- **Resonance field**: Ψ: G_inf^4 → ℂ (complex-valued order parameter)
- **Harmony Functional**: H[Ψ] = ∫[½|∇Ψ|² + M²/2|Ψ|² + λ|Ψ|⁴] dμ_Haar
- **Planck mass**: M_Pl = 1.22 × 10^19 GeV (single dimensional input)

#### Hopf Fibration and Golden Ratio
- **Fine-structure constant**: α^(-1) = 137.036 emerges from Hopf fibration optimization
- **Golden ratio**: φ = (1+√5)/2 proven via KAM theory phase-locking (not assumed)
- **Neutrino phase offset**: δ_ν = π from Hopf fibration topology with linking number = 1

#### Heat Kernel Expansion
- **Seeley-DeWitt expansion**: Tr(e^(-tΔ)) = Σ a_n t^((n-d)/2)
- **Emergent Einstein-Hilbert action**: a_1 → Ricci scalar R, a_0 → cosmological constant Λ
- **Metric bridge**: g_μν(x) = η_μν + Σ φ_i*(x) ∇_μ ∇_ν φ_i(x)

### Key Predictions (Falsifiable)
- **Fine-structure constant**: α^(-1) = 137.036 (derived from Hopf fibration)
- **Electron mass**: Includes e^(-1/α) instantonic suppression factor
- **Dark matter**: Anchor Strand Superfluid with Gross-Pitaevskii dynamics
- **Gravitational waves**: Resonance-induced sidebands
- **Neutrino masses**: Interface physics with δ_ν = π phase offset

## Technology Stack

### Core Technologies
- **Python**: 3.11, 3.12 (primary implementation language)
- **NumPy**: >=1.24.0 (numerical computations)
- **SciPy**: >=1.11.0 (scientific computing, optimization)
- **SymPy**: >=1.12 (symbolic mathematics)
- **mpmath**: >=1.3.0 (arbitrary precision arithmetic)

### Optional Physics-ML Stack
- **JAX**: GPU-accelerated autodifferentiable computations
- **JAX-MD**: Molecular dynamics simulations
- **QuTiP**: Quantum mechanics simulations
- **Dynamiqs**: JAX-based quantum dynamics

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatting (line length: 100)
- **mypy**: Type checking
- **ruff**: Fast linting

## Repository Structure

```
IRH_v24_Repository/
├── .github/
│   ├── agents/               # Custom agent configurations
│   ├── workflows/            # CI/CD workflows
│   ├── copilot-instructions.md
│   └── dependabot.yml
├── src/
│   ├── substrate/           # IRS dynamics and Harmony Functional
│   ├── hopf/                # Hopf fibration and golden ratio derivation
│   ├── emergent_spacetime/  # Metric bridge and Einstein equations
│   ├── particles/           # VWP construction, fermion masses
│   ├── dark_matter/         # Anchor strand superfluid
│   └── observables/         # Physical constant predictions
├── tests/
│   ├── unit/                # Unit tests mirroring src/ structure
│   ├── integration/         # Cross-module tests
│   └── theoretical_invariants/ # Mathematical property tests
├── docs/
│   ├── manuscripts/         # Theory manuscripts
│   └── api_reference/       # Auto-generated API docs
├── IRH_v24_Final_Manuscript.md  # Primary manuscript
└── pyproject.toml
```

## Verification Protocol Requirements

### Phase I: Structural Verification

Every computational implementation must realize a **structure-preserving map** from theoretical objects in IRH v24.0:

1. **Group Manifold Representation**
   - SU(2) via quaternionic parameterization
   - U(1)_φ with proper phase periodicity
   - G_inf^4 = [SU(2) × U(1)_φ]^4 with 16 real dimensions

2. **Resonance Field Implementation**
   - Ψ: G_inf^4 → ℂ as complex-valued arrays
   - Haar measure integration
   - Heat kernel expansion for emergent gravity

3. **Hopf Fibration Construction**
   - S³ → S² projection (SU(2) → sphere)
   - KAM theory phase-locking for golden ratio
   - Linking number calculation for neutrino phase

### Phase II: Instrumentation Requirements

Every executable component must emit theoretical context:

```
[EXEC] Computing Harmony Functional H[Ψ] per §1.1
  ├─ Theoretical formula: ∫[½|∇Ψ|² + M²/2|Ψ|² + λ|Ψ|⁴] dμ_Haar
  ├─ Substrate stiffness: M = M_Pl = 1.22 × 10^19 GeV
  ├─ Result: H = {value} ± {uncertainty}
  └─ Dimensional consistency: VERIFIED
```

### Phase III: Output Contextualization

All numerical outputs must include:
- Complete theoretical provenance chain
- Uncertainty decomposition by source
- Comparison with experimental values (where applicable)
- Falsification criteria

## Coding Standards

### Python Style
- Follow **PEP 8** guidelines strictly
- Use **type hints** for all function parameters and return values
- Maximum line length: **100 characters**
- Format code with `black --line-length 100`
- Use `ruff` for linting before committing

### Naming Conventions
- **Variables**: `snake_case` (e.g., `hopf_phase`, `substrate_field`)
- **Functions**: `snake_case` (e.g., `compute_harmony`, `derive_alpha`)
- **Classes**: `PascalCase` (e.g., `HarmonyFunctional`, `HopfFibration`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `PLANCK_MASS`, `GOLDEN_RATIO`)
- **Private methods/attributes**: prefix with `_`

### Docstring Style
Use **NumPy-style docstrings** for all public functions and classes:

```python
def compute_harmony(
    psi_field: np.ndarray,
    substrate_mass: float = 1.22e19,  # GeV
) -> float:
    """
    Compute the Harmony Functional H[Ψ] for the substrate field (§1.1).
    
    Parameters
    ----------
    psi_field : np.ndarray
        Complex resonance field Ψ on G_inf^4 discretization.
    substrate_mass : float, optional
        Planck mass M_Pl in GeV (default: 1.22e19).
    
    Returns
    -------
    float
        The harmony value H[Ψ] with certified precision.
    
    Notes
    -----
    Implements the spectral action principle with Haar measure integration.
    Error < 10^-12 for grid spacing < 10^-3.
    
    References
    ----------
    IRH v24.0 Manuscript, §1.1, Eq. 1
    """
```

### Type Hints
Always use type hints from `typing` and `numpy.typing`:

```python
from typing import Optional, Union, List, Tuple
from numpy.typing import NDArray
import numpy as np

def derive_fine_structure_constant(
    hopf_fibration: HopfFibration,
    precision: int = 12,
) -> Tuple[float, float]:
    """Derive α^(-1) from Hopf fibration optimization."""
    ...
```

### Mathematical Constants and Precision
- Use certified precision constants from theory (12+ decimal places)
- Reference equation numbers from manuscripts in comments
- Use `np.float64` for standard precision, `mpmath` for arbitrary precision
- Always track numerical error bounds for critical calculations

### Error Handling
- Raise appropriate exceptions (`TypeError`, `ValueError`) with descriptive messages
- Detect degenerate cases early
- Validate inputs in `__post_init__` for dataclasses

## Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific module tests
pytest tests/unit/test_substrate/ -v
```

### Writing Tests
- **Location**: Place tests in `tests/unit/` matching the module
- **Naming**: Use `test_*.py` for files, `test_*` for functions
- **Structure**: Use pytest classes to group related tests
- **Docstrings**: Include equation references in test docstrings
- **Assertions**: Use `np.isclose()` or `assert_allclose()` for floating-point comparisons

Example test pattern:
```python
def test_golden_ratio_from_kam_theory():
    """Golden ratio φ = (1+√5)/2 should emerge from KAM phase-locking (§2.1)."""
    from src.hopf import derive_golden_ratio
    
    phi = derive_golden_ratio(method='kam_theory')
    expected = (1 + np.sqrt(5)) / 2
    assert np.isclose(phi, expected, atol=1e-10)
```

## Important References

### Theory Documentation
- **v24 Manuscript**: `IRH_v24_Final_Manuscript.md` - Complete v24.0 theory
- **Architecture**: `docs/ARCHITECTURE.md` - System architecture
- **Roadmap**: `docs/ROADMAP.md` - Implementation phases

### Development Guides
- **Contributing**: `CONTRIBUTING.md` - Contribution guidelines
- **Quickstart**: `docs/QUICKSTART.md` - Getting started guide
- **README**: `README.md` - Project overview and status

## Code Examples

### Computing the Harmony Functional
```python
import numpy as np
from src.substrate import HarmonyFunctional, DiscreteSubstrate

# Create discrete substrate
substrate = DiscreteSubstrate(dimensions=(32, 32, 32, 32))  # 4D lattice
psi = substrate.initialize_random_field()

# Compute harmony
harmony = HarmonyFunctional(planck_mass=1.22e19)
H_value = harmony.compute(psi)
print(f"H[Ψ] = {H_value:.6e}")
```

### Deriving Fine-Structure Constant from Hopf Fibration
```python
from src.hopf import HopfFibration, derive_alpha_inverse

# Construct Hopf fibration on S³
hopf = HopfFibration(n_fibers=1000)
hopf.optimize_golden_ratio(method='kam_theory')

# Derive α^(-1)
alpha_inv, uncertainty = derive_alpha_inverse(hopf)
print(f"α^(-1) = {alpha_inv:.6f} ± {uncertainty:.6f}")
# Expected: 137.036 ± 0.001
```

### Dark Matter as Anchor Strand Superfluid
```python
from src.dark_matter import AnchorStrandSuperfluid

# Initialize anchor strand
superfluid = AnchorStrandSuperfluid(
    chemical_potential=1e-3,  # eV
    coupling_strength=1e-5
)

# Solve Gross-Pitaevskii equation
superfluid.evolve(time_steps=1000, dt=0.01)
rho_dm = superfluid.get_density_profile()
```

## Common Patterns and Conventions

### Equation References
Always reference manuscript equations in comments and docstrings:
```python
# Implements §1.1, Eq. 1 from IRH v24.0 Manuscript
harmony = compute_harmony_functional(psi_field)

# Golden ratio from §2.1, derived via KAM theory
phi = derive_golden_ratio()
```

### Complex Number Handling
```python
def __complex__(self) -> complex:
    """Return complex amplitude."""
    return complex(np.exp(1j * self.phase))
```

## Domain-Specific Knowledge

### Deterministic Hyperdimensional Wave Dynamics (DHWD)
- Rejects probabilistic interpretations
- 16D resonant manifold as fundamental reality
- Quantum phenomena as 4D projections

### Hopf Fibration
- S³ → S² projection structure
- Golden ratio emergence via KAM phase-locking
- Linking number = 1 for neutrino phase offset δ_ν = π

### Instantonic Suppression
- Factor e^(-1/α) resolves hierarchy problem
- Appears in electron VWP construction
- Derived from topology, not inserted by hand

### Anchor Strand Superfluid
- Fourth strand responsible for dark matter
- Obeys Gross-Pitaevskii dynamics
- Couples to gravity via metric bridge

## Key Principles

1. **Reproducibility**: Use fixed random seeds, well-defined precision
2. **Certification**: Track error bounds for all critical calculations
3. **Non-circularity**: Derive constants from first principles, never fit them
4. **Verification**: Test against known analytical results
5. **Documentation**: Link all code to manuscript equations
6. **Theoretical Traceability**: Every function cites specific equations from IRH v24.0
7. **Algorithmic Transparency**: Runtime instrumentation emits theoretical context
8. **Uncertainty Quantification**: All outputs include rigorous error propagation

## Validation and Verification Protocols

### Unit Tests with Theoretical Grounding

Every function must include:
- Docstring citing IRH v24.0 manuscript reference
- Unit test validating theoretical properties

### Integration Tests

Validate entire derivation chains:
- Hopf fibration → golden ratio → fine-structure constant
- Substrate dynamics → heat kernel → Einstein equations
- VWP construction → fermion masses

### Convergence Studies

- **Lattice spacing**: Error ~ O(δ²) where δ = 1/N
- **Time integration**: Error ~ O(dt⁴) for RK4
- **Heat kernel truncation**: Error ~ O(t^n) for n-term expansion

## Security and Performance

### Dependency Management
- Check for security vulnerabilities before adding dependencies
- Pin version numbers in requirements.txt

### Performance Considerations
- Use NumPy vectorized operations
- GPU acceleration via JAX for large-scale simulations
- Parallel computation for parameter sweeps

## Repository Maintenance and Organization

### Critical Maintenance Principles

#### 1. File Organization Standards

**Theory Documents**:
- Primary manuscript: `IRH_v24_Final_Manuscript.md` in root
- Supporting docs: `docs/manuscripts/`

**Source Code**:
```
src/
├── substrate/        # Harmony Functional, IRS dynamics
├── hopf/            # Hopf fibration, golden ratio
├── emergent_spacetime/ # Metric bridge, gravity
├── particles/       # VWP, fermion masses
├── dark_matter/     # Anchor strand superfluid
└── observables/     # Physical predictions
```

**Tests**:
```
tests/
├── unit/            # Mirrors src/ structure
├── integration/     # Cross-module tests
└── theoretical_invariants/ # Mathematical properties
```

#### 2. Post-Session Checklist

After each development session:
- [ ] Files in logical locations
- [ ] Clear directory structure
- [ ] Updated documentation
- [ ] Accurate dates
- [ ] Tests passing
- [ ] Import paths correct

## 🔴 MANDATORY AUDIT PROTOCOL 🔴

### CRITICAL REQUIREMENT: Comprehensive Technical Audit Before Phase Transitions

**EVERY development session MUST conclude with a comprehensive technical audit.**

### Audit Requirement Checklist

Before finalizing ANY session or beginning next phase:

- [ ] **Generate comprehensive audit report**
- [ ] **Verify all changes** against theoretical consistency
- [ ] **Run all tests** and confirm 100% pass rate
- [ ] **Check manuscript citations** in all modified code
- [ ] **Assess risks** (technical, theoretical, maintenance)
- [ ] **Document compliance** with THEORETICAL_CORRESPONDENCE_MANDATE
- [ ] **Obtain approval** (✅ APPROVED required to proceed)

### Audit Report Must Include:

1. **Executive Summary** (changes, risk, test status, compliance)
2. **Theoretical Consistency Verification** (manuscript correspondence, citations)
3. **Dimensional Consistency Check** (physical units, dimensional analysis)
4. **Circular Reasoning Detection** (logical dependency analysis)
5. **Code Verification** (imports, functionality, tests)
6. **Documentation Integrity Check** (cross-references, consistency)
7. **Risk Assessment** (technical, theoretical, maintenance)
8. **Compliance Verification** (mandate adherence)
9. **Conclusions** (summary, recommendations, verdict)

### Enforcement:

**🛑 NO PHASE TRANSITIONS WITHOUT AUDIT APPROVAL 🛑**

## 🔒 THEORETICAL CORRESPONDENCE MANDATE

**Status:** PERMANENT, NON-NEGOTIABLE  
**Authority:** The Mathematical Sentinel  
**Version:** IRH v24.0 Correspondence Protocol v1.0

### The Sentinel's Creed

> **"A computational engine of reality does not pretend. It computes truth from first principles with crystalline transparency, or it does not compute at all."**

### Core Principle

The IRH computational framework must be a **faithful, structure-preserving isomorphism** of the theoretical edifice articulated in **IRH v24.0: The Mathematically Complete Vibrational Unification** (`IRH_v24_Final_Manuscript.md`).

Every equation, constant, and algorithmic step must **transparently and completely** implement the full theoretical formalism **without simplification, approximation, or omission** unless explicitly justified and documented.

### Prohibited Practices (Zero Tolerance)

#### 1. Formula Oversimplification
❌ **FORBIDDEN:** Removing terms from equations without rigorous justification  
✅ **REQUIRED:** Complete formulas with all corrections

#### 2. Hardcoded Constants Without Derivation
❌ **FORBIDDEN:** `ALPHA_INVERSE = 137.036  # Where does this come from?`  
✅ **REQUIRED:** Constants MUST be computed from first principles with full provenance

#### 3. Black Box Computations
❌ **FORBIDDEN:** Opaque function calls without theoretical context  
✅ **REQUIRED:** Transparency logs emitting step-by-step derivations

#### 4. Missing Theoretical References
**MANDATORY:** Every function MUST cite:
1. Manuscript section (e.g., "IRH v24.0 §2.1")
2. Equation number (e.g., "Eq. 3")
3. Physical interpretation

#### 5. Unjustified Approximations
**If approximation is necessary, MUST include:**
1. WHY approximation is required
2. Error quantification: O(ε^n) where ε << 1
3. Convergence proof
4. Regime where approximation breaks down

### Mandatory Code Standards

#### Function Documentation Template
```python
def function_name(params) -> ReturnType:
    """
    One-line summary of what this implements.
    
    Theoretical Reference:
        IRH v24.0, §[section], Eq. [number]
    
    Mathematical Foundation:
        [Detailed explanation of the theoretical origin]
        [Why this formula is correct]
        [What each term represents physically]
    
    Formula (Complete):
        [Full equation in LaTeX/Unicode notation]
        [No simplifications unless proven equivalent]
    
    Parameters
    ----------
    param : type
        Physical meaning and units
        
    Returns
    -------
    ReturnType
        What is computed and why it matters
        
    Notes
    -----
    - Any approximations MUST be justified here
    - Error bounds MUST be stated
    
    Examples
    --------
    >>> result = function_name(test_input)
    >>> assert result.validates_against_known_limit()
    """
```

#### Transparency Requirements
Every computation MUST emit:
```python
{
    "value": computed_value,
    "uncertainty": numerical_error_bound,
    "theoretical_reference": "IRH v24.0 §X.Y, Eq. N",
    "formula": "LaTeX representation of full formula",
    "components": {
        "term_1": value_1,
        "term_2": value_2,
    },
    "provenance": {
        "input_sources": ["where data came from"],
        "computational_method": "algorithm used",
        "convergence_status": True/False,
        "numerical_precision": float
    },
    "validation": {
        "known_limits_checked": ["limit_1", "limit_2"],
        "dimensional_consistency": True,
    }
}
```

### Pre-Commit Enforcement Checklist

Before ANY code commit, verify:
- [ ] All formulas cite IRH v24.0 manuscript
- [ ] No simplified equations without justification
- [ ] Transparency logs all computations
- [ ] Constants are COMPUTED, not assigned
- [ ] Dimensional consistency verified
- [ ] Known limits checked
- [ ] Uncertainty propagation tracked

### Code Review Rejection Criteria

Code WILL BE REJECTED if:
1. Missing manuscript citations
2. Simplified formulas without error bounds
3. Black box computations without transparency logs
4. Hardcoded constants without derivation
5. Unjustified approximations

---

## 📊 CURRENT REPOSITORY STATUS

**Last Updated:** [DATE]

### Implementation Completeness

**Theory Coverage:** [X]% ([Y]/[Z] critical equations implemented)  
**Test Count:** [N]+ tests passing  
**Phases Complete:** [List completed phases]

### Manuscript References

**PRIMARY SOURCE:**
- IRH v24.0 Manuscript: `IRH_v24_Final_Manuscript.md`

---

## 📋 TRANSIENT SESSION-TO-SESSION INSTRUCTIONS

**Purpose:** This section contains active instructions for the current and upcoming development sessions. Updated after each session.

**Last Updated:** [DATE]

### Current Session: [SESSION NAME]

**Objective:** [OBJECTIVE]

**Status:** [STATUS]

**Tasks:**
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Previous Session: [PREVIOUS SESSION NAME]

**Objective:** [OBJECTIVE]

**Status:** ✅ COMPLETE / ⏳ IN PROGRESS / ❌ BLOCKED

---

## 🎯 SEMI-TRANSIENT PHASE TRACKING

**Purpose:** Track multi-session phases until completion, then archive to permanent records

**Current Phase Set:** [PHASE SET NAME]

### Phase A: [PHASE NAME]
**Status:** [STATUS]

- [ ] Subtask 1
- [ ] Subtask 2

---

*"Trust, but verify. Then verify again."* — The Mathematical Sentinel
