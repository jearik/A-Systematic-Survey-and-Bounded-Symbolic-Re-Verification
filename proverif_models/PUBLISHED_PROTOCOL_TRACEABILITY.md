# Published Protocol Re-Verification Traceability

## C2 - CL-BASA Wang et al. 2022

**Local source PDF**

`<PROJECT_ROOT>\re\A Certificateless-Based Authentication and Key Agreement Scheme for IIoT Cross-Domain.pdf`

**Bibliographic identity**

X. Wang, C. Gu, F. Wei, S. Lu, and Z. Li, "A Certificateless-Based
Authentication and Key Agreement Scheme for IIoT Cross-Domain", Security and
Communication Networks, 2022, DOI: 10.1155/2022/3693748.

## Message-to-model mapping

| Paper item | Paper content modeled | ProVerif encoding |
|---|---|---|
| Figure 3, steps 5-6 | U asks BAS_A for domain B parameters and V's public information | `User_U` sends `(pidU, pidV, reqinfA)` on private `chA`; `BASA_directory` returns `(pidV, domB, pkV)` |
| Section 5.2.2 | BAS_A/BAS_B use secure channels for information responses | Private channels `chA` and `chB` |
| Eq. (4), Token_UV | `NU || IDdomainA || PIDU || TextU || Sign_SkU(...)`; Figure 7 sets `mU = NU || IDdomainA || PIDU || Pk'_U` | `packU(nU, domA, pidU, epkU)` and `sign(packU(...), skU)` |
| Figure 6 | `Pk'_U = r'_U P`, `Pk'_V = r'_V P`, shared key `r'_U r'_V P` | `gexp(gen,rU)`, `gexp(gen,rV)`, `gexp(epkV,rU) = gexp(epkU,rV)` |
| Section 5.2.2 | V asks BAS_B to validate U's anonymous identity and public key | `User_V` sends `(pidV, pidU, epkU, reqinfB)` on private `chB`; `BASB_directory` returns `(pidU, domA, pkU)` |
| Eq. (4), Token_VU | `NV || IDdomainB || PIDV || TextV || Sign_SkV(...)`; Figure 7 sets `mV = NV || IDdomainB || PIDV || Pk'_V` | `packV(nV, domB, pidV, epkV)` and `sign(packV(...), skV)` |

## Main executable result

The original-flow ProVerif model proves session payload secrecy and BASB
validation correspondence, but finds authentication failures:

- responder-side injective agreement fails because no replay cache is explicit
  for `Token_UV`;
- initiator-side agreement fails because `Token_VU` is not bound to `NU`,
  `PIDU`, or `Pk'_U` in the printed message formula.

The hardening model signs `NU`, `PIDU`, and `Pk'_U` inside `Token_VU`. Under the
same abstraction, ProVerif then proves the initiator-side injective-agreement
query.

## What is not claimed

This artifact does not claim a byte-for-byte implementation of CL-BASA, does not
reuse the authors' original Tamarin source, and does not prove the
certificateless signature scheme in the computational model. It is a
machine-checkable symbolic re-verification of the published authentication and
key-agreement message flow.

## C1 - CCAP Tong et al. 2022

**Local source PDF**

`<PROJECT_ROOT>\re\CCAP A Complete Cross-Domain Authentication Based on Blockchain for Internet of Things.pdf`

**Bibliographic identity**

F. Tong, X. Chen, K. Wang, and Y. Zhang, "CCAP: A Complete Cross-Domain
Authentication Based on Blockchain for Internet of Things", IEEE Transactions
on Information Forensics and Security, vol. 17, pp. 3789-3800, 2022,
DOI: 10.1109/TIFS.2022.3214733.

| Paper item | Paper content modeled | ProVerif encoding |
|---|---|---|
| Section V-C.1 | PAS_A validates the local device and PAS_B issues cross-domain access material | `LicensingAndPseudoGen` emits `LicensingIssued` before pseudonym generation |
| Section V-C.2, steps 8-15 | Device chooses `pid` and `PK'_Ai`; VS nodes verify proof and update ledger with ballot/timestamp | `PseudoRequest`, `LedgerPseudonymValid`, and private lookup service |
| Algorithm 2 | NIZK proof verification over blacklist and encrypted identity | Abstracted as a private ledger-validation event; equations are not reimplemented |
| Section V-C.3 | Device sends `{Authenticate, pid, Sign_SK'_Ai}`; PAS_B queries ledger and verifies signature | `DeviceAuthenticate` and `PASB_Authenticate` |

Main result: real-identity non-derivability and non-injective authentication
correspondence pass, but injective authentication cannot be proved. This is
consistent with the printed authentication message lacking an explicit nonce,
timestamp, or replay-cache state in the modeled flow.

## C3 - BCAE Zhang et al. 2024

**Local source PDF**

`<PROJECT_ROOT>\re\BCAE A Blockchain-Based Cross Domain Authentication Scheme for Edge Computing.pdf`

**Bibliographic identity**

S. Zhang, Z. Yan, W. Liang, K.-C. Li, and B. Di Martino, "BCAE: A
Blockchain-Based Cross Domain Authentication Scheme for Edge Computing", IEEE
Internet of Things Journal, vol. 11, no. 13, pp. 24035-24048, 2024,
DOI: 10.1109/JIOT.2024.3387934.

| Paper item | Paper content modeled | ProVerif encoding |
|---|---|---|
| Algorithm 1 | BCCA issues digital certificate `(ra,sa)` for `(IDa,Qa)` | `issuecert(idA,qA,ca)` and `BCCARegistered(idA,qA)` |
| Algorithm 3 | ES_B checks whether `IDa` is registered and obtains cross-domain trust evidence | certificate verification plus BCCA registration correspondence |
| Algorithm 4 | Ea sends `Qa, IDa, (ra,sa), N6P, N7P`; Eb sends `N8P, N9P, ENa1, ENa2`; both derive the session key | static and ephemeral DH terms in `kdf(...)`; encrypted response with `senc(respmsg(...),k)` |

Main result: session secrecy, Ea-accepts-implies-Eb-response, and
Eb-accepts-implies-BCCA-registration pass. Eb acceptance does not imply Ea start
or Ea final acceptance under the modeled first-message flow, which exposes a
missing explicit key-confirmation / ephemeral-possession boundary rather than a
claim of full protocol breakage.
