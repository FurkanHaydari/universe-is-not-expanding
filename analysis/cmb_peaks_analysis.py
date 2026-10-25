#!/usr/bin/env python3
"""
Planck 2018 CMB Acoustic Peaks and Plasma Standing Wave Resonance Analysis
-------------------------------------------------------------------------
This script evaluates the first 6 acoustic peaks of the Cosmic Microwave
Background (CMB) temperature anisotropy angular power spectrum (TT spectrum)
from Planck 2018 data against the acoustic standing wave resonance formulation
of the Unified Contraction Hypothesis, generating publication-quality figures.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Matplotlib style configuration
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'mathtext.fontset': 'cm',
})

# -------------------------------------------------------------------------
# 1. Planck 2018 Observational Acoustic Peaks (Aghanim et al. 2020)
# (n, ell_obs, sigma_ell, delta_T2_uK2, sigma_T2)
# -------------------------------------------------------------------------
planck_peaks = np.array([
    [1, 220.0, 0.5, 5740.0, 45.0],   # Peak 1 (Fundamental mode - compression)
    [2, 537.5, 0.8, 2580.0, 30.0],   # Peak 2 (1st harmonic - rarefaction)
    [3, 810.8, 1.2, 2540.0, 35.0],   # Peak 3 (2nd harmonic - compression)
    [4, 1120.0, 2.5, 1220.0, 25.0],  # Peak 4 (3rd harmonic - rarefaction)
    [5, 1444.0, 3.2, 820.0, 20.0],   # Peak 5 (4th harmonic - compression)
    [6, 1775.0, 4.0, 360.0, 15.0],   # Peak 6 (5th harmonic - rarefaction)
])

n_peak = planck_peaks[:, 0]
ell_obs = planck_peaks[:, 1]
sigma_ell = planck_peaks[:, 2]
amp_obs = planck_peaks[:, 3]
sigma_amp = planck_peaks[:, 4]

# -------------------------------------------------------------------------
# 2. Plasma Acoustic Resonance Model (Acoustic Scale ell_A)
# -------------------------------------------------------------------------
# Standing acoustic wave resonance peak relation:
# ell_n = ell_A * (n - phi_n)
# where ell_A is the acoustic spacing scale and phi_n is the baryonic phase shift.
# In fundamental modes: phi_n = phi_0 + delta * (n - 1)

def model_ell(n, ell_A, phi_0, delta):
    phi_n = phi_0 + delta * (n - 1.0)
    return ell_A * (n - phi_n)

def chi2_cmb(params):
    ell_A, phi_0, delta = params
    pred = model_ell(n_peak, ell_A, phi_0, delta)
    return np.sum(((ell_obs - pred) / sigma_ell)**2)

def run_analysis():
    res = minimize(chi2_cmb, [301.5, 0.268, -0.015])
    ell_A_fit, phi_0_fit, delta_fit = res.x
    chi2_val = res.fun
    dof = len(n_peak) - 3
    chi2_red = chi2_val / dof

    pred_all = model_ell(n_peak, ell_A_fit, phi_0_fit, delta_fit)

    print("=" * 70)
    print("      PLANCK 2018 CMB ACOUSTIC PEAKS: RESONANCE FIT ANALYSIS")
    print("=" * 70)
    print(f"Acoustic Scale Multipole (ell_A) : {ell_A_fit:.2f}")
    print(f"Fundamental Phase Shift (phi_0)  : {phi_0_fit:.4f}")
    print(f"Harmonic Slope Parameter (delta) : {delta_fit:.4f}")
    print(f"Total Chi^2                      : {chi2_val:.2f} (dof = {dof})")
    print(f"Reduced Chi^2 / dof             : {chi2_red:.3f}")
    print("-" * 70)
    print(" n   Observed (Planck)       Model (Contraction)   Residual (Delta ell)")
    print("-" * 70)
    for i in range(len(n_peak)):
        print(f" {int(n_peak[i])}    {ell_obs[i]:7.1f} +/- {sigma_ell[i]:3.1f}     {pred_all[i]:7.1f}           {ell_obs[i]-pred_all[i]:+6.2f}")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # 3. Publication-Ready Figure Generation
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(8.5, 7.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1.2], hspace=0.1)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    n_dense = np.linspace(0.8, 6.2, 200)
    ell_dense = model_ell(n_dense, ell_A_fit, phi_0_fit, delta_fit)

    ax1.errorbar(
        n_peak, ell_obs, yerr=sigma_ell, fmt='o',
        color='#1f2421', markersize=6.5, capsize=3.5, elinewidth=1.2,
        alpha=0.9, label='Planck 2018 Observations (Aghanim et al. 2020)'
    )
    ax1.plot(
        n_dense, ell_dense, '-',
        color='#7209b7', linewidth=2.2,
        label=rf'Plasma Acoustic Standing Wave Model ($\ell_A={ell_A_fit:.1f}$, $\chi^2_{{\mathrm{{red}}}}={chi2_red:.2f}$)'
    )

    for i in range(len(n_peak)):
        ax1.axvline(n_peak[i], color='gray', linestyle=':', alpha=0.35)
        ax1.annotate(
            f'Peak {int(n_peak[i])}\n$\\ell={ell_obs[i]:.0f}$',
            (n_peak[i], ell_obs[i] - 120),
            textcoords="data", ha='center', fontsize=8.5,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='linen', alpha=0.85, edgecolor='tan')
        )

    ax1.set_ylabel(r'Multipole Moment $\ell$')
    ax1.set_title(
        'Planck 2018 CMB Acoustic Peaks and Harmonic Vacuum Resonance',
        pad=12, fontweight='bold'
    )
    ax1.grid(True, which='both', linestyle=':', alpha=0.55)
    ax1.legend(loc='upper left', framealpha=0.92, facecolor='white')
    ax1.set_xlim(0.6, 6.4)
    ax1.set_ylim(100, 2000)

    # Bottom Panel: Residuals
    res_ell = ell_obs - pred_all
    ax2.axhline(0, color='gray', linestyle='-', linewidth=1.2)
    ax2.axhspan(-1.5, 1.5, color='lightgray', alpha=0.3, label=r'$\pm 1.5$ multipole band')

    ax2.errorbar(
        n_peak, res_ell, yerr=sigma_ell, fmt='s',
        color='#7209b7', markersize=5.5, capsize=3, elinewidth=1,
        alpha=0.85, label=r'$\Delta\ell = \ell_{\mathrm{obs}} - \ell_{\mathrm{model}}$'
    )

    ax2.set_xlabel(r'Acoustic Peak Index $n$')
    ax2.set_ylabel(r'$\Delta\ell$')
    ax2.set_ylim(-3.5, 3.5)
    ax2.grid(True, which='both', linestyle=':', alpha=0.55)
    ax2.legend(loc='upper right', framealpha=0.9, fontsize=9)

    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, 'cmb_peaks_comparison.pdf')
    png_path = os.path.join(output_dir, 'cmb_peaks_comparison.png')

    fig.savefig(pdf_path, dpi=300, bbox_inches='tight')
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f"\n[+] CMB acoustic peak figures successfully generated:")
    print(f"    - PDF : {pdf_path}")
    print(f"    - PNG : {png_path}")

if __name__ == '__main__':
    run_analysis()
