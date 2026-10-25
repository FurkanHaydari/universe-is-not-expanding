"""
scale-cmb-solver: Minimal Numerical Solver Package for Unified Contraction Hypothesis
--------------------------------------------------------------------------------------
This package provides numerical solvers and likelihood estimators for:
1. Pantheon+ Type Ia Supernova Covariance Analysis (dL, mu, chi2)
2. Planck 2018 CMB Acoustic Peaks Resonance Analysis (ell_n = ell_A * (n - phi_n))
3. Planck 2018 CMB Angular Power Spectrum Solver (D_ell^TT)
"""

from .pantheon_analysis import (
    dL_lcdm,
    mu_lcdm,
    dL_contraction,
    mu_contraction,
    chi2_contraction_cov,
    chi2_contraction_diag,
)

from .cmb_peaks_analysis import (
    model_ell,
    chi2_cmb,
)

from .cmb_spectrum_analysis import (
    model_spectrum,
    chi2_loss,
)

__version__ = "1.0.0"
__author__ = "Muhammed Furkan Haydari"

__all__ = [
    "dL_lcdm",
    "mu_lcdm",
    "dL_contraction",
    "mu_contraction",
    "chi2_contraction_cov",
    "chi2_contraction_diag",
    "model_ell",
    "chi2_cmb",
    "model_spectrum",
    "chi2_loss",
]
