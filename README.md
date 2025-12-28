# Intrinsic Resonance Holography v22.2: The Cymatic Singularity

<div align="right">

[![Cite this Repository](https://img.shields.io/badge/Cite-Repository-orange?logo=github)](https://github.com/brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography-#-citation) [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography-/blob/main/notebooks/00_quickstart.ipynb)

</div>

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-1000%2B%20passing-brightgreen.svg)](./tests/)
[![Coverage](https://img.shields.io/badge/critical%20equations-100%25-brightgreen.svg)](./THEORETICAL_CORRESPONDENCE.md)

**A complete computational framework deriving fundamental physics from vibrational first principles—transmuting the ontology from Information to Cymatic Resonance.**

---

## 📚 Documentation Quick Links

| Document | Description |
|----------|-------------|
| [**IRH v22.2 Manuscript**](./Intrinsic_Resonance_Holography-v21.1-Part1.md) | 📖 Theoretical foundation: The Cymatic Singularity |
| [**Technical Reference Manual**](./docs/TECHNICAL_REFERENCE.md) | Specifications for CRN, ARO, and Symplectic Guard |
| [**Continuation Guide**](./docs/CONTINUATION_GUIDE.md) | Roadmap for the vibrational ontology transition |
| [**Theoretical Correspondence Map**](./THEORETICAL_CORRESPONDENCE.md) | Mapping code to v22.2 equations |
| [**GitHub Copilot Instructions**](./AGENTS.md) | 🤖 Directives for AI agents (The Mathematician persona) |

---

## 🎯 Overview

**Intrinsic Resonance Holography (IRH) v22.2** marks a paradigm shift from Digital Physics ("It from Bit") to **Cymatic Ontology** ("It from Vibration"). This repository implements the universe as a **Cymatic Resonance Network (CRN)** where fundamental constants and physical laws emerge as resonant eigenvalues of a primordial substrate.

### Core Framework (v22.2)

1.  **Ontological Primitive**: The **NodeOscillator** defined by Phase, Amplitude, and Frequency, not bits.
2.  **Fundamental Dynamics**: Coupled oscillations on a discrete graph minimizing the **Dissonance Functional** ($\Gamma$).
3.  **Emergent Physics**:
    *   **Space**: Emerges from the conductivity of the resonance network ($g_{\mu\nu}$).
    *   **Matter**: Stable **Vortex Wave Patterns (VWPs)** in the resonance field.
    *   **Constants**: Determined by **Phase-Locked Holonomy** ($\alpha^{-1}$) and **Holographic Hum** ($\Lambda$).
4.  **Symplectic Guard**: A filtering mechanism that enforces **One-Loop Exactness** by destructively interfering non-planar diagrams.

### Key Predictions (v22.2)

| Observable | IRH Prediction | Mechanism | Reference |
|-----------|---------------|-----------|-----------|
| Fine-structure constant α⁻¹ | ~137.036 | Phase-Locked Holonomy | Eq. 4.1 |
| Cosmological Constant Λ | ~10⁻⁵² m⁻² | Holographic Hum (Zero-point energy) | Thm 10.1 |
| Spacetime Dimension | 4 | Spectral Stability Criterion | Thm 2.1 |
| SGWB Spectrum | Discrete Comb (ULF) | Cymatic Redshift Broadening | §5.1 |

---

## ✨ Key Features

*   **Cymatic Resonance Network (CRN)**: A graph-based simulation engine for coupled oscillators.
*   **Adaptive Resonance Optimization (ARO)**: A novel solver that "tunes" the network to minimize dissonance, deriving constants without fitting.
*   **Symplectic Guard**: Automated diagrammatic filtering ensuring mathematical rigor.
*   **Legacy Features**: Includes all v21.1 capabilities (web interface, desktop app, ML surrogates) adapted to the new ontology.

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography-.git
cd Intrinsic_Resonance_Holography-
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Analytical Closure Verification

Run the test suite to confirm the derivation of $\alpha^{-1}$ from topological inputs:

```bash
python3 tests/v22_2_cymatic_verification.py
```

### Example: Simulating the Substrate

```python
from src.substrate.manifold import CymaticResonanceNetwork

# Initialize a 4D resonant cavity
crn = CymaticResonanceNetwork(num_nodes=1000, dimension=4)

# Evolve the network
for _ in range(100):
    crn.step(dt=0.01)

# Check synchronization
r = crn.get_synchrony_order_parameter()
print(f"Network Synchrony: {r:.4f}")
```

---

## 🏗️ Repository Architecture (v22.2)

The codebase is stratified by the **Cymatic Ontology**:

```
src/
├── substrate/       # The Medium: NodeOscillators, Manifold, Holonomy
├── operators/       # The Dynamics: Laplacian, Symplectic Guard, ARO
├── physics/         # The Result: Constants, Tensors (Stress-Energy, Metric)
├── observables/     # The Evidence: SGWB, Spectral lines
├── ml/              # Surrogate models (v21 legacy + v22 adapters)
└── webapp/          # User Interface
```

---

## 📄 License

**GPL v3**. See [LICENSE](./LICENSE).

---

> **Note**: This repository represents the "Cymatic Singularity" architecture (v22.2). Legacy v21.1 code remains available but the primary development focus is on the vibrational paradigm.
