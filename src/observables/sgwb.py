"""
Observables Layer: SGWB and Cymatic Redshift

THEORETICAL FOUNDATION: IRH v22.2 Manuscript Part 1 §5.1

This module calculates the Stochastic Gravitational Wave Background (SGWB)
spectrum, incorporating Cymatic Redshift Broadening which resolves the
conflict between discrete resonance peaks and observed smooth spectra.

Key Concepts:
- **Cymatic Redshift Broadening**: \Delta f = f_n \sqrt{H_0 / f_n}.
- **Resonance Comb**: Discrete peaks visible in ULF regime.

Authors: Brandon D. McCrary
Last Updated: December 2025
"""

import numpy as np
from typing import List

__version__ = "22.2.0"
__theoretical_foundation__ = "IRH v22.2 Manuscript Part 1 §5.1"

# Hubble Constant (approximate value in Hz, H0 ~ 2.2e-18 Hz)
H0_HZ = 2.2e-18


def cymatic_redshift_broadening(frequency: float, h0: float = H0_HZ) -> float:
    """
    Calculate the phase diffusion width for a given frequency.

    Formula: \Delta f \approx f_n \cdot \sqrt{H_0 / f_n}

    Mechanism: Waves propagating through the fluctuating conductivity of the
    emergent metric undergo phase diffusion, smearing the resonance peaks.

    Args:
        frequency (float): Central resonant frequency f_n.
        h0 (float): Hubble constant (measure of expansion/dissipation).

    Returns:
        float: Broadening width \Delta f.
    """
    if frequency <= 0:
        return 0.0
    return frequency * np.sqrt(h0 / frequency)


def compute_sgwb_spectrum(
    frequencies: np.ndarray,
    resonance_peaks: List[float],
    ulf_regime: bool = False
) -> np.ndarray:
    """
    Compute the SGWB power spectral density \Omega_{GW}(f).

    Args:
        frequencies (np.ndarray): Array of frequencies to evaluate.
        resonance_peaks (List[float]): Fundamental frequencies of the CRN.
        ulf_regime (bool): If True, disables broadening for Ultra-Low Frequency check.

    Returns:
        np.ndarray: Power spectrum values.
    """
    spectrum = np.zeros_like(frequencies)

    for f_peak in resonance_peaks:
        if ulf_regime:
            # Discrete Comb: Dirac delta-like peaks (narrow Gaussian)
            width = f_peak * 1e-9 # Very narrow
        else:
            # Broadened Spectrum
            width = cymatic_redshift_broadening(f_peak)

        # Gaussian approximation of the resonance line shape
        # Amplitude arbitrary for shape verification; in full theory depends on energy density
        amplitude = 1.0

        # Contribution from this peak
        # Avoid division by zero
        if width > 0:
            peak_shape = np.exp(-0.5 * ((frequencies - f_peak) / width) ** 2)
            # Normalize to preserve energy? For visualization, height preservation is often clearer,
            # but physically, broadening conserves area. Let's conserve area.
            # Area of gaussian = amp * width * sqrt(2pi).
            # If we want unit area: amp = 1 / (width * sqrt(2pi))
            norm_amplitude = amplitude / (width * np.sqrt(2 * np.pi))
            spectrum += norm_amplitude * peak_shape

    return spectrum
