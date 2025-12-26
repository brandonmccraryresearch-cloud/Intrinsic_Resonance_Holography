#!/usr/bin/env python3
"""
Demonstration: Fine-Structure Constant Verification

This script demonstrates the corrected implementation that exposes
the circularity and empirical discrepancy in the IRH α⁻¹ calculation.

Run: python scripts/demo_alpha_verification.py
"""

import sys
from pathlib import Path

# Add src to path
_repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_repo_root))

from src.observables.alpha_inverse import (
    compute_fine_structure_constant,
    verify_alpha_inverse_precision,
    get_implementation_warnings,
    ALPHA_INVERSE_EXPERIMENTAL,
    ALPHA_INVERSE_UNCERTAINTY,
    ALPHA_INVERSE_CLAIMED,
)


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_warning_box(message):
    """Print warning in a box."""
    lines = message.split('\n')
    width = max(len(line) for line in lines) + 4
    print("┌" + "─" * (width - 2) + "┐")
    for line in lines:
        print(f"│ ⚠️  {line:<{width - 6}}│")
    print("└" + "─" * (width - 2) + "┘")


def main():
    """Run verification demonstration."""
    
    print_header("IRH Fine-Structure Constant Verification")
    
    print("This demonstration exposes critical issues in the IRH α⁻¹ calculation:")
    print("  1. Hardcoded result (circular reasoning)")
    print("  2. Missing non-perturbative terms")
    print("  3. Disagreement with CODATA 2022 (4.4σ)")
    print("  4. Reference to non-existent 'CODATA 2026'")
    
    # Show experimental values
    print_header("Experimental Values")
    
    print(f"CODATA 2022 (actual measurement):")
    print(f"  α⁻¹ = {ALPHA_INVERSE_EXPERIMENTAL:.12f} ± {ALPHA_INVERSE_UNCERTAINTY:.12f}")
    print()
    print(f"IRH Manuscript Claim (§3.2.2):")
    print(f"  α⁻¹ = {ALPHA_INVERSE_CLAIMED:.12f} (claimed from 'CODATA 2026')")
    print()
    
    discrepancy = ALPHA_INVERSE_CLAIMED - ALPHA_INVERSE_EXPERIMENTAL
    sigma = discrepancy / ALPHA_INVERSE_UNCERTAINTY
    print(f"Discrepancy:")
    print(f"  Δα⁻¹ = {discrepancy:.12f}")
    print(f"  σ deviation = {sigma:.2f}σ")
    print()
    
    print_warning_box(
        "CRITICAL: 4.4σ deviation is statistically significant!\n"
        "In particle physics, > 5σ is discovery-level evidence.\n"
        "This 4.4σ discrepancy suggests theoretical issues."
    )
    
    # Test different methods
    print_header("Method Comparison")
    
    for method in ['analytical', 'leading', 'full']:
        print(f"\n--- Method: '{method}' ---")
        try:
            result = compute_fine_structure_constant(method=method)
            print(f"Computed: α⁻¹ = {result.alpha_inverse:.12f}")
            print(f"Uncertainty: {result.uncertainty:.2e}")
            print(f"σ deviation: {result.sigma_deviation:.2f}σ")
            print(f"Consistent (3σ): {result.is_consistent(3.0)}")
            
            if method == 'analytical':
                note = result.components.get('note', '')
                if 'HARDCODED' in note:
                    print_warning_box("⚠️  This method returns HARDCODED value!")
                    
            if method == 'full':
                if 'NOT_IMPLEMENTED' in result.components:
                    missing = result.components['NOT_IMPLEMENTED']
                    print("\nMissing implementations:")
                    for key, desc in missing.items():
                        print(f"  • {key}: {desc}")
                        
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Show precision verification
    print_header("Precision Verification")
    
    verification = verify_alpha_inverse_precision(n_digits=12)
    
    print(f"Claimed value:      {verification['claimed_str']}")
    print(f"CODATA 2022 value:  {verification['experimental_str']}")
    print(f"Matching digits:    {verification['matching_digits']}/12")
    print(f"First mismatch:     Position {verification['first_mismatch_digit']}")
    print(f"Test result:        {'✓ PASS' if verification['passed'] else '✗ FAIL'}")
    print()
    
    print(f"Statistical analysis:")
    print(f"  Discrepancy:      {verification['discrepancy']:.12f}")
    print(f"  σ deviation:      {verification['sigma_deviation']:.2f}σ")
    print(f"  Consistency:      {verification['consistency_status']}")
    print()
    
    print(f"Manuscript claim:   {verification['manuscript_claim']}")
    print(f"Reality:            {verification['reality']}")
    
    # Show implementation warnings
    print_header("Implementation Warnings")
    
    warnings = get_implementation_warnings()
    
    print(f"Implementation status: {warnings['implementation_status']}")
    print(f"Circularity detected: {warnings['circularity_detected']}")
    print()
    
    print("Critical warnings:")
    for i, warning in enumerate(warnings['warnings'], 1):
        print(f"  {i}. {warning}")
    print()
    
    print("Missing implementations:")
    for impl in warnings['missing_implementations']:
        print(f"  • {impl}")
    print()
    
    print("Required for completion:")
    for req in warnings['required_for_completion']:
        print(f"  ✗ {req}")
    
    # Final summary
    print_header("Summary")
    
    print("⚠️  CRITICAL ISSUES DETECTED:")
    print()
    print("1. CIRCULAR REASONING:")
    print("   The 'analytical' and 'full' methods return a HARDCODED value")
    print("   instead of computing α⁻¹ from first principles.")
    print()
    print("2. INCOMPLETE IMPLEMENTATION:")
    print("   Non-perturbative terms (𝒢_QNCD, 𝒱) are NOT computed.")
    print("   The claimed formula is not fully implemented.")
    print()
    print("3. EMPIRICAL MISMATCH:")
    print(f"   IRH claim: {ALPHA_INVERSE_CLAIMED:.12f}")
    print(f"   CODATA 2022: {ALPHA_INVERSE_EXPERIMENTAL:.12f}")
    print(f"   Discrepancy: {abs(sigma):.2f}σ (statistically significant)")
    print()
    print("4. FICTIONAL DATA SOURCE:")
    print("   Manuscript claims 'CODATA 2026' which does not exist.")
    print("   Most recent data is CODATA 2022.")
    print()
    
    print_warning_box(
        "VERDICT: The current implementation FAILS to constitute\n"
        "a genuine first-principles derivation and is INCONSISTENT\n"
        "with experimental measurements."
    )
    
    print("\nFor full details, see: docs/ALPHA_INVERSE_VERIFICATION_REPORT.md")
    print()


if __name__ == '__main__':
    main()
