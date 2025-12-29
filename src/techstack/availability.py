"""
Tech Stack Availability Checker.

Checks which optional Physics-ML libraries are available in the current environment.

References
----------
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Integrated Library Stack
"""

from typing import Dict, List, Optional
import importlib.util
from dataclasses import dataclass


@dataclass
class LibraryStatus:
    """Status information for a tech stack library."""
    
    name: str
    available: bool
    version: Optional[str] = None
    import_name: str = ""
    description: str = ""
    
    def __repr__(self) -> str:
        status = "✓" if self.available else "✗"
        version_str = f" v{self.version}" if self.version else ""
        return f"{status} {self.name}{version_str}: {self.description}"


def _check_library(import_name: str, display_name: str, description: str) -> LibraryStatus:
    """Check if a library is available and get its version."""
    spec = importlib.util.find_spec(import_name)
    available = spec is not None
    
    version = None
    if available:
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, "__version__", None)
        except Exception:
            pass
    
    return LibraryStatus(
        name=display_name,
        available=available,
        version=version,
        import_name=import_name,
        description=description
    )


def check_available_libraries() -> Dict[str, LibraryStatus]:
    """
    Check availability of all IRH tech stack libraries.
    
    Returns
    -------
    Dict[str, LibraryStatus]
        Dictionary mapping library names to their availability status.
        
    Examples
    --------
    >>> status = check_available_libraries()
    >>> if status["jax"].available:
    ...     print("JAX is available")
    """
    libraries = {
        # Core JAX stack
        "jax": _check_library("jax", "JAX", "Automatic differentiation and GPU acceleration"),
        "jaxlib": _check_library("jaxlib", "JAXlib", "JAX backend library"),
        
        # Physics-ML libraries
        "jax_md": _check_library("jax_md", "JAX-MD", "Molecular dynamics with JAX"),
        "modulus": _check_library("modulus", "NVIDIA Modulus", "Physics-ML framework"),
        "qutip": _check_library("qutip", "QuTiP", "Quantum toolbox in Python"),
        "dynamiqs": _check_library("dynamiqs", "Dynamiqs", "JAX-based GPU quantum simulation"),
        "sympy": _check_library("sympy", "SymPy", "Symbolic mathematics"),
        "phiflow": _check_library("phi", "PhiFlow", "Differentiable physics simulations"),
        "taichi": _check_library("taichi", "Taichi", "High-performance parallel computing"),
        
        # GPU acceleration
        "cupy": _check_library("cupy", "CuPy", "NumPy-compatible GPU arrays"),
        
        # Core dependencies (should always be available)
        "numpy": _check_library("numpy", "NumPy", "Numerical computing"),
        "scipy": _check_library("scipy", "SciPy", "Scientific computing"),
    }
    
    return libraries


def get_tech_stack_status() -> str:
    """
    Get a formatted string showing tech stack availability.
    
    Returns
    -------
    str
        Multi-line string showing library availability status.
        
    Examples
    --------
    >>> print(get_tech_stack_status())
    IRH Tech Stack Status:
    ======================
    ✓ NumPy v1.24.0: Numerical computing
    ✓ SciPy v1.10.0: Scientific computing
    ...
    """
    libs = check_available_libraries()
    
    lines = ["IRH Tech Stack Status:", "=" * 50]
    
    # Core libraries
    lines.append("\nCore Libraries:")
    lines.append("-" * 50)
    for key in ["numpy", "scipy", "sympy"]:
        if key in libs:
            lines.append(f"  {libs[key]}")
    
    # JAX stack
    lines.append("\nJAX Ecosystem:")
    lines.append("-" * 50)
    for key in ["jax", "jaxlib", "jax_md"]:
        if key in libs:
            lines.append(f"  {libs[key]}")
    
    # Quantum libraries
    lines.append("\nQuantum Libraries:")
    lines.append("-" * 50)
    for key in ["qutip", "dynamiqs"]:
        if key in libs:
            lines.append(f"  {libs[key]}")
    
    # Physics-ML
    lines.append("\nPhysics-ML Libraries:")
    lines.append("-" * 50)
    for key in ["modulus", "phiflow", "taichi"]:
        if key in libs:
            lines.append(f"  {libs[key]}")
    
    # GPU acceleration
    lines.append("\nGPU Acceleration:")
    lines.append("-" * 50)
    if "cupy" in libs:
        lines.append(f"  {libs['cupy']}")
    
    # Summary
    available = sum(1 for lib in libs.values() if lib.available)
    total = len(libs)
    lines.append("\n" + "=" * 50)
    lines.append(f"Available: {available}/{total} libraries")
    
    return "\n".join(lines)


def get_required_libraries() -> List[str]:
    """
    Get list of libraries required for core IRH functionality.
    
    Returns
    -------
    List[str]
        List of required library import names.
    """
    return ["numpy", "scipy", "sympy"]


def get_optional_libraries() -> List[str]:
    """
    Get list of optional Physics-ML enhancement libraries.
    
    Returns
    -------
    List[str]
        List of optional library import names.
    """
    return [
        "jax", "jaxlib", "jax_md",
        "qutip", "dynamiqs",
        "modulus", "phi", "taichi",
        "cupy"
    ]


def check_gpu_available() -> bool:
    """
    Check if GPU acceleration is available (JAX or CuPy).
    
    Returns
    -------
    bool
        True if either JAX with GPU or CuPy is available.
    """
    libs = check_available_libraries()
    
    # Check CuPy
    if libs.get("cupy", LibraryStatus("", False)).available:
        return True
    
    # Check JAX with GPU
    if libs.get("jax", LibraryStatus("", False)).available:
        try:
            import jax
            devices = jax.devices()
            return any(d.platform == "gpu" for d in devices)
        except Exception:
            pass
    
    return False
