# Published Protocol Re-Verification Models

This folder separates executable models of real published protocols from the
six mechanism templates M1-M6. The purpose is to avoid claiming that a template
is a full reproduction of a paper.

## Current real-protocol cases

### C2: CL-BASA, Wang et al. 2022

Source paper: "A Certificateless-Based Authentication and Key Agreement Scheme
for IIoT Cross-Domain", Security and Communication Networks, 2022,
DOI: 10.1155/2022/3693748.

Modeled source text:

- Section 5.2.2, authentication and key agreement stage.
- Figure 3, information request and response through BAS_A/BAS_B.
- Figure 5 and Eq. (4), Token_UV and Token_VU.
- Figure 6, ECDHE key exchange.
- Figure 7 narrative, U/V authentication and key agreement.

Main files:

- `clbasa_wang2022/clbasa_wang2022.pv`: ProVerif model of the printed flow.
- `clbasa_wang2022/clbasa_wang2022_transcript_bound_fix.pv`: minimal
  transcript-bound hardening experiment.
- `clbasa_wang2022/clbasa_wang2022_direct_auth.spdl`: Scyther direct-token
  projection after ideal BAS lookup.
- `clbasa_wang2022/clbasa_wang2022_direct_auth_fix.spdl`: Scyther projection of
  the transcript-bound variant.

Run from Ubuntu/WSL:

```bash
cd proverif_models
export PATH="$HOME/.opam/default/bin:$HOME/.local/bin:$PATH"
bash run_published_protocols.sh
```

Logs are written to `results_published_protocols/`. The compact summary is
`PUBLISHED_PROTOCOL_REVERIFY_SUMMARY.csv`.

### C1: CCAP, Tong et al. 2022

Source paper: "CCAP: A Complete Cross-Domain Authentication Based on
Blockchain for Internet of Things", IEEE Transactions on Information Forensics
and Security, 2022, DOI: 10.1109/TIFS.2022.3214733.

Modeled source text:

- Section V-C.1, cross-domain licensing.
- Section V-C.2, on-demand pseudo identity generation, steps 8-15.
- Algorithm 2, pseudonym proof verification.
- Section V-C.3, cross-domain authentication with `{Authenticate, pid,
  Sign_SK'_Ai}`.

Main files:

- `ccap_tong2022/ccap_tong2022.pv`: ProVerif model of licensing,
  pseudonym-ledger validation, and Authenticate-token verification.
- `ccap_tong2022/ccap_tong2022_replay_cache_fix.pv`: nonce/cache hardening
  experiment. This remains inconclusive in ProVerif and is kept as evidence
  that replay-state reasoning should be moved to Tamarin rather than forced
  into a false PASS.

### C3: BCAE, Zhang et al. 2024

Source paper: "BCAE: A Blockchain-Based Cross Domain Authentication Scheme for
Edge Computing", IEEE Internet of Things Journal, 2024,
DOI: 10.1109/JIOT.2024.3387934.

Modeled source text:

- Algorithm 1, user registration and blockchain certificate issuance.
- Algorithm 3, cross-domain authentication through ES_A, ES_B, and BCCA.
- Algorithm 4, key agreement with static public keys and N6/N7/N8/N9 elliptic
  curve values.

Main file:

- `bcae_zhang2024/bcae_zhang2024.pv`: ProVerif model of certificate-backed
  cross-domain authorization and static-plus-ephemeral ECDH key agreement.

## Boundary

All published-protocol models are independent symbolic abstractions, not the
authors' original source code. They preserve the source paper's security-relevant
message dependencies and make abstraction boundaries explicit. Pairing/NIZK
equations, DPoS or consortium consensus, threshold tracing, ECES arithmetic,
and implementation parsers are outside these symbolic models unless stated.
