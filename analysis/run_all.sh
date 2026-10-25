#!/bin/bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$DIR")"
VENV_PY="$ROOT_DIR/.venv/bin/python3"

if [ ! -f "$VENV_PY" ]; then
    echo "Virtual environment not found at $ROOT_DIR/.venv. Using system python3..."
    PYTHON_CMD="python3"
else
    PYTHON_CMD="$VENV_PY"
fi

echo "================================================================="
echo " Unified Contraction Hypothesis: Numerical Analysis Suite"
echo "================================================================="
echo ""
echo "[1/3] Running Pantheon+ Supernova Likelihood & Covariance Analysis..."
"$PYTHON_CMD" "$DIR/pantheon_analysis.py"

echo ""
echo "[2/3] Running Planck 2018 CMB Acoustic Peaks Resonance Analysis..."
"$PYTHON_CMD" "$DIR/cmb_peaks_analysis.py"

echo ""
echo "[3/3] Running Planck 2018 CMB Angular Power Spectrum (D_ell^TT) Solver..."
"$PYTHON_CMD" "$DIR/cmb_spectrum_analysis.py"

echo ""
echo "All analyses successfully completed and publication figures generated:"
echo " - $DIR/pantheon_fit_comparison.pdf"
echo " - $DIR/pantheon_covariance_matrix.pdf"
echo " - $DIR/cmb_peaks_comparison.pdf"
echo " - $DIR/cmb_spectrum_comparison.pdf"
