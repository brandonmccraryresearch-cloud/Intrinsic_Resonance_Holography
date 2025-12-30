"""
Tests for library availability checker.

References
----------
src/techstack/availability.py
"""

import pytest
from src.techstack.availability import (
    check_available_libraries,
    get_tech_stack_status,
    get_required_libraries,
    get_optional_libraries,
    check_gpu_available,
    LibraryStatus,
)


class TestLibraryStatus:
    """Tests for LibraryStatus dataclass."""
    
    def test_library_status_creation(self):
        """Test creating LibraryStatus instance."""
        status = LibraryStatus(
            name="TestLib",
            available=True,
            version="1.0.0",
            import_name="testlib",
            description="Test library"
        )
        
        assert status.name == "TestLib"
        assert status.available is True
        assert status.version == "1.0.0"
    
    def test_library_status_repr(self):
        """Test string representation."""
        status = LibraryStatus(
            name="TestLib",
            available=True,
            version="1.0.0",
            description="Test library"
        )
        
        repr_str = repr(status)
        assert "TestLib" in repr_str
        assert "✓" in repr_str


class TestAvailabilityChecker:
    """Tests for availability checking functions."""
    
    def test_check_available_libraries(self):
        """Test checking all libraries."""
        libs = check_available_libraries()
        
        # Should return dictionary
        assert isinstance(libs, dict)
        
        # Should have required libraries
        assert "numpy" in libs
        assert "scipy" in libs
        assert "sympy" in libs
        
        # All values should be LibraryStatus
        for status in libs.values():
            assert isinstance(status, LibraryStatus)
    
    def test_required_libraries_available(self):
        """Test that required libraries are available."""
        libs = check_available_libraries()
        
        # NumPy and SciPy should always be available
        assert libs["numpy"].available is True
        assert libs["scipy"].available is True
    
    def test_get_tech_stack_status(self):
        """Test getting formatted status."""
        status = get_tech_stack_status()
        
        # Should return string
        assert isinstance(status, str)
        
        # Should contain section headers
        assert "Core Libraries" in status
        assert "JAX Ecosystem" in status
        assert "Quantum Libraries" in status
    
    def test_get_required_libraries(self):
        """Test getting required library list."""
        required = get_required_libraries()
        
        assert isinstance(required, list)
        assert "numpy" in required
        assert "scipy" in required
        assert "sympy" in required
    
    def test_get_optional_libraries(self):
        """Test getting optional library list."""
        optional = get_optional_libraries()
        
        assert isinstance(optional, list)
        assert "jax" in optional
        assert "qutip" in optional
    
    def test_check_gpu_available(self):
        """Test GPU availability check."""
        gpu_available = check_gpu_available()
        
        # Should return boolean
        assert isinstance(gpu_available, bool)
        
        # If True, at least one GPU library should be available
        if gpu_available:
            libs = check_available_libraries()
            assert libs.get("jax", LibraryStatus("", False)).available or \
                   libs.get("cupy", LibraryStatus("", False)).available


class TestLibraryVersions:
    """Tests for library version detection."""
    
    def test_numpy_version(self):
        """Test NumPy version detection."""
        libs = check_available_libraries()
        numpy_status = libs["numpy"]
        
        assert numpy_status.available is True
        assert numpy_status.version is not None
        assert len(numpy_status.version) > 0
    
    def test_scipy_version(self):
        """Test SciPy version detection."""
        libs = check_available_libraries()
        scipy_status = libs["scipy"]
        
        assert scipy_status.available is True
        assert scipy_status.version is not None


class TestFailureHandling:
    """Tests for graceful handling of missing libraries."""
    
    def test_missing_library_status(self):
        """Test status of missing libraries."""
        libs = check_available_libraries()
        
        # Check each optional library
        for lib_name in ["jax", "qutip", "taichi", "cupy"]:
            if lib_name in libs:
                status = libs[lib_name]
                # Should have status even if not available
                assert isinstance(status, LibraryStatus)
                assert status.name != ""
    
    def test_no_crash_on_missing_libs(self):
        """Test that functions don't crash with missing libraries."""
        # These should not raise exceptions
        libs = check_available_libraries()
        status = get_tech_stack_status()
        gpu = check_gpu_available()
        
        # All should return valid results
        assert libs is not None
        assert status is not None
        assert gpu in [True, False]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
