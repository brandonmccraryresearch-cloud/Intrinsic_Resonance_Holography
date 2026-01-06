# IRH Plugin System Design (Phase 4.6)

**Status**: 📋 DESIGN PHASE  
**Target**: Q3 2026  
**Priority**: LOW  
**Complexity**: Medium-High

---

## Executive Summary

The IRH Plugin System will enable third-party developers to extend the framework with custom physics modules, analysis tools, and experimental data adapters without modifying the core codebase. This document specifies the design, API, security model, and implementation roadmap.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Design Goals](#2-design-goals)
3. [Architecture Overview](#3-architecture-overview)
4. [Plugin API Specification](#4-plugin-api-specification)
5. [Security Model](#5-security-model)
6. [Plugin Discovery & Loading](#6-plugin-discovery--loading)
7. [Plugin Categories](#7-plugin-categories)
8. [Implementation Roadmap](#8-implementation-roadmap)
9. [Example Plugins](#9-example-plugins)

---

## 1. Motivation

### Current Limitations

The IRH framework is comprehensive but cannot anticipate all research needs:
- Custom observables for specific experiments
- Alternative compression algorithms for QNCD
- Specialized visualization for particular research questions
- Integration with experimental collaboration frameworks (ATLAS, CMS, etc.)
- Custom export formats for different publication venues

### Plugin System Benefits

1. **Extensibility**: Add new features without core modifications
2. **Community Contributions**: Lower barrier to community development
3. **Experimentation**: Test new ideas without risking core stability
4. **Specialization**: Domain-specific tools for subfields (cosmology, particle physics, quantum gravity)
5. **Rapid Prototyping**: Iterate quickly on research ideas

---

## 2. Design Goals

### Functional Goals

- [ ] **Easy Discovery**: Plugins auto-discovered from standard locations
- [ ] **Simple API**: Minimal boilerplate, inherit from base classes
- [ ] **Type Safety**: Full type hints, runtime validation
- [ ] **Documentation**: Auto-generate plugin documentation
- [ ] **Versioning**: Plugin compatibility with IRH versions
- [ ] **Dependencies**: Manage plugin-specific dependencies

### Non-Functional Goals

- [ ] **Security**: Sandboxed execution, permission model
- [ ] **Performance**: Minimal overhead for core operations
- [ ] **Stability**: Core remains stable if plugins fail
- [ ] **Testability**: Plugin testing framework included
- [ ] **Distribution**: PyPI-compatible plugin packages

---

## 3. Architecture Overview

### Component Structure

```
irh-framework/
├── src/irh/
│   ├── plugins/
│   │   ├── __init__.py          # Plugin system core
│   │   ├── base.py              # Base plugin classes
│   │   ├── loader.py            # Plugin discovery & loading
│   │   ├── registry.py          # Plugin registration
│   │   ├── security.py          # Security sandbox
│   │   └── api.py               # Public plugin API
│   └── ...
└── plugins/                     # Standard plugin location
    ├── experimental_adapters/
    ├── custom_visualizations/
    └── analysis_tools/
```

### Plugin Lifecycle

```
Discovery → Validation → Loading → Initialization → Registration → Execution → Cleanup
```

1. **Discovery**: Scan standard plugin locations
2. **Validation**: Check version compatibility, signatures
3. **Loading**: Import plugin module
4. **Initialization**: Call plugin `setup()` method
5. **Registration**: Add to plugin registry
6. **Execution**: User calls plugin methods
7. **Cleanup**: Call plugin `teardown()` on exit

---

## 4. Plugin API Specification

### Base Plugin Class

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from irh.plugins.base import IRHPlugin, PluginMetadata

class CustomObservablePlugin(IRHPlugin):
    """
    Base class for custom observable plugins.
    
    All plugins must inherit from IRHPlugin or a specific subclass
    and implement required abstract methods.
    """
    
    # Plugin metadata (required)
    metadata = PluginMetadata(
        name="custom-observable",
        version="1.0.0",
        author="Research Group",
        description="Computes custom observable from cGFT condensate",
        irh_version_min="21.0.0",
        irh_version_max="22.0.0",
        dependencies=["numpy>=1.24", "scipy>=1.11"],
        license="MIT",
        url="https://github.com/group/irh-custom-observable",
    )
    
    @abstractmethod
    def compute(self, condensate: Any, **kwargs) -> Dict[str, Any]:
        """
        Compute the custom observable.
        
        Parameters
        ----------
        condensate : CondensateState
            The cGFT condensate state
        **kwargs : dict
            Additional computation parameters
            
        Returns
        -------
        dict
            Results with keys: 'value', 'uncertainty', 'metadata'
        """
        pass
    
    def setup(self) -> None:
        """Initialize plugin (optional override)."""
        pass
    
    def teardown(self) -> None:
        """Cleanup plugin resources (optional override)."""
        pass
    
    def validate_input(self, condensate: Any) -> bool:
        """Validate input data (optional override)."""
        return True
```

### Plugin Categories

```python
# Observable Plugin
class IRHObservablePlugin(IRHPlugin):
    """Plugin for computing custom observables."""
    category = "observable"
    
# Visualization Plugin
class IRHVisualizationPlugin(IRHPlugin):
    """Plugin for custom visualizations."""
    category = "visualization"
    
# Data Adapter Plugin
class IRHDataAdapterPlugin(IRHPlugin):
    """Plugin for experimental data adapters."""
    category="data_adapter"
    
# Analysis Tool Plugin
class IRHAnalysisPlugin(IRHPlugin):
    """Plugin for custom analysis tools."""
    category = "analysis"
    
# Compression Algorithm Plugin
class IRHCompressionPlugin(IRHPlugin):
    """Plugin for alternative QNCD compression algorithms."""
    category = "compression"
```

---

## 5. Security Model

### Permission System

Plugins operate in different trust levels:

| Level | Permissions | Use Case |
|-------|-------------|----------|
| **SAFE** | Read IRH data, compute, visualize | Community plugins, untrusted code |
| **TRUSTED** | Write to disk, network access | Experimental data fetching, export |
| **CORE** | Modify IRH internals | Official plugins only |

### Sandboxing

```python
from irh.plugins.security import PluginSandbox, PermissionLevel

# Safe plugins run in restricted environment
sandbox = PluginSandbox(level=PermissionLevel.SAFE)
with sandbox:
    result = plugin.compute(condensate)
```

Restricted operations for SAFE plugins:
- ❌ File I/O (except temp directory)
- ❌ Network access
- ❌ System calls
- ❌ IRH core modification
- ✅ NumPy/SciPy computations
- ✅ Matplotlib plotting (in-memory)

### Code Signing (Future)

```python
# Verify plugin signature before loading
from irh.plugins.security import verify_plugin_signature

if verify_plugin_signature(plugin_path, public_key):
    plugin = load_plugin(plugin_path)
```

---

## 6. Plugin Discovery & Loading

### Standard Plugin Locations

1. **System-wide**: `/usr/share/irh/plugins/`
2. **User-local**: `~/.irh/plugins/`
3. **Virtual env**: `$VIRTUAL_ENV/share/irh/plugins/`
4. **Project-specific**: `./plugins/`
5. **Environment variable**: `$IRH_PLUGIN_PATH`

### Discovery Process

```python
from irh.plugins import discover_plugins, load_plugin

# Auto-discover all plugins
plugins = discover_plugins()

# Load specific plugin
custom_obs = load_plugin("custom-observable")

# Use plugin
result = custom_obs.compute(condensate)
```

### Plugin Manifest

Each plugin directory must contain `plugin.yaml`:

```yaml
name: custom-observable
version: 1.0.0
author: Research Group
description: Custom observable computation
entry_point: custom_observable.main:CustomObservablePlugin
irh_version:
  min: 21.0.0
  max: 22.0.0
dependencies:
  - numpy>=1.24
  - scipy>=1.11
permissions:
  level: SAFE
license: MIT
url: https://github.com/group/irh-custom-observable
```

---

## 7. Plugin Categories

### 7.1 Observable Plugins

Compute custom observables from condensate state.

**Example**: Higgs trilinear coupling λ_HHH (§3.3.3)

```python
class HiggsTrilinearPlugin(IRHObservablePlugin):
    metadata = PluginMetadata(
        name="higgs-trilinear",
        description="Compute Higgs trilinear coupling from fixed point",
    )
    
    def compute(self, fixed_point, **kwargs):
        """Compute λ_HHH = 3m_H²/v* (Eq. 3.9)."""
        m_H = 125.0  # GeV
        v = 246.22   # GeV
        lambda_HHH = 3 * m_H**2 / v
        return {
            "value": lambda_HHH,
            "uncertainty": 0.5,  # GeV
            "unit": "GeV",
            "reference": "IRH v21.4 §3.3.3, Eq. 3.9"
        }
```

### 7.2 Visualization Plugins

Custom visualizations beyond core framework.

**Example**: VWP field configuration renderer

```python
class VWPVisualizationPlugin(IRHVisualizationPlugin):
    def render(self, vwp_state, **kwargs):
        """Render VWP topological configuration."""
        import matplotlib.pyplot as plt
        # Custom visualization code
        return fig
```

### 7.3 Data Adapter Plugins

Interface with experimental databases.

**Example**: ATLAS collaboration data adapter

```python
class ATLASDataAdapterPlugin(IRHDataAdapterPlugin):
    permissions_required = PermissionLevel.TRUSTED  # Network access
    
    def fetch_latest_higgs_mass(self):
        """Fetch latest Higgs mass measurement from ATLAS."""
        # API call to ATLAS public data
        return ExperimentalValue(...)
```

### 7.4 Analysis Plugins

Custom analysis workflows.

**Example**: Parameter sensitivity scanner

```python
class SensitivityScannerPlugin(IRHAnalysisPlugin):
    def scan_parameter_space(self, param_ranges, observable):
        """Scan parameter space for observable sensitivity."""
        results = []
        for params in param_ranges:
            value = observable.compute(params)
            results.append((params, value))
        return results
```

### 7.5 Compression Plugins

Alternative QNCD compression algorithms.

**Example**: LZMA compression for QNCD

```python
class LZMACompressionPlugin(IRHCompressionPlugin):
    def compress(self, data: bytes) -> bytes:
        """LZMA compression (alternative to zlib)."""
        import lzma
        return lzma.compress(data)
    
    def verify_qucc_compliance(self) -> bool:
        """Verify QUCC-Theorem compliance (Appendix A.4)."""
        # Test compressor-independence
        return True
```

---

## 8. Implementation Roadmap

### Phase 1: Foundation (4 weeks)

- [ ] Implement base plugin classes
- [ ] Create plugin discovery system
- [ ] Build plugin registry
- [ ] Add basic validation
- [ ] Write developer documentation

### Phase 2: Security (3 weeks)

- [ ] Implement sandboxing for SAFE level
- [ ] Add permission checking
- [ ] Create security audit tools
- [ ] Write security guidelines

### Phase 3: Standard Plugins (4 weeks)

- [ ] Implement 5 example plugins (one per category)
- [ ] Package as separate pip installable packages
- [ ] Write plugin development tutorial
- [ ] Create plugin template repository

### Phase 4: Distribution (3 weeks)

- [ ] Set up plugin registry website
- [ ] Create PyPI naming convention (irh-plugin-*)
- [ ] Build plugin discovery service
- [ ] Add plugin rating system

### Phase 5: Advanced Features (4 weeks)

- [ ] Add plugin dependency resolution
- [ ] Implement plugin update mechanism
- [ ] Create plugin testing framework
- [ ] Add plugin performance profiling

---

## 9. Example Plugins

### Example 1: Custom Observable

**Repository**: `irh-plugin-custom-observable`

Computes a custom observable (e.g., specific correlation function).

### Example 2: GW Sideband Detector

**Repository**: `irh-plugin-gw-sidebands`

Computes gravitational wave sideband structure (Appendix J.2).

### Example 3: PDG Live Adapter

**Repository**: `irh-plugin-pdg-live`

Fetches latest particle data from PDG in real-time.

### Example 4: Publication Figure Generator

**Repository**: `irh-plugin-pub-figures`

Generates publication-quality figures matching journal requirements.

### Example 5: CODATA Updater

**Repository**: `irh-plugin-codata-sync`

Automatically syncs with latest CODATA release.

---

## Appendix A: Plugin Development Quickstart

### Step 1: Install IRH Plugin SDK

```bash
pip install irh-framework
pip install irh-plugin-sdk  # Development tools
```

### Step 2: Create Plugin from Template

```bash
irh-plugin create my-observable
cd irh-plugin-my-observable
```

Generated structure:
```
irh-plugin-my-observable/
├── pyproject.toml
├── README.md
├── src/
│   └── irh_plugin_my_observable/
│       ├── __init__.py
│       └── plugin.py
├── tests/
│   └── test_plugin.py
└── plugin.yaml
```

### Step 3: Implement Plugin

Edit `src/irh_plugin_my_observable/plugin.py`:

```python
from irh.plugins import IRHObservablePlugin, PluginMetadata

class MyObservablePlugin(IRHObservablePlugin):
    metadata = PluginMetadata(
        name="my-observable",
        version="0.1.0",
        # ... fill in metadata
    )
    
    def compute(self, condensate, **kwargs):
        # Your computation here
        return {"value": result, "uncertainty": error}
```

### Step 4: Test Plugin

```bash
pytest tests/
irh-plugin test  # Run IRH plugin test suite
```

### Step 5: Package and Distribute

```bash
python -m build
twine upload dist/*
```

### Step 6: Use Plugin

```python
from irh.plugins import load_plugin

my_obs = load_plugin("my-observable")
result = my_obs.compute(condensate)
```

---

## Appendix B: Plugin Metadata Specification

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | str | Unique plugin name (kebab-case) |
| `version` | str | Semantic version (MAJOR.MINOR.PATCH) |
| `author` | str | Author name or organization |
| `description` | str | One-line description (< 80 chars) |
| `irh_version_min` | str | Minimum IRH version |
| `irh_version_max` | str | Maximum IRH version |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `dependencies` | List[str] | Python package dependencies |
| `license` | str | License identifier (SPDX) |
| `url` | str | Plugin homepage/repository URL |
| `keywords` | List[str] | Search keywords |
| `category` | str | Plugin category |
| `permissions` | Dict | Required permissions |

---

## Appendix C: Security Best Practices

### For Plugin Developers

1. **Minimize Permissions**: Request only necessary permission level
2. **Validate Inputs**: Check all user inputs thoroughly
3. **Handle Errors**: Catch exceptions, don't crash IRH
4. **Document Side Effects**: Clearly document any I/O operations
5. **Version Dependencies**: Pin dependency versions

### For Plugin Users

1. **Verify Source**: Only install plugins from trusted sources
2. **Check Permissions**: Review permission requests before installing
3. **Read Reviews**: Check plugin ratings and reviews
4. **Update Regularly**: Keep plugins updated for security patches
5. **Report Issues**: Report suspicious behavior immediately

---

**Last Updated**: December 30, 2025  
**Next Review**: Q1 2026  
**Status**: DESIGN PHASE - Ready for Implementation
