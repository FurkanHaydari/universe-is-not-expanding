#!/usr/bin/env python3
"""
Pantheon+ Type Ia Supernova Analysis and Unified Contraction Hypothesis Fit Test
--------------------------------------------------------------------------------
This script performs a statistical comparison between the Standard Lambda-CDM
Expansion Model and the Unified Contraction Hypothesis (Scale-Time Calculus)
using the official Pantheon+ Type Ia Supernova compilation and covariance matrix.
It conducts chi-square minimization and generates publication-ready vector figures.
"""

import os
import numpy as np
import scipy.integrate as integrate
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Matplotlib style configuration (Physical Review / Nature standard)
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 15,
    'mathtext.fontset': 'cm',
})

# Physical Constants
c_km_s = 299792.458  # Speed of light in km/s

# -------------------------------------------------------------------------
# 1. Official Pantheon+ Supernova Dataset and Covariance Matrix
# (Brout et al. 2022 / Scolnic et al. 2022 Official Release)
# -------------------------------------------------------------------------
# Authentic observational data and covariance matrix obtained from the official
# Pantheon+SH0ES release. Synthetic exponential models have been fully replaced.
# -------------------------------------------------------------------------

data_dir = os.path.join(os.path.dirname(__file__), 'data')
cov_file = os.path.join(data_dir, 'pantheon_cov_binned.npy')
z_file = os.path.join(data_dir, 'pantheon_z_binned.npy')
mu_file = os.path.join(data_dir, 'pantheon_mu_binned.npy')
sigma_file = os.path.join(data_dir, 'pantheon_sigma_binned.npy')

if os.path.exists(cov_file) and os.path.exists(z_file) and os.path.exists(mu_file) and os.path.exists(sigma_file):
    z_data = np.load(z_file)
    mu_data = np.load(mu_file)
    sigma_data = np.load(sigma_file)
    cov_matrix = np.load(cov_file)
else:
    raise FileNotFoundError(f"Official Pantheon+ data and covariance files not found in {data_dir}!")

n_data = len(z_data)

# Inverse covariance matrix and correlation matrix
cov_inv = np.linalg.inv(cov_matrix)
corr_matrix = cov_matrix / np.outer(sigma_data, sigma_data)

# -------------------------------------------------------------------------
# 2. Theoretical Models
# -------------------------------------------------------------------------

def dL_lcdm(z, H0, Om=0.3, Ol=0.7):
    """
    Standard Lambda-CDM Model Luminosity Distance (Mpc).
    """
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1.0 + zp)**3 + Ol)
    
    if np.isscalar(z):
        val, _ = integrate.quad(integrand, 0, z)
        return (c_km_s * (1.0 + z) / H0) * val
    else:
        res = np.zeros_like(z)
        for i, zi in enumerate(z):
            val, _ = integrate.quad(integrand, 0, zi)
            res[i] = (c_km_s * (1.0 + zi) / H0) * val
        return res

def mu_lcdm(z, H0, Om=0.3, Ol=0.7):
    """Standard Lambda-CDM Distance Modulus: mu = 5 log10(dL) + 25"""
    dl = dL_lcdm(z, H0, Om, Ol)
    return 5.0 * np.log10(dl) + 25.0

def dL_contraction(z, H0):
    """
    Unified Contraction Hypothesis Luminosity Distance:
    dL(z) = (c / H0) * (1 + z) * ln(1 + z)
    Derived analytically from the conformal contraction of atomic standards
    in static Euclidean space. Contains zero dark energy parameters (Omega_Lambda = 0)!
    """
    return (c_km_s / H0) * (1.0 + z) * np.log(1.0 + z)

def mu_contraction(z, H0):
    """Unified Contraction Hypothesis Distance Modulus"""
    dl = dL_contraction(z, H0)
    return 5.0 * np.log10(dl) + 25.0

# -------------------------------------------------------------------------
# 3. Statistical Likelihood Fitting (Full Covariance & Diagonal Chi-Square)
# -------------------------------------------------------------------------

def chi2_lcdm_cov(params):
    H0 = params[0]
    delta = mu_data - mu_lcdm(z_data, H0)
    return float(delta @ cov_inv @ delta)

def chi2_contraction_cov(params):
    H0 = params[0]
    delta = mu_data - mu_contraction(z_data, H0)
    return float(delta @ cov_inv @ delta)

def chi2_lcdm_diag(H0):
    delta = mu_data - mu_lcdm(z_data, H0)
    return float(np.sum((delta / sigma_data)**2))

def chi2_contraction_diag(H0):
    delta = mu_data - mu_contraction(z_data, H0)
    return float(np.sum((delta / sigma_data)**2))

def run_analysis():
    # Optimization under full covariance matrix
    res_lcdm = minimize(chi2_lcdm_cov, [70.0], bounds=[(50.0, 90.0)])
    res_cont = minimize(chi2_contraction_cov, [70.0], bounds=[(50.0, 90.0)])

    H0_lcdm = res_lcdm.x[0]
    chi2_cov_lcdm = res_lcdm.fun
    chi2_diag_lcdm = chi2_lcdm_diag(H0_lcdm)
    dof_lcdm = n_data - 1
    chi2_red_lcdm = chi2_cov_lcdm / dof_lcdm

    H0_cont = res_cont.x[0]
    chi2_cov_cont = res_cont.fun
    chi2_diag_cont = chi2_contraction_diag(H0_cont)
    dof_cont = n_data - 1
    chi2_red_cont = chi2_cov_cont / dof_cont

    # Analytical 1-sigma uncertainty from Fisher information matrix:
    # d(mu)/d(H0) = -5 / (H0 * ln 10)
    sum_cov_inv = np.sum(cov_inv)
    sigma_H0_lcdm = (H0_lcdm * np.log(10.0)) / (5.0 * np.sqrt(sum_cov_inv))
    sigma_H0_cont = (H0_cont * np.log(10.0)) / (5.0 * np.sqrt(sum_cov_inv))

    # Information Criteria (AIC & BIC)
    aic_lcdm = chi2_cov_lcdm + 2 * 1
    bic_lcdm = chi2_cov_lcdm + np.log(n_data) * 1

    aic_cont = chi2_cov_cont + 2 * 1
    bic_cont = chi2_cov_cont + np.log(n_data) * 1

    print("=" * 72)
    print("   PANTHEON+ SUPERNOVA COMPILATION: FULL COVARIANCE FIT ANALYSIS")
    print("=" * 72)
    print(f"Total Binned Data Points (N)    : {n_data}")
    print(f"Covariance Matrix Dimensions    : {cov_matrix.shape[0]}x{cov_matrix.shape[1]}")
    print("-" * 72)
    print(f"STANDARD LAMBDA-CDM MODEL (Omega_m = 0.30, Omega_Lambda = 0.70):")
    print(f"  Best-fit H0                   : {H0_lcdm:.2f} +/- {sigma_H0_lcdm:.2f} km/s/Mpc")
    print(f"  Total Chi^2 (Covariance)     : {chi2_cov_lcdm:.2f}")
    print(f"  Total Chi^2 (Diagonal)       : {chi2_diag_lcdm:.2f}")
    print(f"  Degrees of Freedom (dof)     : {dof_lcdm}")
    print(f"  Reduced Chi^2 / dof          : {chi2_red_lcdm:.3f}")
    print(f"  AIC / BIC                    : {aic_lcdm:.2f} / {bic_lcdm:.2f}")
    print("-" * 72)
    print(f"UNIFIED CONTRACTION HYPOTHESIS (Scale-Time Calculus, Zero Dark Energy):")
    print(f"  Best-fit H0                   : {H0_cont:.2f} +/- {sigma_H0_cont:.2f} km/s/Mpc")
    print(f"  Total Chi^2 (Covariance)     : {chi2_cov_cont:.2f}")
    print(f"  Total Chi^2 (Diagonal)       : {chi2_diag_cont:.2f}")
    print(f"  Degrees of Freedom (dof)     : {dof_cont}")
    print(f"  Reduced Chi^2 / dof          : {chi2_red_cont:.3f}")
    print(f"  AIC / BIC                    : {aic_cont:.2f} / {bic_cont:.2f}")
    print("=" * 72)

    # -------------------------------------------------------------------------
    # 4. Publication-Ready Figure Generation (Matplotlib)
    # -------------------------------------------------------------------------

    z_smooth = np.logspace(np.log10(0.008), np.log10(2.5), 250)
    mu_smooth_lcdm = mu_lcdm(z_smooth, H0_lcdm)
    mu_smooth_cont = mu_contraction(z_smooth, H0_cont)

    fig = plt.figure(figsize=(8.5, 7.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.2], hspace=0.08)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    # Top Panel: Hubble Diagram
    ax1.errorbar(
        z_data, mu_data, yerr=sigma_data, fmt='o',
        color='#1f2421', markersize=5, capsize=2.5, elinewidth=1,
        alpha=0.85, label=f'Pantheon+ Sample (Binned, N={n_data})'
    )
    ax1.plot(
        z_smooth, mu_smooth_lcdm, '--',
        color='#2e6f40', linewidth=2,
        label=rf'Standard $\Lambda\mathrm{{CDM}}$ ($\Omega_m=0.3, \Omega_\Lambda=0.7$, $\chi^2_{{\mathrm{{red}}}}={chi2_red_lcdm:.2f}$)'
    )
    ax1.plot(
        z_smooth, mu_smooth_cont, '-',
        color='#c1121f', linewidth=2.2,
        label=rf'Unified Contraction ($d_L \propto (1+z)\ln(1+z)$, $\chi^2_{{\mathrm{{red}}}}={chi2_red_cont:.2f}$)'
    )

    ax1.set_xscale('log')
    ax1.set_ylabel(r'Distance Modulus $\mu(z) = m - M$ [mag]')
    ax1.set_title(
        'Pantheon+ Type Ia Supernova Hubble Diagram and Model Fits',
        pad=12, fontweight='bold'
    )
    ax1.grid(True, which='both', linestyle=':', alpha=0.55)
    ax1.legend(loc='lower right', framealpha=0.92, facecolor='white')
    ax1.set_ylim(32, 47)

    # Bottom Panel: Residuals (Data - Model)
    res_lcdm_pts = mu_data - mu_lcdm(z_data, H0_lcdm)
    res_cont_pts = mu_data - mu_contraction(z_data, H0_cont)

    ax2.axhline(0, color='gray', linestyle='-', linewidth=1.2)
    ax2.axhspan(-0.1, 0.1, color='lightgray', alpha=0.3, label=r'$\pm 0.1$ mag band')

    ax2.errorbar(
        z_data, res_lcdm_pts, yerr=sigma_data, fmt='s',
        color='#2e6f40', markersize=4, capsize=2, elinewidth=0.8,
        alpha=0.7, label=r'$\Delta\mu$ ($\Lambda\mathrm{CDM}$)'
    )
    ax2.errorbar(
        z_data, res_cont_pts, yerr=sigma_data, fmt='^',
        color='#c1121f', markersize=4.5, capsize=2, elinewidth=0.8,
        alpha=0.85, label=r'$\Delta\mu$ (Unified Contraction)'
    )

    ax2.set_xscale('log')
    ax2.set_xlabel(r'Redshift $z$')
    ax2.set_ylabel(r'$\Delta\mu$ [mag]')
    ax2.set_ylim(-0.35, 0.35)
    ax2.grid(True, which='both', linestyle=':', alpha=0.55)
    ax2.legend(loc='upper right', ncol=3, framealpha=0.9, fontsize=8.5)

    # Save outputs
    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, 'pantheon_fit_comparison.pdf')
    png_path = os.path.join(output_dir, 'pantheon_fit_comparison.png')

    fig.savefig(pdf_path, dpi=300, bbox_inches='tight')
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    # Supplementary Figure: Covariance & Correlation Matrix Heatmap
    fig_cov, ax_cov = plt.subplots(figsize=(6.5, 5.5))
    im = ax_cov.imshow(corr_matrix, cmap='viridis', origin='lower', vmin=0, vmax=1)
    cbar = fig_cov.colorbar(im, ax=ax_cov, fraction=0.046, pad=0.04)
    cbar.set_label(r'Correlation Coefficient $\rho_{ij}$', rotation=270, labelpad=15)

    step = 4
    ticks_idx = np.arange(0, n_data, step)
    ax_cov.set_xticks(ticks_idx)
    ax_cov.set_xticklabels([f"{z_data[i]:.2f}" for i in ticks_idx], rotation=45)
    ax_cov.set_yticks(ticks_idx)
    ax_cov.set_yticklabels([f"{z_data[i]:.2f}" for i in ticks_idx])

    ax_cov.set_xlabel(r'Redshift $z_j$')
    ax_cov.set_ylabel(r'Redshift $z_i$')
    ax_cov.set_title(r'Pantheon+ Binned Covariance Correlation Matrix $R_{ij}$', pad=12, fontweight='bold', fontsize=11)

    cov_pdf = os.path.join(output_dir, 'pantheon_covariance_matrix.pdf')
    cov_png = os.path.join(output_dir, 'pantheon_covariance_matrix.png')
    fig_cov.savefig(cov_pdf, dpi=300, bbox_inches='tight')
    fig_cov.savefig(cov_png, dpi=300, bbox_inches='tight')
    plt.close(fig_cov)

    print(f"\n[+] Publication figures successfully generated:")
    print(f"    - PDF        : {pdf_path}")
    print(f"    - PNG        : {png_path}")
    print(f"    - Matrix PDF : {cov_pdf}")
    print(f"    - Matrix PNG : {cov_png}")

if __name__ == '__main__':
    run_analysis()
