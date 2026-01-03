# IRH v24.0 Migration Guide

This guide provides detailed instructions for setting up a new IRH v24.0 repository using the provided templates.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Template Integration](#template-integration)
4. [Creating Essential Scripts](#creating-essential-scripts)
5. [Implementing Core Modules](#implementing-core-modules)
6. [Setting Up Testing Infrastructure](#setting-up-testing-infrastructure)
7. [Configuring CI/CD](#configuring-cicd)
8. [First Implementation Session](#first-implementation-session)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- Python 3.10, 3.11, or 3.12
- Git
- GitHub account
- Text editor or IDE (VS Code recommended)

### Required Knowledge
- Python programming
- Git/GitHub basics
- IRH v24.0 theoretical framework (read the manuscript)

### Optional but Recommended
- Docker (for containerized development)
- LaTeX (for documentation)
- JAX (for GPU acceleration)

---

## Initial Setup

### 1. Create GitHub Repository

```bash
# On GitHub, create new repository
# Name: YOUR-IRH-V24-REPO
# Description: IRH v24.0: The Mathematically Complete Vibrational Unification
# Visibility: Public or Private
# Initialize with README: No (we'll add our own)

# Clone locally
git clone https://github.com/YOUR-ORG/YOUR-IRH-V24-REPO.git
cd YOUR-IRH-V24-REPO
```

### 2. Copy IRH v24.0 Manuscript

```bash
# Copy the primary manuscript to repository root
cp /path/to/IRH_v24_Final_Manuscript.md .

# Commit
git add IRH_v24_Final_Manuscript.md
git commit -m "Add IRH v24.0 manuscript"
git push origin main
```

---

## Template Integration

### 1. Copy Template Files

```bash
# Copy GitHub configuration
cp -r /path/to/irh_v24_templates/github/ .github/

# Verify files copied
ls -la .github/
# Should see: copilot-instructions.md, GITHUB_COPILOT_AGENT_IRH_v24.md,
#             dependabot.yml, pull_request_template.md, workflows/
```

### 2. Customize Repository-Specific References

```bash
# Update GitHub Copilot Agent config
# Replace [YOUR-ORG]/[YOUR-REPO-NAME] with actual values
sed -i 's/\[YOUR-ORG\]\/\[YOUR-REPO-NAME\]/your-org\/your-repo/g' \
    .github/GITHUB_COPILOT_AGENT_IRH_v24.md
```

### 3. Update Copilot Instructions

Edit `.github/copilot-instructions.md`:

```markdown
# In "Current Repository Status" section, update:

**Last Updated:** January 3, 2026

### Implementation Completeness

**Theory Coverage:** 0% (0/27 critical derivations implemented)
**Test Count:** 0 tests
**Phases Complete:** None yet - just getting started!
```

---

## Creating Essential Scripts

### 1. Create `scripts/` Directory

```bash
mkdir -p scripts
```

### 2. Create Compliance Verification Script

Create `scripts/verify_compliance.py`:

```python
#!/usr/bin/env python3
"""
IRH v24.0 Compliance Verification Script

Checks code for theoretical correspondence compliance.
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

def check_manuscript_citations(src_dir: Path) -> Dict:
    """Check that all compute functions cite manuscript."""
    violations = []
    warnings = []
    passes = 0
    
    for py_file in src_dir.rglob("*.py"):
        if "test_" in py_file.name:
            continue
            
        content = py_file.read_text()
        
        # Find all function definitions
        functions = re.findall(r'def (compute_|derive_|calculate_)\w+', content)
        
        for func in functions:
            # Check for IRH v24.0 citation nearby
            func_match = re.search(rf'def {func}.*?""".*?"""', content, re.DOTALL)
            if func_match:
                docstring = func_match.group(0)
                if "IRH v24" in docstring or "§" in docstring:
                    passes += 1
                else:
                    violations.append({
                        "category": "Missing Citation",
                        "file": str(py_file),
                        "message": f"Function {func} lacks IRH v24.0 citation"
                    })
    
    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "warnings": warnings,
        "passes_count": passes
    }

def check_hardcoded_constants(src_dir: Path) -> Dict:
    """Check for hardcoded physical constants."""
    violations = []
    
    patterns = [
        (r"= *137\.03\d+", "Fine-structure constant"),
        (r"= *0\.51\d+ *# *electron", "Electron mass"),
        (r"= *1\.22\d*e19 *(?!.*#.*input)", "Planck mass (should be marked as input)"),
    ]
    
    for py_file in src_dir.rglob("*.py"):
        if "test_" in py_file.name:
            continue
            
        content = py_file.read_text()
        
        for pattern, description in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Check if marked as derived or computed
                line = content[max(0, match.start()-50):match.end()+50]
                if "derived" not in line.lower() and "computed" not in line.lower():
                    violations.append({
                        "category": "Hardcoded Constant",
                        "file": str(py_file),
                        "message": f"Potential hardcoded {description} without derivation"
                    })
    
    return violations

def main():
    src_dir = Path("src")
    if not src_dir.exists():
        print("Error: src/ directory not found")
        sys.exit(1)
    
    # Run checks
    citation_results = check_manuscript_citations(src_dir)
    constant_violations = check_hardcoded_constants(src_dir)
    
    # Combine results
    all_violations = citation_results["violations"] + constant_violations
    
    report = {
        "compliant": len(all_violations) == 0,
        "violations": all_violations,
        "warnings": citation_results["warnings"],
        "passes_count": citation_results["passes_count"]
    }
    
    # Write report
    with open("compliance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"Compliance Check: {'✅ PASSED' if report['compliant'] else '❌ FAILED'}")
    print(f"Passes: {report['passes_count']}")
    print(f"Violations: {len(all_violations)}")
    print(f"Warnings: {len(report['warnings'])}")
    
    sys.exit(0 if report['compliant'] else 1)

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x scripts/verify_compliance.py
```

### 3. Create Theoretical Annotation Verification

Create `scripts/verify_theoretical_annotations.py`:

```python
#!/usr/bin/env python3
"""Verify all functions have theoretical annotations."""
import re
from pathlib import Path

def check_file(filepath: Path):
    """Check a single file for annotation compliance."""
    content = filepath.read_text()
    
    # Find all public functions
    functions = re.finditer(r'def ([a-z_]\w+)\(', content)
    
    missing_citations = []
    for match in functions:
        func_name = match.group(1)
        if func_name.startswith('_'):  # Private function
            continue
            
        # Check docstring has reference
        func_start = match.start()
        next_500 = content[func_start:func_start+500]
        
        if '"""' in next_500 or "'''" in next_500:
            if "IRH v24" not in next_500 and "§" not in next_500:
                missing_citations.append(func_name)
        else:
            missing_citations.append(f"{func_name} (no docstring)")
    
    return missing_citations

def main():
    src_dir = Path("src")
    all_missing = {}
    
    for py_file in src_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
            
        missing = check_file(py_file)
        if missing:
            all_missing[str(py_file)] = missing
    
    if all_missing:
        print("⚠️  Missing theoretical citations:")
        for filepath, functions in all_missing.items():
            print(f"\n{filepath}:")
            for func in functions:
                print(f"  - {func}")
    else:
        print("✅ All functions have theoretical citations")

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x scripts/verify_theoretical_annotations.py
```

### 4. Create Equation Implementation Audit

Create `scripts/audit_equation_implementations.py`:

```python
#!/usr/bin/env python3
"""
Audit equation coverage from IRH v24.0 manuscript.
"""
from pathlib import Path
import re

# Critical equations from IRH v24.0
CRITICAL_EQUATIONS = {
    "§1.1": "Harmony Functional H[Ψ]",
    "§1.2": "Heat Kernel Expansion (Seeley-DeWitt)",
    "§2.1": "KAM Theory Phase-Locking (Golden Ratio)",
    "§2.2": "Fine-Structure Constant α⁻¹ from Hopf",
    "§2.3": "Neutrino Phase Offset δ_ν = π",
    "§3.1": "Electron VWP with e^(-1/α)",
    "§3.2": "Fermion Mass Hierarchy",
    "§4.1": "Metric Bridge g_μν(x)",
    "§5.1": "Gross-Pitaevskii for Anchor Strand",
}

def find_implementations(src_dir: Path):
    """Find which equations are implemented."""
    implemented = set()
    
    for py_file in src_dir.rglob("*.py"):
        content = py_file.read_text()
        
        for section in CRITICAL_EQUATIONS.keys():
            if section in content:
                implemented.add(section)
    
    return implemented

def main():
    src_dir = Path("src")
    implemented = find_implementations(src_dir)
    
    print("📊 IRH v24.0 Equation Coverage\n")
    print(f"Implemented: {len(implemented)}/{len(CRITICAL_EQUATIONS)}\n")
    
    for section, description in CRITICAL_EQUATIONS.items():
        status = "✅" if section in implemented else "❌"
        print(f"{status} {section}: {description}")

if __name__ == "__main__":
    main()
```

Make executable:
```bash
chmod +x scripts/audit_equation_implementations.py
```

---

## Implementing Core Modules

### 1. Create Module Structure

```bash
# Create source directories
mkdir -p src/{substrate,hopf,emergent_spacetime,particles,dark_matter,observables,logging,utilities}

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;

# Create test directories matching structure
mkdir -p tests/{unit,integration,theoretical_invariants,convergence,benchmarks}
find tests -type d -exec touch {}/__init__.py \;
```

### 2. Implement TransparencyEngine

Create `src/logging/transparency_engine.py`:

```python
"""
Transparency Engine for IRH v24.0

Provides runtime instrumentation for computational transparency.
"""
from enum import IntEnum
from typing import Any, Optional
import json

class VerbosityLevel(IntEnum):
    """Verbosity levels for transparency logging."""
    SILENT = 0
    MINIMAL = 1
    STANDARD = 2
    DETAILED = 3
    FULL = 4

class TransparencyEngine:
    """
    Runtime transparency logger for IRH computations.
    
    Emits step-by-step derivation logs with theoretical references.
    """
    
    def __init__(self, verbosity: VerbosityLevel = VerbosityLevel.STANDARD):
        self.verbosity = verbosity
        self.log = []
    
    def info(self, message: str, reference: Optional[str] = None):
        """Log informational message with optional manuscript reference."""
        if self.verbosity >= VerbosityLevel.STANDARD:
            entry = {"type": "info", "message": message}
            if reference:
                entry["reference"] = reference
            self.log.append(entry)
            self._print(f"[INFO] {message}", reference)
    
    def step(self, description: str, equation: Optional[str] = None):
        """Log a computational step."""
        if self.verbosity >= VerbosityLevel.DETAILED:
            entry = {"type": "step", "description": description}
            if equation:
                entry["equation"] = equation
            self.log.append(entry)
            self._print(f"[STEP] {description}", equation)
    
    def value(self, name: str, value: Any, uncertainty: Optional[float] = None):
        """Log a computed value with uncertainty."""
        if self.verbosity >= VerbosityLevel.DETAILED:
            entry = {"type": "value", "name": name, "value": str(value)}
            if uncertainty:
                entry["uncertainty"] = uncertainty
            self.log.append(entry)
            
            if uncertainty:
                self._print(f"[VALUE] {name} = {value} ± {uncertainty}")
            else:
                self._print(f"[VALUE] {name} = {value}")
    
    def passed(self, check: str):
        """Log a passed validation check."""
        if self.verbosity >= VerbosityLevel.STANDARD:
            self.log.append({"type": "passed", "check": check})
            self._print(f"[✅] {check}")
    
    def failed(self, check: str, reason: Optional[str] = None):
        """Log a failed validation check."""
        entry = {"type": "failed", "check": check}
        if reason:
            entry["reason"] = reason
        self.log.append(entry)
        self._print(f"[❌] {check}", reason)
    
    def _print(self, message: str, detail: Optional[str] = None):
        """Print to console."""
        print(message)
        if detail and self.verbosity >= VerbosityLevel.FULL:
            print(f"     {detail}")
    
    def get_log(self) -> str:
        """Get full log as JSON."""
        return json.dumps(self.log, indent=2)

# Convenience exports
SILENT = VerbosityLevel.SILENT
MINIMAL = VerbosityLevel.MINIMAL
STANDARD = VerbosityLevel.STANDARD
DETAILED = VerbosityLevel.DETAILED
FULL = VerbosityLevel.FULL
```

### 3. Create First Implementation Module

Create `src/substrate/harmony.py`:

```python
"""
Harmony Functional Implementation

Implements §1.1 from IRH v24.0 manuscript.
"""
import numpy as np
from typing import Tuple
from ..logging.transparency_engine import TransparencyEngine, FULL

def compute_harmony_functional(
    psi: np.ndarray,
    planck_mass: float = 1.22e19,  # GeV
    lambda_coupling: float = 1.0,
    lattice_spacing: float = 0.01,
    engine: TransparencyEngine = None
) -> Tuple[float, dict]:
    """
    Compute the Harmony Functional H[Ψ] for substrate field.
    
    Theoretical Reference:
        IRH v24.0, §1.1, Eq. 1
    
    Formula (Complete):
        H[Ψ] = ∫[½|∇Ψ|² + M²/2|Ψ|² + λ|Ψ|⁴] dμ_Haar
        
        where M = M_Pl is the substrate stiffness.
    
    Parameters
    ----------
    psi : np.ndarray
        Complex resonance field on discretized G_inf^4
    planck_mass : float
        Substrate stiffness M_Pl in GeV (default: 1.22×10^19)
    lambda_coupling : float
        Self-interaction coupling λ
    lattice_spacing : float
        Discretization spacing δ
    engine : TransparencyEngine, optional
        Logging engine for transparency
    
    Returns
    -------
    Tuple[float, dict]
        (harmony_value, components_dict)
    
    Notes
    -----
    Discretization error: O(δ²) where δ = lattice_spacing
    """
    if engine is None:
        engine = TransparencyEngine(verbosity=FULL)
    
    engine.info("Computing Harmony Functional H[Ψ]", reference="IRH v24.0 §1.1")
    
    # Kinetic term: ½|∇Ψ|²
    engine.step("Computing kinetic term ½|∇Ψ|²")
    grad_psi = np.gradient(psi)
    kinetic = 0.5 * np.sum([np.abs(g)**2 for g in grad_psi]) * (lattice_spacing ** 4)
    engine.value("kinetic", kinetic)
    
    # Mass term: M²/2|Ψ|²
    engine.step(f"Computing mass term (M²/2)|Ψ|² with M = {planck_mass:.2e} GeV")
    mass_term = 0.5 * (planck_mass ** 2) * np.sum(np.abs(psi)**2) * (lattice_spacing ** 4)
    engine.value("mass_term", mass_term)
    
    # Interaction term: λ|Ψ|⁴
    engine.step("Computing interaction term λ|Ψ|⁴")
    interaction = lambda_coupling * np.sum(np.abs(psi)**4) * (lattice_spacing ** 4)
    engine.value("interaction", interaction)
    
    # Total
    H_total = kinetic + mass_term + interaction
    engine.value("H_total", H_total, uncertainty=H_total * 1e-12)
    engine.passed("Harmony Functional computation complete")
    
    components = {
        "kinetic": kinetic,
        "mass": mass_term,
        "interaction": interaction,
        "total": H_total
    }
    
    return H_total, components
```

---

## Setting Up Testing Infrastructure

### 1. Create First Test

Create `tests/unit/test_substrate/test_harmony.py`:

```python
"""
Unit tests for Harmony Functional (§1.1)
"""
import numpy as np
import pytest
from src.substrate.harmony import compute_harmony_functional

def test_harmony_functional_dimensions():
    """Harmony functional should have correct dimensions."""
    # Create small test field
    psi = np.random.randn(4, 4, 4, 4) + 1j * np.random.randn(4, 4, 4, 4)
    
    H, components = compute_harmony_functional(psi, planck_mass=1e19, lattice_spacing=0.1)
    
    # H should be positive (energy)
    assert H > 0, "Harmony functional must be positive"
    
    # Components should all be positive
    assert components["kinetic"] >= 0
    assert components["mass"] >= 0
    assert components["interaction"] >= 0

def test_harmony_functional_scaling():
    """Harmony should scale correctly with field amplitude."""
    psi_small = np.ones((4, 4, 4, 4), dtype=complex) * 0.1
    psi_large = np.ones((4, 4, 4, 4), dtype=complex) * 1.0
    
    H_small, _ = compute_harmony_functional(psi_small, lattice_spacing=0.1)
    H_large, _ = compute_harmony_functional(psi_large, lattice_spacing=0.1)
    
    # Larger field should have larger harmony
    assert H_large > H_small

def test_harmony_functional_zero_field():
    """Zero field should give zero harmony (up to numerical precision)."""
    psi = np.zeros((4, 4, 4, 4), dtype=complex)
    
    H, _ = compute_harmony_functional(psi, lattice_spacing=0.1)
    
    assert np.isclose(H, 0.0, atol=1e-10)
```

### 2. Run Tests

```bash
# Install pytest if not already
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src --cov-report=term
```

---

## Configuring CI/CD

### 1. Enable GitHub Actions

```bash
# Commit workflows
git add .github/workflows/
git commit -m "Add CI/CD workflows"
git push origin main

# Navigate to GitHub repository
# Go to "Actions" tab
# Workflows should now be visible and active
```

### 2. Test Workflow Execution

```bash
# Make a test change
echo "# Test" >> README.md
git add README.md
git commit -m "Test CI/CD"
git push origin main

# Check Actions tab on GitHub
# compliance_check and irh_validation should run
```

---

## First Implementation Session

### 1. Start with Core Module

```bash
# Create feature branch
git checkout -b feature/implement-hopf-fibration

# Implement Hopf fibration (§2.1-2.2)
# Create src/hopf/fibration.py
# Create tests/unit/test_hopf/test_fibration.py

# Update copilot-instructions.md status
# Add entry to transient session tracking
```

### 2. Use report_progress Pattern

In your copilot instructions session tracking:
```markdown
### Current Session: Implement Hopf Fibration

**Objective:** Derive α⁻¹ from Hopf optimization

**Tasks:**
- [x] Create hopf module structure
- [x] Implement KAM phase-locking
- [ ] Implement Hopf optimization
- [ ] Add comprehensive tests
- [ ] Verify against manuscript §2.2
```

### 3. Follow Development Cycle

1. **Implement** → 2. **Test** → 3. **Audit** → 4. **Commit**

```bash
# After implementing
pytest tests/unit/test_hopf/ -v

# Run compliance check
python scripts/verify_compliance.py

# Commit
git add src/hopf/ tests/unit/test_hopf/
git commit -m "Implement Hopf fibration optimization (§2.1-2.2)"
git push origin feature/implement-hopf-fibration

# Create PR on GitHub
# Workflows will run automatically
```

---

## Troubleshooting

### Workflow Failures

**Problem:** `verify_compliance.py` not found
```bash
# Solution: Create the script (see "Creating Essential Scripts")
python scripts/verify_compliance.py --help
```

**Problem:** Import errors in tests
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH=$PWD
pytest tests/ -v
```

### Citation Compliance

**Problem:** "Missing IRH v24.0 citation" violation
```python
# Wrong:
def compute_something():
    """Compute something."""
    pass

# Right:
def compute_something():
    """
    Compute something from substrate dynamics.
    
    Theoretical Reference:
        IRH v24.0, §X.Y
    """
    pass
```

### Test Coverage

**Problem:** Coverage too low
```bash
# Find uncovered lines
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html in browser
# Identify missing tests
```

---

## Next Steps

1. **Complete Core Modules** (substrate, hopf, emergent_spacetime)
2. **Implement Particle Physics** (VWP, fermion masses)
3. **Add Dark Matter** (anchor strand superfluid)
4. **Validate Against Manuscript** (all 27 constants)
5. **Write Documentation** (API reference, tutorials)
6. **Prepare Publication** (reproducible results, data)

---

**Remember:** Every line of code is a statement about reality. Make it count! 🌟
