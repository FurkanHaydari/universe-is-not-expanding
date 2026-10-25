#!/usr/bin/env bash
# ==============================================================================
# Birleşik Büzülme Hipotezi - Zenodo / Açık Arşiv Dağıtım Paketi Hazırlama Betiği
# Unified Contraction Hypothesis - Zenodo Distribution & Release Export Script
# ==============================================================================
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

DIST_DIR="$ROOT_DIR/dist"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "================================================================="
echo "  ZENODO DAĞITIM VE YAYIN PAKETİ HAZIRLANIYOR (TR & EN)"
echo "  PREPARING ZENODO DISTRIBUTION PACKAGE (TR & EN)"
echo "================================================================="

# 1. LaTeX Geçici Dosyalarını Temizle (Clean LaTeX auxiliary files)
echo "[*] Geçici LaTeX derleme artıkları temizleniyor..."
find tr en -type f \( -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.toc" -o -name "*.synctex.gz" -o -name "indent.log" \) -delete

# 2. Türkçe PDF'leri Akademik İsimleriyle dist/ Klasörüne Kopyala (Turkish Editions from tr/)
echo "[*] [TR] Türkçe PDF'ler dist/ dizinine kopyalanıyor..."
cp tr/monograph/main.pdf                       "$DIST_DIR/Monograph_TR_Haydari_Birlesik_Buzulme_Hipotezi.pdf"
cp tr/papers/01_cosmology_pantheon/main.pdf   "$DIST_DIR/Paper_01_TR_Kozmoloji_ve_Pantheon.pdf"
cp tr/papers/02_scale_calculus/main.pdf       "$DIST_DIR/Paper_02_TR_Olcek_Zaman_Kalkulusu.pdf"
cp tr/papers/03_jwst_letter/main.pdf          "$DIST_DIR/Paper_03_TR_JWST_Erken_Galaksiler_Mektup.pdf"
cp tr/papers/04_gravity_river_model/main.pdf  "$DIST_DIR/Paper_04_TR_Kutlecekim_ve_Nehir_Modeli.pdf"
cp tr/papers/05_electromagnetism_137/main.pdf "$DIST_DIR/Paper_05_TR_Elektromanyetizma_ve_Kuantum_Kararlilik.pdf"
cp tr/papers/06_strong_force/main.pdf         "$DIST_DIR/Paper_06_TR_Guclu_Nukleer_Kuvvet_ve_Kuark_Hapsi.pdf"
cp tr/papers/07_weak_force/main.pdf           "$DIST_DIR/Paper_07_TR_Zayif_Nukleer_Kuvvet_ve_Kiral_Faz.pdf"

# 3. İngilizce PDF'leri Akademik İsimleriyle dist/ Klasörüne Kopyala (English Editions from en/)
echo "[*] [EN] İngilizce PDF'ler dist/ dizinine kopyalanıyor..."
cp en/monograph/main.pdf                       "$DIST_DIR/Monograph_EN_Haydari_Unified_Contraction_Hypothesis.pdf"
cp en/papers/01_cosmology_pantheon/main.pdf   "$DIST_DIR/Paper_01_EN_Cosmology_and_Pantheon.pdf"
cp en/papers/02_scale_calculus/main.pdf       "$DIST_DIR/Paper_02_EN_Scale_Time_Calculus.pdf"
cp en/papers/03_jwst_letter/main.pdf          "$DIST_DIR/Paper_03_EN_JWST_Early_Galaxies_Letter.pdf"
cp en/papers/04_gravity_river_model/main.pdf  "$DIST_DIR/Paper_04_EN_Gravitation_and_River_Model.pdf"
cp en/papers/05_electromagnetism_137/main.pdf "$DIST_DIR/Paper_05_EN_Electromagnetism_and_Quantum_Stability.pdf"
cp en/papers/06_strong_force/main.pdf         "$DIST_DIR/Paper_06_EN_Strong_Force_and_Quark_Confinement.pdf"
cp en/papers/07_weak_force/main.pdf           "$DIST_DIR/Paper_07_EN_Weak_Force_and_Chiral_Phase.pdf"

# 4. Sayısal Analiz Kodlarını ve Verileri ZIP Olarak Paketle
echo "[*] scale-cmb-solver analiz paketi ve veriler ZIP arşivine sıkıştırılıyor..."
zip -rq "$DIST_DIR/scale-cmb-solver-1.0.0-code-and-data.zip" \
    analysis \
    pyproject.toml \
    README.md \
    LICENSE \
    CITATION.cff \
    corpus.bib \
    -x "*.pyc" "*__pycache__*" "*.DS_Store*"

# 5. SHA-256 Sağlama Toplamlarını Üret (Generate SHA-256 Checksums)
echo "[*] SHA-256 sağlama toplamları üretiliyor..."
(cd "$DIST_DIR" && shasum -a 256 *.pdf *.zip > CHECKSUMS.sha256)

echo ""
echo "================================================================="
echo "  ZENODO YAYIN PAKETİ TAMAMLANDI (dist/):"
echo "  ZENODO PUBLICATION PACKAGE READY (16 PDFs + Code ZIP + CHECKSUMS):"
echo "================================================================="
ls -lh "$DIST_DIR"
echo "================================================================="
