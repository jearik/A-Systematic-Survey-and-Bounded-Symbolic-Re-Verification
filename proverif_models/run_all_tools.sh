#!/usr/bin/env bash
# Unified runner for the ProVerif/Tamarin/AVISPA/Scyther artifact set.
# The script is deliberately conservative: missing tools are reported as SKIP,
# not as successful verification.

set -u

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
RESULTS="$ROOT/results_multitool"
mkdir -p "$RESULTS"
SUMMARY="$RESULTS/SUMMARY.txt"
: > "$SUMMARY"

timestamp() { date '+%Y-%m-%d %H:%M:%S %z'; }

log() {
  printf '%s\n' "$*" | tee -a "$SUMMARY"
}

find_first() {
  for c in "$@"; do
    if command -v "$c" >/dev/null 2>&1; then
      command -v "$c"
      return 0
    fi
  done
  return 1
}

maybe_add_opam() {
  if [ -d "$HOME/.local/bin" ]; then
    PATH="$HOME/.local/bin:$PATH"
    export PATH
  fi
  if [ -d "$HOME/.opam/default/bin" ]; then
    PATH="$HOME/.opam/default/bin:$PATH"
    export PATH
  fi
}

run_and_capture() {
  label="$1"
  outfile="$2"
  shift 2
  log ">>> $label"
  "$@" > "$outfile" 2>&1
  code=$?
  log "exit_code=$code log=$outfile"
  return "$code"
}

log "Multi-tool symbolic verification run: $(timestamp)"
log "root=$ROOT"
log "--------------------------------------------"

maybe_add_opam

PROVERIF="$(find_first proverif || true)"
if [ -n "$PROVERIF" ]; then
  log "ProVerif: $($PROVERIF -help 2>&1 | head -1)"
  for f in "$ROOT"/M*.pv; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .pv)"
    out="$RESULTS/proverif_${name}.txt"
    if run_and_capture "ProVerif $name" "$out" "$PROVERIF" "$f"; then
      grep -E '^RESULT|is true|is false|cannot be proved' "$out" | sed 's/^/  /' | tee -a "$SUMMARY" || true
    else
      grep -E 'Error|error|Syntax|RESULT|cannot be proved|is false' "$out" | head -20 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    fi
    log ""
  done
else
  log "SKIP ProVerif: command not found"
fi

log "--------------------------------------------"
TAMARIN="$(find_first tamarin-prover tamarin || true)"
if [ -n "$TAMARIN" ]; then
  log "Tamarin: $($TAMARIN --version 2>&1 | head -1 || true)"
  for f in "$ROOT"/tamarin_models/*.spthy; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .spthy)"
    out="$RESULTS/tamarin_${name}.txt"
    if run_and_capture "Tamarin $name" "$out" "$TAMARIN" "$f" --prove; then
      grep -Ei 'verified|falsified|analysis incomplete|lemma|summary|error' "$out" | tail -40 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    else
      grep -Ei 'error|parse|unexpected|falsified|incomplete' "$out" | head -40 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    fi
    log ""
  done
else
  log "SKIP Tamarin: tamarin-prover/tamarin command not found"
fi

log "--------------------------------------------"
AVISPA="$(find_first avispa || true)"
HLPSL2IF="$(find_first hlpsl2if || true)"
OFMC="$(find_first ofmc || true)"
CLATSE="$(find_first cl-atse || true)"
if [ -n "$AVISPA" ]; then
  log "AVISPA: $($AVISPA -h 2>&1 | head -1 || true)"
  for f in "$ROOT"/avispa_models/*.hlpsl; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .hlpsl)"
    out="$RESULTS/avispa_${name}.txt"
    run_and_capture "AVISPA $name" "$out" "$AVISPA" "$f"
    grep -Ei 'SUMMARY|SAFE|UNSAFE|INCONCLUSIVE|ERROR|ATTACK|parse' "$out" | tail -60 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    log ""
  done
elif [ -n "$HLPSL2IF" ] && { [ -n "$OFMC" ] || [ -n "$CLATSE" ]; }; then
  log "AVISPA split tools detected: hlpsl2if=$HLPSL2IF ofmc=$OFMC cl-atse=$CLATSE"
  for f in "$ROOT"/avispa_models/*.hlpsl; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .hlpsl)"
    ifile="$RESULTS/${name}.if"
    conv="$RESULTS/avispa_${name}_convert.txt"
    "$HLPSL2IF" "$f" > "$ifile" 2> "$conv"
    if [ -n "$OFMC" ]; then
      out="$RESULTS/ofmc_${name}.txt"
      run_and_capture "OFMC $name" "$out" "$OFMC" "$ifile"
      grep -Ei 'SUMMARY|SAFE|UNSAFE|INCONCLUSIVE|ERROR|ATTACK' "$out" | tail -60 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    fi
    if [ -n "$CLATSE" ]; then
      out="$RESULTS/clatse_${name}.txt"
      run_and_capture "CL-AtSe $name" "$out" "$CLATSE" "$ifile"
      grep -Ei 'SUMMARY|SAFE|UNSAFE|INCONCLUSIVE|ERROR|ATTACK' "$out" | tail -60 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    fi
    log ""
  done
else
  log "SKIP AVISPA: avispa or hlpsl2if+backend commands not found"
fi

log "--------------------------------------------"
SCYTHER="$(find_first scyther-linux scyther || true)"
if [ -n "$SCYTHER" ]; then
  log "Scyther: $($SCYTHER --version 2>&1 | head -1 || true)"
  for f in "$ROOT"/scyther_models/*.spdl; do
    [ -f "$f" ] || continue
    name="$(basename "$f" .spdl)"
    out="$RESULTS/scyther_${name}.txt"
    run_and_capture "Scyther $name" "$out" "$SCYTHER" "$f"
    grep -Ei 'claim|secret|ok|fail|attack|verified|falsified|error|syntax|parse' "$out" | tail -80 | sed 's/^/  /' | tee -a "$SUMMARY" || true
    if grep -q $'\033\\[31mFail' "$out" || grep -Eiq 'error|syntax|parse|attack' "$out"; then
      log "  normalized_status=not-verified-or-needs-inspection"
    elif grep -q $'\033\\[32mOk' "$out" || grep -Eiq 'proof of correctness|Ok' "$out"; then
      log "  normalized_status=verified"
    else
      log "  normalized_status=inconclusive"
    fi
    log ""
  done
else
  log "SKIP Scyther: scyther/scyther-linux command not found"
fi

log "--------------------------------------------"
log "Completed: $(timestamp)"
log "Detailed logs are in $RESULTS"
