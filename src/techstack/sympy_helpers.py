"""
SymPy Integration Helpers.

Provides symbolic mathematics capabilities for analytical derivations
and verification.

References
----------
.github/GITHUB_COPILOT_AGENT_IRH_v21.4.md - SymPy patterns
IRH v21.4 Manuscript - Analytical derivations throughout
"""

from typing import Optional

# SymPy should be available (it's in core requirements)
try:
    import sympy as sp
    from sympy import symbols, Matrix, exp, I, pi, sqrt
    from sympy.algebras.quaternion import Quaternion
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    sp = None


class SymbolicBetaFunctions:
    """
    Symbolic computation of beta functions.
    
    Provides analytical expressions for RG flow equations.
    
    References
    ----------
    IRH v21.4 Manuscript, Equation 1.13 - Beta functions
    
    Examples
    --------
    >>> beta_sym = SymbolicBetaFunctions()
    >>> if beta_sym.available:
    ...     expr = beta_sym.beta_lambda_expr()
    ...     print(expr)
    """
    
    def __init__(self):
        """Initialize symbolic beta functions."""
        self.available = SYMPY_AVAILABLE
        
        if self.available:
            # Define symbolic variables
            self.lambda_sym = symbols('lambda', real=True, positive=True)
            self.gamma_sym = symbols('gamma', real=True, positive=True)
            self.mu_sym = symbols('mu', real=True, positive=True)
    
    def beta_lambda_expr(self) -> Optional[object]:
        """
        Get symbolic expression for β_λ.
        
        Returns
        -------
        sympy expression or None
            β_λ = -2λ̃ + (9/8π²)λ̃²
        """
        if not self.available:
            return None
        
        return -2 * self.lambda_sym + (9 / (8 * pi**2)) * self.lambda_sym**2
    
    def beta_gamma_expr(self) -> Optional[object]:
        """
        Get symbolic expression for β_γ.
        
        Returns
        -------
        sympy expression or None
            β_γ = (3/4π²)λ̃γ̃
        """
        if not self.available:
            return None
        
        return (3 / (4 * pi**2)) * self.lambda_sym * self.gamma_sym
    
    def beta_mu_expr(self) -> Optional[object]:
        """
        Get symbolic expression for β_μ.
        
        Returns
        -------
        sympy expression or None
            β_μ = 2μ̃ + (1/2π²)λ̃μ̃
        """
        if not self.available:
            return None
        
        return 2 * self.mu_sym + (1 / (2 * pi**2)) * self.lambda_sym * self.mu_sym
    
    def find_fixed_point_symbolic(self) -> Optional[dict]:
        """
        Compute symbolic one-loop β-function zeros (not the full IRH fixed point).
        
        This helper solves the **one-loop** truncated beta function for λ̃
        (Eq. 1.13 in the IRH v21.4 Manuscript) by imposing β_λ(λ̃) = 0 and returns
        the resulting symbolic λ̃ solutions. It does **not** incorporate the full
        functional RG (Wetterich) equation (Eq. 1.12) and therefore does **not**
        reproduce the certified cosmic fixed point (Eq. 1.14), which is implemented
        in the numerical RG flow stack (see ``src/rg_flow/fixed_points.py``).
        
        This method is intended solely for analytical verification and sanity checks
        of the one-loop structure; it MUST NOT be used as the IRH v21.4 cosmic fixed
        point in any production computations.
        
        Returns
        -------
        dict or None
            Dictionary with symbolic one-loop β_λ=0 solutions and associated
            metadata, or None if SymPy is unavailable.
        """
        if not self.available:
            return None
        
        # Solve β_λ = 0 for the one-loop truncated beta function (Eq. 1.13).
        # This yields the perturbative β_λ-zero(s) only; it is **not** the
        # full IRH v21.4 cosmic fixed point from the Wetterich equation (Eq. 1.12).
        lambda_fps = sp.solve(self.beta_lambda_expr(), self.lambda_sym)
        
        # Return explicit metadata to prevent confusion with the certified
        # CosmicFixedPoint implementation in src/rg_flow/fixed_points.py.
        return {
            "lambda_star": lambda_fps,
            "beta_order": "one_loop",
            "scheme": "symbolic_one_loop_beta_lambda_zero",
            "is_certified_irh_v21_4_fixed_point": False,
            "description": (
                "Symbolic one-loop β_λ=0 solutions for analytical verification only; "
                "does NOT implement the full Wetterich equation or Eq. 1.14."
            ),
            "note": (
                "One-loop approximation of β_λ=0. The certified cosmic fixed point "
                "requires the full Wetterich equation and is implemented in "
                "src/rg_flow/fixed_points.py."
            ),
        }


class QuaternionicAlgebra:
    """
    Symbolic quaternion algebra operations.
    
    Handles quaternionic field computations symbolically.
    
    References
    ----------
    IRH v21.4 Manuscript, Section 1.2.1 - Quaternionic cGFT
    
    Examples
    --------
    >>> quat = QuaternionicAlgebra()
    >>> if quat.available:
    ...     q1 = quat.create(1, 2, 3, 4)
    ...     q2 = quat.create(5, 6, 7, 8)
    ...     product = quat.multiply(q1, q2)
    """
    
    def __init__(self):
        """Initialize quaternionic algebra."""
        self.available = SYMPY_AVAILABLE
    
    def create(self, w: float, x: float, y: float, z: float) -> Optional[object]:
        """
        Create quaternion w + xi + yj + zk.
        
        Parameters
        ----------
        w, x, y, z : float
            Quaternion components.
            
        Returns
        -------
        Quaternion or None
            SymPy quaternion object.
        """
        if not self.available:
            return None
        
        return Quaternion(w, x, y, z)
    
    def multiply(self, q1: object, q2: object) -> Optional[object]:
        """
        Multiply two quaternions.
        
        Parameters
        ----------
        q1, q2 : Quaternion
            Quaternions to multiply.
            
        Returns
        -------
        Quaternion or None
            Product q1 * q2.
        """
        if not self.available or q1 is None or q2 is None:
            return None
        
        return q1 * q2
    
    def conjugate(self, q: object) -> Optional[object]:
        """
        Compute quaternion conjugate.
        
        Parameters
        ----------
        q : Quaternion
            Quaternion to conjugate.
            
        Returns
        -------
        Quaternion or None
            Conjugate q̄ = w - xi - yj - zk.
        """
        if not self.available or q is None:
            return None
        
        return q.conjugate()
    
    def norm(self, q: object) -> Optional[float]:
        """
        Compute quaternion norm.
        
        Parameters
        ----------
        q : Quaternion
            Quaternion.
            
        Returns
        -------
        float or None
            Norm |q| = √(w² + x² + y² + z²).
        """
        if not self.available or q is None:
            return None
        
        return q.norm()


class SymbolicDerivations:
    """
    Helper class for symbolic derivations and verifications.
    
    Examples
    --------
    >>> deriv = SymbolicDerivations()
    >>> if deriv.available:
    ...     # Verify analytical formula
    ...     expr = deriv.verify_commutator()
    """
    
    def __init__(self):
        """Initialize symbolic derivations helper."""
        self.available = SYMPY_AVAILABLE
    
    def verify_commutator(
        self,
        A: Optional[object] = None,
        B: Optional[object] = None
    ) -> Optional[object]:
        """
        Verify commutator relations symbolically.
        
        Parameters
        ----------
        A, B : sympy Matrix, optional
            Operators to compute commutator. If None, uses SU(2) generators.
            
        Returns
        -------
        sympy expression or None
            [A, B] = AB - BA.
        """
        if not self.available:
            return None
        
        if A is None or B is None:
            # Default: Pauli matrices (SU(2) generators)
            A = Matrix([[0, 1], [1, 0]])  # σ_x
            B = Matrix([[0, -I], [I, 0]])  # σ_y
        
        return A * B - B * A
    
    def generate_latex(self, expr: object) -> Optional[str]:
        """
        Generate LaTeX representation of expression.
        
        Parameters
        ----------
        expr : sympy expression
            Expression to convert.
            
        Returns
        -------
        str or None
            LaTeX string.
        """
        if not self.available or expr is None:
            return None
        
        return sp.latex(expr)


def is_available() -> bool:
    """Check if SymPy is available."""
    return SYMPY_AVAILABLE


def get_version() -> Optional[str]:
    """Get SymPy version if available."""
    if SYMPY_AVAILABLE:
        try:
            return sp.__version__
        except Exception:
            return "unknown"
    return None
