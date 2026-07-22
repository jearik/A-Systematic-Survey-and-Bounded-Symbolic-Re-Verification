#!/usr/bin/env bash
# One-command runner for the six ProVerif re-verification models.
# Prereq: ProVerif installed (Linux/macOS):  opam init -y && opam install proverif
# Usage:  bash run_all.sh        (writes each model's full output to results/<model>.txt
#                                  and a one-line PASS/ATTACK summary to results/SUMMARY.txt)

set -u
mkdir -p results
SUM=results/SUMMARY.txt
: > "$SUM"
echo "ProVerif re-verification run  $(date)" | tee -a "$SUM"
echo "proverif version: $(proverif -help 2>&1 | head -1)" | tee -a "$SUM"
echo "--------------------------------------------" | tee -a "$SUM"

for m in M1_certificate_based_ECDHE M2_IBS_blockchain M3_certificateless_AKA \
         M4_blockchain_pseudonym M5_PUF_keyestab M6_anonymous_ZKP; do
  out="results/${m}.txt"
  echo ">>> running $m"
  proverif "${m}.pv" > "$out" 2>&1
  # extract every RESULT line (true / false / cannot be proved)
  echo "### $m" >> "$SUM"
  grep -E "^RESULT|is true|is false|cannot be proved" "$out" >> "$SUM" || echo "  (no RESULT lines - check $out for syntax errors)" >> "$SUM"
  echo "" >> "$SUM"
done

echo "Done. Per-model logs in results/*.txt ; one-line verdicts in $SUM"
echo "Send me results/SUMMARY.txt (and any file with syntax errors) and I will fill Section XV."
