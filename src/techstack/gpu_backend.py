"""
Unified GPU Backend Abstraction.

Provides a single interface that works with JAX, CuPy, or falls back to NumPy.

References
----------
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - GPU acceleration patterns
"""

from typing import Optional
import numpy as np
from enum import Enum

# Try importing GPU libraries
try:
    import jax
    import jax.numpy as jnp
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
    jnp = np

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    cp = np


class GPUBackendType(Enum):
    """Available GPU backend types."""
    JAX = "jax"
    CUPY = "cupy"
    NUMPY = "numpy"


class GPUArray:
    """
    Unified GPU array wrapper.
    
    Automatically uses best available backend (JAX > CuPy > NumPy).
    
    Examples
    --------
    >>> arr = GPUArray.zeros((100, 100))
    >>> print(arr.backend)  # 'jax', 'cupy', or 'numpy'
    >>> result = arr.sum()
    """
    
    def __init__(self, data: np.ndarray, backend: Optional[GPUBackendType] = None):
        """
        Initialize GPU array.
        
        Parameters
        ----------
        data : array-like
            Input data.
        backend : GPUBackendType, optional
            Force specific backend. If None, auto-select best available.
        """
        if backend is None:
            # Auto-select best backend
            if JAX_AVAILABLE:
                self.backend = GPUBackendType.JAX
                self._data = jnp.array(data)
            elif CUPY_AVAILABLE:
                self.backend = GPUBackendType.CUPY
                self._data = cp.array(data)
            else:
                self.backend = GPUBackendType.NUMPY
                self._data = np.array(data)
        else:
            self.backend = backend
            if backend == GPUBackendType.JAX and JAX_AVAILABLE:
                self._data = jnp.array(data)
            elif backend == GPUBackendType.CUPY and CUPY_AVAILABLE:
                self._data = cp.array(data)
            else:
                self._data = np.array(data)
                self.backend = GPUBackendType.NUMPY
    
    @property
    def data(self):
        """Get underlying array data."""
        return self._data
    
    def to_numpy(self) -> np.ndarray:
        """Convert to NumPy array."""
        if self.backend == GPUBackendType.JAX:
            return np.array(self._data)
        elif self.backend == GPUBackendType.CUPY:
            return cp.asnumpy(self._data)
        else:
            return self._data
    
    @classmethod
    def zeros(cls, shape: tuple, backend: Optional[GPUBackendType] = None):
        """Create array of zeros."""
        if backend is None:
            if JAX_AVAILABLE:
                backend = GPUBackendType.JAX
            elif CUPY_AVAILABLE:
                backend = GPUBackendType.CUPY
            else:
                backend = GPUBackendType.NUMPY
        
        if backend == GPUBackendType.JAX and JAX_AVAILABLE:
            data = jnp.zeros(shape)
        elif backend == GPUBackendType.CUPY and CUPY_AVAILABLE:
            data = cp.zeros(shape)
        else:
            data = np.zeros(shape)
            backend = GPUBackendType.NUMPY
        
        return cls(data, backend=backend)
    
    @classmethod
    def ones(cls, shape: tuple, backend: Optional[GPUBackendType] = None):
        """Create array of ones."""
        if backend is None:
            if JAX_AVAILABLE:
                backend = GPUBackendType.JAX
            elif CUPY_AVAILABLE:
                backend = GPUBackendType.CUPY
            else:
                backend = GPUBackendType.NUMPY
        
        if backend == GPUBackendType.JAX and JAX_AVAILABLE:
            data = jnp.ones(shape)
        elif backend == GPUBackendType.CUPY and CUPY_AVAILABLE:
            data = cp.ones(shape)
        else:
            data = np.ones(shape)
            backend = GPUBackendType.NUMPY
        
        return cls(data, backend=backend)
    
    def __repr__(self) -> str:
        return f"GPUArray(backend={self.backend.value}, shape={self._data.shape}, dtype={self._data.dtype})"


class GPUBackend:
    """
    Unified GPU backend interface.
    
    Provides consistent API across JAX, CuPy, and NumPy.
    
    Examples
    --------
    >>> backend = GPUBackend()
    >>> print(backend.name)  # 'jax', 'cupy', or 'numpy'
    >>> arr = backend.zeros((100, 100))
    >>> result = backend.matmul(arr, arr)
    """
    
    def __init__(self, prefer: Optional[GPUBackendType] = None):
        """
        Initialize GPU backend.
        
        Parameters
        ----------
        prefer : GPUBackendType, optional
            Preferred backend. If None or unavailable, auto-select.
        """
        if prefer == GPUBackendType.JAX and JAX_AVAILABLE:
            self.backend_type = GPUBackendType.JAX
            self._module = jnp
        elif prefer == GPUBackendType.CUPY and CUPY_AVAILABLE:
            self.backend_type = GPUBackendType.CUPY
            self._module = cp
        else:
            # Auto-select or fallback
            if JAX_AVAILABLE:
                self.backend_type = GPUBackendType.JAX
                self._module = jnp
            elif CUPY_AVAILABLE:
                self.backend_type = GPUBackendType.CUPY
                self._module = cp
            else:
                self.backend_type = GPUBackendType.NUMPY
                self._module = np
    
    @property
    def name(self) -> str:
        """Get backend name."""
        return self.backend_type.value
    
    @property
    def is_gpu(self) -> bool:
        """Check if using GPU acceleration."""
        return self.backend_type in [GPUBackendType.JAX, GPUBackendType.CUPY]
    
    def zeros(self, shape: tuple, dtype=None) -> np.ndarray:
        """Create array of zeros."""
        return self._module.zeros(shape, dtype=dtype)
    
    def ones(self, shape: tuple, dtype=None) -> np.ndarray:
        """Create array of ones."""
        return self._module.ones(shape, dtype=dtype)
    
    def array(self, data, dtype=None) -> np.ndarray:
        """Create array from data."""
        return self._module.array(data, dtype=dtype)
    
    def matmul(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Matrix multiplication."""
        return self._module.matmul(a, b)
    
    def dot(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """Dot product."""
        return self._module.dot(a, b)
    
    def exp(self, x: np.ndarray) -> np.ndarray:
        """Element-wise exponential."""
        return self._module.exp(x)
    
    def sin(self, x: np.ndarray) -> np.ndarray:
        """Element-wise sine."""
        return self._module.sin(x)
    
    def cos(self, x: np.ndarray) -> np.ndarray:
        """Element-wise cosine."""
        return self._module.cos(x)
    
    def fft(self, x: np.ndarray) -> np.ndarray:
        """Fast Fourier Transform."""
        if self.backend_type == GPUBackendType.JAX:
            return jnp.fft.fft(x)
        elif self.backend_type == GPUBackendType.CUPY:
            return cp.fft.fft(x)
        else:
            return np.fft.fft(x)
    
    def to_numpy(self, x: np.ndarray) -> np.ndarray:
        """Convert to NumPy array."""
        if self.backend_type == GPUBackendType.JAX:
            return np.array(x)
        elif self.backend_type == GPUBackendType.CUPY:
            return cp.asnumpy(x)
        else:
            return x


# Global default backend
_default_backend = None


def get_default_backend() -> GPUBackend:
    """Get global default GPU backend."""
    global _default_backend
    if _default_backend is None:
        _default_backend = GPUBackend()
    return _default_backend


def set_default_backend(backend: GPUBackend) -> None:
    """Set global default GPU backend."""
    global _default_backend
    _default_backend = backend


def get_available_backends() -> list:
    """Get list of available backends."""
    backends = [GPUBackendType.NUMPY]
    if JAX_AVAILABLE:
        backends.append(GPUBackendType.JAX)
    if CUPY_AVAILABLE:
        backends.append(GPUBackendType.CUPY)
    return backends


def is_gpu_available() -> bool:
    """Check if any GPU backend is available."""
    return JAX_AVAILABLE or CUPY_AVAILABLE
