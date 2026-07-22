# Model Scope and v15.3F Evidence Correction

This notice supersedes any v15.3E wording that interpreted the six family
files as semantic cross-tool replications of six mechanism algorithms.

## M1 ProVerif correction

In the v15.3E source, the initiator checked a responder signature over
`(pkB,pkA,X,Y)`, whereas the responder signed only `(pkB,pkA)`. The honest
initiator therefore could not continue past the signature match. The source in
this archive signs the four-field transcript. The recorded v15.3E aggregate M1
PASS log predates that correction and is withdrawn. Query-specific ProVerif
2.05 reruns in `reachability_checks/` give:

- honest-completion witness: PASS;
- initiator and responder payload secrecy: PASS;
- responder acceptance implies an injective initiator run: PASS;
- initiator acceptance implies an injective responder run: TIMEOUT at 120 s.

The corrected M1 result is therefore partial and must not be summarized as an
all-properties PASS.

## Tamarin and Scyther scope

The M1-M6 Tamarin files use idealized internal-state rules and fresh session
atoms. They do not encode the same certificate, DH, certificateless, ledger,
PUF, or ZK message semantics as the ProVerif files. In particular, the M3 lemma
named `pfs_after_kgc_reveal` checks non-disclosure of a fresh session atom that
is independent of the revealed KGC master material; it is not a valid PFS test.

The Scyther files are compact AKE-style role skeletons. They are not semantic
translations of the ProVerif or Tamarin files. An `Ok` result is therefore
reported only as execution of the encoded Scyther skeleton.

## Seeded-fault scope

The files under `ablation_models/` replace a baseline with an explicit secret
release and/or acceptance-without-run template. They are retained under the
legacy path for reproducibility, but they are parser/runner sanity checks, not
minimal-difference ablations. No causal component effect, false-positive rate,
or false-negative rate is inferred from them.

## Status labels

- `WITHDRAWN`: an earlier result has a source/model validity defect and is not evidence.
- `ILLUSTRATIVE`: the tool executed the encoded skeleton, without an algorithm-level inference.
- `BOUNDED CASE`: a named-paper model supports only the listed message-flow query.
- `PARTIAL`: query-specific reruns contain both PASS and TIMEOUT outcomes.
