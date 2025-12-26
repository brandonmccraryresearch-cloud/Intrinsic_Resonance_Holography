"""
Test Suite for Fine-Structure Constant Verification

This test suite validates the corrections made to expose the circularity
and discrepancy in the IRH fine-structure constant prediction.

Theoretical Reference:
    IRH v21.4 Part 1 §3.2.2, Eq. 3.4-3.5
    
Test Purpose:
    1. Verify CODATA 2022 values are correctly used
    2. Expose hardcoded implementation
    3. Calculate actual σ deviation from experiment
    4. Validate warning system functionality
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from src.observables.alpha_inverse import (
    compute_fine_structure_constant,
    verify_alpha_inverse_precision,
    get_implementation_warnings,
    ALPHA_INVERSE_EXPERIMENTAL,
    ALPHA_INVERSE_UNCERTAINTY,
    ALPHA_INVERSE_CLAIMED,
)


class TestAlphaInverseVerification:
    """Test suite for alpha inverse verification."""
    
    def test_codata_2022_value_correct(self):
        """Verify CODATA 2022 value is correctly set."""
        assert ALPHA_INVERSE_EXPERIMENTAL == 137.035999177, \
            "CODATA 2022 value should be 137.035999177"
        assert ALPHA_INVERSE_UNCERTAINTY == 0.000000021, \
            "CODATA 2022 uncertainty should be 0.000000021"
    
    def test_claimed_value_differs_from_experiment(self):
        """Verify IRH claim differs from CODATA 2022."""
        discrepancy = ALPHA_INVERSE_CLAIMED - ALPHA_INVERSE_EXPERIMENTAL
        # Discrepancy is negative (claim is lower than experiment)
        assert abs(discrepancy + 0.000000093) < 1e-9, \
            f"Discrepancy should be ~-0.000000093, got {discrepancy}"
    
    def test_sigma_deviation_calculation(self):
        """Verify correct calculation of σ deviation."""
        discrepancy = ALPHA_INVERSE_CLAIMED - ALPHA_INVERSE_EXPERIMENTAL
        sigma = discrepancy / ALPHA_INVERSE_UNCERTAINTY
        
        # Should be approximately -4.4σ
        assert abs(sigma + 4.4286) < 0.01, \
            f"σ deviation should be ~-4.4, got {sigma}"
    
    def test_analytical_method_returns_claimed_value(self):
        """Verify 'analytical' method returns hardcoded claim."""
        result = compute_fine_structure_constant(method='analytical')
        
        assert result.alpha_inverse == ALPHA_INVERSE_CLAIMED, \
            "Analytical method should return claimed value"
        assert 'HARDCODED' in str(result.components.get('note', '')), \
            "Components should indicate hardcoding"
    
    def test_full_method_shows_discrepancy(self):
        """Verify 'full' method exposes experimental discrepancy."""
        result = compute_fine_structure_constant(method='full')
        
        assert 'experimental_discrepancy' in result.components, \
            "Full method should include experimental comparison"
        
        disc = result.components['experimental_discrepancy']
        assert abs(disc['sigma_deviation'] + 4.4286) < 0.01, \
            f"Should show ~4.4σ deviation, got {disc['sigma_deviation']}"
    
    def test_precision_verification_fails(self):
        """Verify precision verification detects mismatch."""
        verification = verify_alpha_inverse_precision(n_digits=12)
        
        # Should NOT pass 12-digit agreement
        assert not verification['passed'], \
            "Should fail 12-digit precision test"
        
        # Mismatch occurs after "137.0359990" - so 10 digits match before divergence
        # The 11th significant digit differs: ...84 vs ...77
        assert verification['matching_digits'] >= 8, \
            f"Should match at least 8 digits, got {verification['matching_digits']}"
        assert verification['matching_digits'] < 12, \
            f"Should not match all 12 digits, got {verification['matching_digits']}"
        
        assert abs(verification['sigma_deviation'] + 4.4286) < 0.01, \
            "Should report ~4.4σ deviation"
    
    def test_implementation_warnings_exist(self):
        """Verify warning system reports incomplete implementation."""
        warnings = get_implementation_warnings()
        
        assert warnings['implementation_status'] == 'INCOMPLETE', \
            "Should report incomplete implementation"
        assert warnings['circularity_detected'] is True, \
            "Should detect circular reasoning"
        
        # Check for critical warnings
        warning_texts = ' '.join(warnings['warnings'])
        assert '𝒢_QNCD' in warning_texts or 'G_QNCD' in warning_texts, \
            "Should warn about missing QNCD term"
        assert 'hardcoded' in warning_texts.lower(), \
            "Should warn about hardcoding"
        assert '4.4' in warning_texts or 'sigma' in warning_texts.lower(), \
            "Should warn about sigma deviation"
    
    def test_missing_implementations_documented(self):
        """Verify missing implementations are documented."""
        warnings = get_implementation_warnings()
        
        missing = warnings['missing_implementations']
        assert len(missing) >= 3, \
            "Should document at least 3 missing implementations"
        
        # Check for critical missing pieces
        missing_str = ' '.join(missing)
        assert 'G_QNCD' in missing_str or '𝒢_QNCD' in missing_str, \
            "Should list missing QNCD computation"
        assert 'V_vertex' in missing_str or '𝒱' in missing_str, \
            "Should list missing vertex corrections"
    
    def test_leading_order_shows_deviation(self):
        """Verify leading-order method shows deviation from experiment."""
        result = compute_fine_structure_constant(method='leading')
        
        assert 'deviation_from_experiment' in result.components, \
            "Leading order should show deviation"
        
        # Leading order will have different value from both claim and experiment
        assert result.alpha_inverse != ALPHA_INVERSE_CLAIMED, \
            "Leading order should differ from hardcoded claim"
    
    def test_result_marks_inconsistency(self):
        """Verify result properly marks inconsistency with experiment."""
        result = compute_fine_structure_constant(method='full')
        
        # Should show significant sigma deviation
        assert abs(result.sigma_deviation) > 3.0, \
            f"Should show >3σ deviation, got {result.sigma_deviation}"
        
        # At 4.4σ, it's beyond 3σ but the is_consistent() method
        # checks abs(deviation) < n_sigma, so at 5σ it returns True (just barely)
        assert not result.is_consistent(3.0), \
            "Should not be consistent within 3σ"
        # Note: 4.43σ is technically < 5σ threshold, but statistically inconsistent
        assert abs(result.sigma_deviation) > 4.0, \
            "Should be beyond 4σ (statistically very inconsistent)"
    
    def test_codata_2026_claim_debunked(self):
        """Verify code documents that CODATA 2026 does not exist."""
        verification = verify_alpha_inverse_precision()
        
        assert 'CODATA 2026' in str(verification.get('manuscript_claim', '')), \
            "Should reference manuscript's CODATA 2026 claim"
        assert 'does not exist' in str(verification.get('reality', '')).lower(), \
            "Should state CODATA 2026 does not exist"


class TestCircularReasoningDetection:
    """Tests specifically for circular reasoning detection."""
    
    def test_full_method_admits_circularity(self):
        """Verify full method admits to circular implementation."""
        result = compute_fine_structure_constant(method='full')
        
        components = result.components
        
        # Should have circularity warning
        assert 'CIRCULARITY_WARNING' in components, \
            "Should include circularity warning"
        
        # Should list non-implemented terms
        assert 'NOT_IMPLEMENTED' in components, \
            "Should list non-implemented terms"
        
        not_impl = components['NOT_IMPLEMENTED']
        assert 'G_QNCD' in not_impl or 'V_vertex' in not_impl, \
            "Should list critical missing terms"


class TestExperimentalComparison:
    """Tests for proper experimental comparison."""
    
    def test_experimental_value_is_codata_2022(self):
        """Verify we compare against CODATA 2022, not hardcoded claim."""
        result = compute_fine_structure_constant(method='analytical')
        
        assert result.experimental == ALPHA_INVERSE_EXPERIMENTAL, \
            "Should compare against CODATA 2022"
        assert result.experimental == 137.035999177, \
            "CODATA 2022 value should be 137.035999177"
    
    def test_sigma_deviation_uses_correct_uncertainty(self):
        """Verify sigma deviation uses CODATA uncertainty."""
        result = compute_fine_structure_constant(method='analytical')
        
        expected_sigma = (ALPHA_INVERSE_CLAIMED - ALPHA_INVERSE_EXPERIMENTAL) / ALPHA_INVERSE_UNCERTAINTY
        
        assert abs(result.sigma_deviation - expected_sigma) < 1e-6, \
            f"Sigma deviation should be {expected_sigma}, got {result.sigma_deviation}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
