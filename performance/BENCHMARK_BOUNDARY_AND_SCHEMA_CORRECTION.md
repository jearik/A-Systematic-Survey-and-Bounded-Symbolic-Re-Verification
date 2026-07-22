# Benchmark boundary and schema correction

- Source raw SHA-256 before label normalization: `42ff3a17f9480069f35c0cd8f2d4db5e0979ed48dc90319e1cd52a81aa6e653d`.
- Rows: 750; operations: 25; repeated outer samples per operation: 30.
- Normalized category labels in 420 raw rows from `ledger` to `hash_path`; numeric values were not changed.
- The Merkle-style rows are sequential SHA-256 loops. They do not implement a Merkle proof, authenticated tree, blockchain, storage, consensus, smart contract, or finality.
- The timing rows measure primitives on one captured Windows/Python environment. The original run did not capture a validated CPU identity or cryptographic backend version, so the results are illustrative and are not transferred to an IIoT device.
