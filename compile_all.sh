#!/usr/bin/env bash
# ==============================================================================
# Birleşik Büzülme Hipotezi - Monorepo Tüm Makaleler ve Külliyat Derleme Betiği
# Unified Contraction Hypothesis - Build Script for TR & EN Academic Papers
# ==============================================================================
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

echo "================================================================="
echo "  MONOREPO: TÜM MAKALELER VE MONOGRAFİ DERLENİYOR (TR & EN)"
echo "  BUILDING ALL ACADEMIC PAPERS AND MONOGRAPHS (TR & EN)"
echo "================================================================="

compile_doc() {
    local dir=$1
    local name=$2
    local lang=$3
    echo "[*] Derleniyor [$lang]: $name ($dir)..."
    cd "$ROOT_DIR/$dir"
    if [ -f "main.tex" ]; then
        pdflatex -interaction=nonstopmode main.tex > /dev/null
        pdflatex -interaction=nonstopmode main.tex > /dev/null
        echo "    -> [$lang] $dir/main.pdf TAMAMLANDI / COMPLETED"
    else
        echo "    [!] UYARI: $dir/main.tex bulunamadı!"
    fi
}

echo ""
echo "--- [1/2] TÜRKÇE KÜLLİYAT VE MAKALELER (TR) ---"
compile_doc "tr/papers/01_cosmology_pantheon"   "Makale 01 (Kozmoloji & Pantheon+)"         "TR"
compile_doc "tr/papers/02_scale_calculus"       "Makale 02 (Ölçek-Zaman Kalkülüsü)"         "TR"
compile_doc "tr/papers/03_jwst_letter"          "Makale 03 (JWST Ön-Baskı Mektubu)"         "TR"
compile_doc "tr/papers/04_gravity_river_model"  "Makale 04 (Kütleçekim & Nehir Modeli)"     "TR"
compile_doc "tr/papers/05_electromagnetism_137" "Makale 05 (Elektromanyetizma & 137)"       "TR"
compile_doc "tr/papers/06_strong_force"         "Makale 06 (Güçlü Kuvvet & Kuark Hapsi)"    "TR"
compile_doc "tr/papers/07_weak_force"           "Makale 07 (Zayıf Kuvvet & Kiral Faz)"      "TR"
compile_doc "tr/monograph"                      "Külliyat (Kapsamlı Teori Monografisi)"     "TR"

echo ""
echo "--- [2/2] ENGLISH CORPUS AND PAPERS (EN) ---"
compile_doc "en/papers/01_cosmology_pantheon"   "Paper 01 (Cosmology & Pantheon+)"          "EN"
compile_doc "en/papers/02_scale_calculus"       "Paper 02 (Scale-Time Calculus)"            "EN"
compile_doc "en/papers/03_jwst_letter"          "Paper 03 (JWST Early Galaxies Letter)"     "EN"
compile_doc "en/papers/04_gravity_river_model"  "Paper 04 (Gravitation & River Model)"      "EN"
compile_doc "en/papers/05_electromagnetism_137" "Paper 05 (Electromagnetism & 137)"         "EN"
compile_doc "en/papers/06_strong_force"         "Paper 06 (Strong Force & Confinement)"     "EN"
compile_doc "en/papers/07_weak_force"           "Paper 07 (Weak Force & Chiral Phase)"       "EN"
compile_doc "en/monograph"                      "Corpus (Comprehensive Research Monograph)" "EN"

echo ""
echo "================================================================="
echo "  MONOREPO'DAKİ TÜM MAKALELER VE MONOGRAFİLER BAŞARIYLA DERLENDİ!"
echo "  ALL PAPERS AND MONOGRAPHS SUCCESSFULLY COMPILED!"
echo "================================================================="
cd "$ROOT_DIR"
find tr en -name "main.pdf" -exec ls -lh {} +
