# Supplement S5: Theory Derivations and Claim Boundaries

This supplement is a proof-support note for the revised manuscript. It does not claim a universal computational-soundness theorem for ProVerif, Tamarin, or Scyther. It states the exact conditional assumptions under which the symbolic artifact can be read as one term in a computational proof obligation.

## A. Conditional Computational-Symbolic Bridge

Let Pi be a bounded-session cross-domain AKE with parties U_i in domain D_a and U_j in domain D_b. Let ctx = (D_a, D_b, role_i, role_j, epoch, policy, trust-evidence) and sid = H(ctx, messages, fresh contributions). The symbolic abstraction Pi_sym is admissible only when:

- A1: every symbolic encryption, signature, MAC, KEM, hash, and KDF constructor is mapped to a primitive satisfying the matching computational notion;
- A2: every message carrying identity, domain, epoch, policy, relay, or ledger state is included in the signed/MACed or hashed transcript;
- A3: tags or parse domains make message classes disjoint, preventing type-flaw and role-confusion reinterpretation;
- A4: trust-substrate state is represented by an explicit predicate ValidTrust(ctx, epoch), and any missing substrate assumption is charged to eps_substrate;
- A5: implementation failures such as side channels, invalid-curve handling, parser bugs, bad randomness, and state rollback are charged to eps_impl rather than hidden inside the symbolic result.

Game sequence. G0 is the RoR experiment for Pi. G1 aborts on transcript collision, losing at most q_h^2/2^lambda. G2 replaces DH/KEM-derived material by random, losing q_dh Adv_ECCDH + q_kem Adv_IND-CCA^KEM. G3 rejects any forged credential, signature, MAC, ledger proof, or ZK proof, losing the relevant unforgeability/soundness terms. G4 replaces KDF outputs by random, losing q_prf Adv_PRF. G5 is the symbolic reachability/correspondence game for Pi_sym plus explicit eps_substrate and eps_impl events. By the triangle inequality over these game hops:

Adv_RoR^Pi(A) <= Adv_sym^Pi_sym(B) + q_dh Adv_ECCDH + q_kem Adv_IND-CCA^KEM + q_sig Adv_EUF-CMA^Sig + q_mac Adv_SU-CMA^MAC + q_prf Adv_PRF^KDF + q_h^2/2^lambda + eps_substrate + eps_impl.

The bound is conditional. If A2-A5 are false, the bridge is not applicable and the manuscript treats the symbolic result as message-flow evidence only.

## B. Cross-Domain PFS and KCI Games

PFS-CD freshness requires that the tested session key and its matching partner key were not revealed before Test. Long-term keys, KGC partial keys, ledger signing keys, or edge credentials may be corrupted only after the accepted session, unless the specific game intentionally studies stronger exposure. The winning condition is distinguishing the Test key while preserving freshness. If sid binds both domains, roles, epochs, and fresh peer contributions, the usual loss is bounded by the DH/KEM and PRF terms plus eps_bind. If the session key can be recomputed from long-term credentials and public transcript after corruption, a direct adversary wins by recomputation.

KCI-CD starts with Corrupt(U_i) and asks whether the adversary can make U_i accept peer U_j without a matching Running(U_j,U_i,sid,k). The cross-domain extension adds that the peer domain, trust anchor, relay/ledger evidence, and policy context must be inside sid. If any of these terms is omitted, a substitution adversary can replay or swap the peer's trust evidence while preserving ordinary secrecy.

## C. Extended IIoT Adversaries

PUF modeling is parameterized by q_c challenge-response observations and tolerance tau. A wins if it predicts a fresh response within tau; the residual term Adv_PUF(q_c,tau) must be carried into any AKE bound using the PUF as a root of trust.

Semi-honest edge adversaries follow the forwarding/cache algorithm but try to distinguish keys, identities, or link relations from the ideal view. The loss term eps_edge captures cache freshness, enclave assumptions, and edge credential protection.

Cross-chain relay adversaries control ordering, delay, stale proofs, and fork visibility. A win occurs if a party accepts trust evidence not final in the source chain at the accepted epoch. This contributes eps_consensus and eps_finality terms that ordinary AKE secrecy does not model.

Quantum adversaries replace PPT algorithms with QPT algorithms. Hash and KDF reasoning must be stated in QROM-style terms, and post-quantum claims must name the exact ML-KEM/ML-DSA parameter set and binding transcript.

## D. Complexity Derivation

The table `S5_COMPLEXITY_DERIVATION.csv` derives each asymptotic entry in Table XVII from the number of cryptographic operations, proof depth, chain count, ring size, circuit size, PUF enrollment size, or lattice dimension. This is a structural upper-bound analysis, not an embedded-device measurement.
