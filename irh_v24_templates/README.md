# IRH v24.0 Repository Template Package

This package contains the core policies, workflows, and configuration files for building a new IRH v24.0 computational repository. These templates are adapted from the IRH v21.4 repository, with all repository-specific content removed and updated for the IRH v24.0 manuscript.

## 📦 Package Contents

```
irh_v24_templates/
├── README.md (this file)
├── MIGRATION_GUIDE.md
├── github/
│   ├── copilot-instructions.md          # Main copilot instructions
│   ├── GITHUB_COPILOT_AGENT_IRH_v24.md  # Specialized AI assistant config
│   ├── dependabot.yml                    # Dependency management
│   ├── pull_request_template.md         # PR template
│   └── workflows/
│       ├── compliance_check.yml          # Theoretical compliance checks
│       ├── irh_validation.yml            # Standard validation workflow
│       └── nightly_comprehensive.yml     # Comprehensive nightly tests
```

## 🎯 What's Included

### 1. Copilot Instructions (`copilot-instructions.md`)
The single source of truth for repository development, containing:
- **Mandatory Documentation Policy** - Single source of truth mandate
- **Computational Verification Protocol** - Isomorphic implementation requirements
- **Theoretical Foundation** - IRH v24.0 core concepts
- **Coding Standards** - Python style guide, naming conventions, docstring format
- **Testing Guidelines** - Test structure and best practices
- **Repository Maintenance** - Organization and cleanup protocols
- **Mandatory Audit Protocol** - Pre-merge audit requirements
- **Theoretical Correspondence Mandate** - Zero-tolerance policy for approximations
- **Transient Session Tracking** - Active development session management

### 2. GitHub Copilot Agent (`GITHUB_COPILOT_AGENT_IRH_v24.md`)
Specialized AI assistant configuration for IRH v24.0, including:
- IRH v24.0 theoretical foundation
- Integrated library stack (NumPy, SymPy, JAX, etc.)
- Code architecture patterns (Hopf fibration, substrate field, etc.)
- Implementation priorities
- Example interactions

### 3. Workflows
Three CI/CD workflows for automated validation:

#### `compliance_check.yml`
Runs on every PR and push to verify:
- Theoretical correspondence compliance
- No hardcoded constants without derivation
- Manuscript citations present
- Documentation sync

#### `irh_validation.yml`
Standard validation workflow:
- Unit tests across Python 3.10, 3.11, 3.12
- Test coverage reporting
- Linting (black, flake8, isort)
- Theoretical annotation verification

#### `nightly_comprehensive.yml`
Extensive nightly testing:
- Full test suite with long-running convergence studies
- Performance benchmarks
- Dimensional consistency checks
- Mathematical identity verification

### 4. Pull Request Template
Comprehensive PR checklist enforcing:
- Theoretical correspondence compliance
- Formula completeness
- Transparency engine integration
- Testing requirements
- Documentation updates
- Rejection criteria

## 🚀 Quick Start

### Step 1: Create Your New Repository
```bash
# Create new repository on GitHub
# Clone it locally
git clone https://github.com/YOUR-ORG/YOUR-IRH-V24-REPO.git
cd YOUR-IRH-V24-REPO
```

### Step 2: Copy Templates
```bash
# Copy all templates to your repository
cp -r /path/to/irh_v24_templates/github/ .github/

# Copy the manuscript (ensure you have IRH_v24_Final_Manuscript.md)
cp /path/to/IRH_v24_Final_Manuscript.md .
```

### Step 3: Customize for Your Repository
```bash
# Update repository-specific references in workflows
# Replace [YOUR-ORG]/[YOUR-REPO-NAME] with your actual repo details
sed -i 's/\[YOUR-ORG\]\/\[YOUR-REPO-NAME\]/your-org\/your-repo/g' .github/GITHUB_COPILOT_AGENT_IRH_v24.md
```

### Step 4: Initialize Project Structure
```bash
# Create basic directory structure
mkdir -p src/{substrate,hopf,emergent_spacetime,particles,dark_matter,observables,logging}
mkdir -p tests/{unit,integration,theoretical_invariants,convergence,benchmarks}
mkdir -p docs/{manuscripts,api_reference}
mkdir -p scripts

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;
```

### Step 5: Create Essential Files
```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
numpy>=1.24.0
scipy>=1.11.0
sympy>=1.12
mpmath>=1.3.0
pytest>=7.4.0
pytest-cov>=4.1.0
black>=23.0.0
mypy>=1.5.0
ruff>=0.0.285
EOF

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "irh-v24"
version = "0.1.0"
description = "IRH v24.0: The Mathematically Complete Vibrational Unification"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24.0",
    "scipy>=1.11.0",
    "sympy>=1.12",
    "mpmath>=1.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "mypy>=1.5.0",
    "ruff>=0.0.285",
]
physics-ml = [
    "jax[cpu]>=0.4.13",
    "qutip>=4.7.0",
]

[tool.black]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --strict-markers"
EOF
```

### Step 6: Create Initial Scripts
See `MIGRATION_GUIDE.md` for details on creating compliance scripts.

### Step 7: First Commit
```bash
git add .
git commit -m "Initial repository setup with IRH v24.0 templates"
git push origin main
```

## 📋 What You Need to Implement

The templates provide the framework, but you need to implement:

### 1. Core Modules (in `src/`)
- `substrate/` - Harmony Functional, IRS dynamics
- `hopf/` - Hopf fibration, golden ratio derivation, α calculation
- `emergent_spacetime/` - Metric bridge, heat kernel expansion
- `particles/` - VWP construction, fermion masses with e^(-1/α)
- `dark_matter/` - Anchor strand superfluid, Gross-Pitaevskii
- `observables/` - Physical constant predictions
- `logging/` - TransparencyEngine for computational transparency

### 2. Test Suite (in `tests/`)
- Unit tests for each module
- Integration tests for derivation chains
- Theoretical invariant tests (mathematical properties)
- Convergence studies
- Performance benchmarks

### 3. Validation Scripts (in `scripts/`)
- `verify_compliance.py` - Compliance checking
- `verify_theoretical_annotations.py` - Citation verification
- `audit_equation_implementations.py` - Equation coverage
- `check_dimensional_consistency.py` - Unit checking
- `verify_mathematical_identities.py` - Identity validation

### 4. Documentation (in `docs/`)
- `ARCHITECTURE.md` - System architecture
- `TECHNICAL_REFERENCE.md` - API documentation
- `ROADMAP.md` - Implementation roadmap
- `QUICKSTART.md` - Getting started guide

## 🔧 Customization Points

### Workflow Customization
Edit `.github/workflows/*.yml` to:
- Adjust Python versions
- Add/remove testing stages
- Configure notification settings
- Add deployment steps

### Copilot Instructions Customization
Edit `.github/copilot-instructions.md` to:
- Update implementation status in "Current Repository Status"
- Add new modules to repository structure
- Update phase tracking in transient sections
- Add project-specific conventions

### Agent Configuration Customization
Edit `.github/GITHUB_COPILOT_AGENT_IRH_v24.md` to:
- Add repository-specific context
- Update example interactions
- Add custom library integrations
- Specify deployment targets

## 📚 Key Concepts from IRH v24.0

### Zero Free Parameters Philosophy
- Single dimensional input: M_Pl = 1.22 × 10^19 GeV
- Everything else derived from G_inf^4 topology
- 27:1 explanatory leverage ratio

### Critical Derivation Chain
```
M_Pl (input)
  ↓
16D Substrate G_inf^4 = [SU(2) × U(1)_φ]^4
  ↓
Hopf Fibration S³ → S²
  ↓
KAM Phase-Locking → φ = (1+√5)/2
  ↓
Optimization → α⁻¹ = 137.036
  ↓
VWP + e^(-1/α) → Fermion masses
  ↓
Heat Kernel → Einstein-Hilbert
```

### Key Differences from v21.4
- **v21.4**: Quaternionic cGFT with RG flow
- **v24.0**: Deterministic Hyperdimensional Wave Dynamics (DHWD)
- **v21.4**: Multiple versions (v16, v18, v21)
- **v24.0**: Single unified framework
- **v21.4**: Spectral dimension flow
- **v24.0**: Heat kernel expansion
- **v21.4**: β₁ = 12, n_inst = 3
- **v24.0**: Hopf topology, linking number = 1

## ⚠️ Important Notes

### Mandatory Compliance
All code MUST:
1. Cite IRH v24.0 manuscript sections
2. Use complete formulas (no oversimplifications)
3. Emit transparency logs
4. Include uncertainty quantification
5. Pass pre-merge audit

### Workflow Requirements
- All workflows require Python 3.10+
- Some scripts may need additional dependencies
- Workflows assume specific script locations

### Documentation Sync
Changes to code must trigger updates to:
- `.github/copilot-instructions.md`
- `README.md`
- `docs/TECHNICAL_REFERENCE.md`

## 🆘 Support

For questions about:
- **Template usage**: See `MIGRATION_GUIDE.md`
- **IRH v24.0 theory**: Read `IRH_v24_Final_Manuscript.md`
- **Compliance requirements**: See `.github/copilot-instructions.md`

## 📄 License

These templates are provided as-is for building IRH v24.0 computational repositories.
Ensure your repository includes appropriate license for your code.

## 🙏 Attribution

Templates adapted from the IRH v21.4 repository:
- Original repository: `brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography`
- Adapted for IRH v24.0: January 2026

---

**Ready to build the computational engine of vibrational unification? Let's begin! 🚀**
