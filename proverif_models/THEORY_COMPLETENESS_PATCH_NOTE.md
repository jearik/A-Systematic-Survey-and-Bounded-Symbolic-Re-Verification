# Theory Completeness Patch Note

This note records the theory-oriented manuscript changes made after the
reviewer criticism on RoR/eCK, PFS, KCI, post-quantum reductions, extended
IIoT adversaries, and asymptotic cost analysis.

## What Was Added to the Manuscript

- Section IV-D, `Conditional Computational-Symbolic Bridge and IIoT Games`.
  This section gives a conditional reduction template:
  `Adv_RoR <= Adv_sym + primitive losses + eps_impl`.
- Explicit PFS and KCI games. The manuscript now defines the relevant oracles,
  freshness condition, failure event, and generic advantage bounds.
- A post-quantum reduction obligation for ML-KEM/ML-DSA-style cross-domain
  AKEs, including QPT adversaries, QROM loss, transcript binding, and primitive
  security terms.
- Extended IIoT adversary games for PUF modeling, semi-honest edge nodes,
  cross-chain relays, and quantum adversaries.
- A new Table XVII with asymptotic computation, communication, storage, and
  dominant scaling risk for each mechanism family.

## Deliberate Claim Boundary

The manuscript still should not claim a complete RoR/eCK proof for every
surveyed protocol or for every abstract model. The correct claim is narrower:

- The three-tool artifact provides executable symbolic evidence for the encoded
  AKE skeletons.
- The new theory section explains how such evidence can be connected to a
  computational proof only under explicit primitive-security, transcript-
  binding, implementation, and trust-substrate assumptions.
- ML-KEM/ML-DSA discussion is a proof obligation and reduction template, not a
  new proof of a concrete post-quantum cross-domain protocol.

## Rebuttal Wording

The revised manuscript does not assert that symbolic verification implies
computational security. It now states a conditional bridge and gives explicit
advantage terms for the symbolic abstraction, primitive reductions, hash/KDF
losses, and unmodeled implementation or substrate assumptions. This directly
addresses the reviewer concern while preserving the paper's identity as a
survey plus reproducible symbolic re-verification framework rather than a new
protocol-proof paper.
