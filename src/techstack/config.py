"""
Tech Stack Configuration.

Centralized configuration for Physics-ML library backends and preferences.

References
----------
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - Implementation Priorities
"""

from dataclasses import dataclass, field
from typing import Literal, Optional
from enum import Enum


class GPUBackend(Enum):
    """Available GPU backend options."""
    JAX = "jax"
    CUPY = "cupy"
    NONE = "none"


class QuantumBackend(Enum):
    """Available quantum simulation backend options."""
    QUTIP = "qutip"
    DYNAMIQS = "dynamiqs"
    NUMPY = "numpy"  # Fallback


class PhysicsBackend(Enum):
    """Available physics simulation backend options."""
    PHIFLOW = "phiflow"
    TAICHI = "taichi"
    NUMPY = "numpy"  # Fallback


@dataclass
class TechStackConfig:
    """
    Configuration for IRH tech stack library preferences.
    
    Attributes
    ----------
    gpu_backend : GPUBackend
        Preferred GPU acceleration backend (JAX, CuPy, or None).
    quantum_backend : QuantumBackend
        Preferred quantum simulation backend.
    physics_backend : PhysicsBackend
        Preferred physics simulation backend.
    enable_symbolic : bool
        Whether to use SymPy for symbolic mathematics.
    enable_jax_md : bool
        Whether to use JAX-MD for molecular dynamics.
    enable_modulus : bool
        Whether to use NVIDIA Modulus for neural operators.
    precision : Literal["float32", "float64"]
        Default floating-point precision.
    auto_fallback : bool
        Whether to automatically fall back to NumPy if preferred backend unavailable.
        
    Examples
    --------
    >>> config = TechStackConfig(gpu_backend=GPUBackend.JAX)
    >>> config.enable_gpu()
    True
    """
    
    gpu_backend: GPUBackend = GPUBackend.NONE
    quantum_backend: QuantumBackend = QuantumBackend.NUMPY
    physics_backend: PhysicsBackend = PhysicsBackend.NUMPY
    
    enable_symbolic: bool = True
    enable_jax_md: bool = False
    enable_modulus: bool = False
    
    precision: Literal["float32", "float64"] = "float64"
    auto_fallback: bool = True
    
    # Advanced settings
    jax_enable_x64: bool = True
    taichi_arch: Optional[str] = None  # "cpu", "cuda", "vulkan", etc.
    
    def enable_gpu(self) -> bool:
        """Check if GPU acceleration is enabled."""
        return self.gpu_backend != GPUBackend.NONE
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            "gpu_backend": self.gpu_backend.value,
            "quantum_backend": self.quantum_backend.value,
            "physics_backend": self.physics_backend.value,
            "enable_symbolic": self.enable_symbolic,
            "enable_jax_md": self.enable_jax_md,
            "enable_modulus": self.enable_modulus,
            "precision": self.precision,
            "auto_fallback": self.auto_fallback,
            "jax_enable_x64": self.jax_enable_x64,
            "taichi_arch": self.taichi_arch,
        }
    
    @classmethod
    def default(cls) -> "TechStackConfig":
        """Get default configuration (CPU-only, fallback enabled)."""
        return cls()
    
    @classmethod
    def gpu_optimized(cls) -> "TechStackConfig":
        """Get GPU-optimized configuration."""
        return cls(
            gpu_backend=GPUBackend.JAX,
            quantum_backend=QuantumBackend.DYNAMIQS,
            physics_backend=PhysicsBackend.TAICHI,
            enable_jax_md=True,
            precision="float32",  # Better GPU performance
        )
    
    @classmethod
    def symbolic_analysis(cls) -> "TechStackConfig":
        """Get configuration optimized for symbolic analysis."""
        return cls(
            enable_symbolic=True,
            quantum_backend=QuantumBackend.QUTIP,
            precision="float64",
        )
    
    @classmethod
    def ml_surrogate(cls) -> "TechStackConfig":
        """Get configuration optimized for ML surrogate training."""
        return cls(
            gpu_backend=GPUBackend.JAX,
            enable_modulus=True,
            enable_jax_md=True,
            precision="float32",
        )


# Global configuration instance
_global_config = TechStackConfig.default()


def get_config() -> TechStackConfig:
    """Get global tech stack configuration."""
    return _global_config


def set_config(config: TechStackConfig) -> None:
    """Set global tech stack configuration."""
    global _global_config
    _global_config = config


def configure_jax(config: TechStackConfig) -> None:
    """
    Configure JAX based on tech stack configuration.
    
    Parameters
    ----------
    config : TechStackConfig
        Configuration to apply.
    """
    try:
        import jax
        
        if config.jax_enable_x64:
            jax.config.update("jax_enable_x64", True)
        
        if config.precision == "float64":
            jax.config.update("jax_default_dtype_bits", "64")
        else:
            jax.config.update("jax_default_dtype_bits", "32")
            
    except ImportError:
        pass


def configure_taichi(config: TechStackConfig) -> None:
    """
    Configure Taichi based on tech stack configuration.
    
    Parameters
    ----------
    config : TechStackConfig
        Configuration to apply.
    """
    try:
        import taichi as ti
        
        arch = config.taichi_arch
        if arch is None:
            # Auto-detect
            if config.enable_gpu():
                try:
                    ti.init(arch=ti.cuda)
                except Exception:
                    try:
                        ti.init(arch=ti.vulkan)
                    except Exception:
                        ti.init(arch=ti.cpu)
            else:
                ti.init(arch=ti.cpu)
        else:
            ti.init(arch=getattr(ti, arch))
            
    except ImportError:
        pass


def apply_config(config: TechStackConfig) -> None:
    """
    Apply configuration to all libraries.
    
    Parameters
    ----------
    config : TechStackConfig
        Configuration to apply globally.
    """
    set_config(config)
    configure_jax(config)
    configure_taichi(config)
