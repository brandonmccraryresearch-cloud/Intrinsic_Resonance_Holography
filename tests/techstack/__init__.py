"""
Tests for tech stack integration module.

Tests cover:
- Library availability detection
- Backend configuration
- GPU backend abstraction
- Library wrappers with fallbacks
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
