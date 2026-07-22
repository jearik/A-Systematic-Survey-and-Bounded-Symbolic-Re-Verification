#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$ROOT/results_published_protocols"
C2="$ROOT/published_protocol_models/clbasa_wang2022"
C1="$ROOT/published_protocol_models/ccap_tong2022"
C3="$ROOT/published_protocol_models/bcae_zhang2024"
mkdir -p "$OUT"

PROVERIF_BIN="${PROVERIF_BIN:-proverif}"
SCYTHER_BIN="${SCYTHER_BIN:-scyther}"

run_and_log() {
  local label="$1"
  shift
  local log="$OUT/${label}.log"
  echo "[RUN] $label"
  { time "$@"; } >"$log" 2>&1 || {
    echo "[FAIL] $label (see $log)"
    return 1
  }
  echo "[OK] $label -> $log"
}

run_and_log_keep_status() {
  local label="$1"
  shift
  local log="$OUT/${label}.log"
  echo "[RUN] $label"
  set +e
  { time "$@"; } >"$log" 2>&1
  local code=$?
  set -e
  echo "[DONE:$code] $label -> $log"
}

run_and_log clbasa_wang2022_proverif \
  "$PROVERIF_BIN" "$C2/clbasa_wang2022.pv"

run_and_log clbasa_wang2022_transcript_bound_fix_proverif \
  "$PROVERIF_BIN" "$C2/clbasa_wang2022_transcript_bound_fix.pv"

run_and_log_keep_status clbasa_wang2022_direct_auth_scyther \
  "$SCYTHER_BIN" --max-runs=4 "$C2/clbasa_wang2022_direct_auth.spdl"

run_and_log_keep_status clbasa_wang2022_direct_auth_fix_scyther \
  "$SCYTHER_BIN" --max-runs=4 "$C2/clbasa_wang2022_direct_auth_fix.spdl"

run_and_log ccap_tong2022_proverif \
  "$PROVERIF_BIN" "$C1/ccap_tong2022.pv"

run_and_log ccap_tong2022_replay_cache_fix_proverif \
  "$PROVERIF_BIN" "$C1/ccap_tong2022_replay_cache_fix.pv"

run_and_log bcae_zhang2024_proverif \
  "$PROVERIF_BIN" "$C3/bcae_zhang2024.pv"

echo
echo "Key ProVerif verdicts:"
grep -h '^RESULT\|^Query ' "$OUT"/*_proverif.log || true
echo
echo "Key Scyther verdicts:"
grep -h '^claim' "$OUT"/clbasa_wang2022_direct_auth*_scyther.log || true
