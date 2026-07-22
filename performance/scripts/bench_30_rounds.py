#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import statistics
import time
from pathlib import Path

from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa, x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

ROUNDS = 30
MSG = os.urandom(256)


def time_op(fn, n: int, warmup: int = 20) -> float:
    for _ in range(warmup):
        fn()
    t0 = time.perf_counter_ns()
    for _ in range(n):
        fn()
    t1 = time.perf_counter_ns()
    return (t1 - t0) / n / 1000.0  # us/op


def summarize(values: list[float]) -> dict[str, float | int]:
    return {
        "rounds": len(values),
        "mean_us": statistics.mean(values),
        "std_us": statistics.stdev(values) if len(values) > 1 else 0.0,
        "median_us": statistics.median(values),
        "min_us": min(values),
        "max_us": max(values),
    }


def hash_path_lookup(n_state: int) -> None:
    depth = max(1, math.ceil(math.log2(n_state)))
    x = b"x" * 32
    for i in range(depth):
        x = hashlib.sha256(x + i.to_bytes(4, "little")).digest()


def hash_path_update(n_state: int) -> None:
    depth = max(1, math.ceil(math.log2(n_state))) + 2
    x = b"w" * 32
    for i in range(depth):
        x = hashlib.sha256(x + b"|" + i.to_bytes(4, "little")).digest()


def main() -> None:
    raw_rows: list[dict[str, str | int | float]] = []

    sk = ec.generate_private_key(ec.SECP256R1())
    pk = sk.public_key()
    sig = sk.sign(MSG, ec.ECDSA(hashes.SHA256()))
    sk2 = ec.generate_private_key(ec.SECP256R1())
    pk2 = sk2.public_key()
    xsk = x25519.X25519PrivateKey.generate()
    xpk2 = x25519.X25519PrivateKey.generate().public_key()
    key = os.urandom(32)
    aes = AESGCM(os.urandom(16))
    nonce = b"\x00" * 12
    ct = aes.encrypt(nonce, MSG, None)
    rk = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rpk = rk.public_key()
    rsig = rk.sign(MSG, padding.PKCS1v15(), hashes.SHA256())

    def do_sha() -> None:
        h = hashes.Hash(hashes.SHA256())
        h.update(MSG)
        h.finalize()

    def do_hmac() -> None:
        h = hmac.HMAC(key, hashes.SHA256())
        h.update(MSG)
        h.finalize()

    operations: list[tuple[str, str, int, object]] = [
        ("crypto", "SHA-256 (256 B)", 2000, do_sha),
        ("crypto", "HMAC-SHA256 (256 B)", 2000, do_hmac),
        ("crypto", "AES-128-GCM encrypt (256 B)", 2000, lambda: aes.encrypt(nonce, MSG, None)),
        ("crypto", "AES-128-GCM decrypt (256 B)", 2000, lambda: aes.decrypt(nonce, ct, None)),
        ("crypto", "ECDSA-P256 sign", 300, lambda: sk.sign(MSG, ec.ECDSA(hashes.SHA256()))),
        ("crypto", "ECDSA-P256 verify", 300, lambda: pk.verify(sig, MSG, ec.ECDSA(hashes.SHA256()))),
        ("crypto", "ECDH-P256 shared secret", 300, lambda: sk.exchange(ec.ECDH(), pk2)),
        ("crypto", "ECC-P256 key generation", 80, lambda: ec.generate_private_key(ec.SECP256R1())),
        ("crypto", "X25519 shared secret", 600, lambda: xsk.exchange(xpk2)),
        ("crypto", "RSA-2048 sign", 50, lambda: rk.sign(MSG, padding.PKCS1v15(), hashes.SHA256())),
        ("crypto", "RSA-2048 verify", 300, lambda: rpk.verify(rsig, MSG, padding.PKCS1v15(), hashes.SHA256())),
    ]
    for n_state in [1, 10, 50, 100, 200, 500, 1000]:
        operations.append(("hash_path", f"Merkle-style hash-path lookup N={n_state}", 1000, lambda n=n_state: hash_path_lookup(n)))
        operations.append(("hash_path", f"Merkle-style hash-path update N={n_state}", 1000, lambda n=n_state: hash_path_update(n)))

    grouped: dict[str, list[float]] = {name: [] for _, name, _, _ in operations}
    categories: dict[str, str] = {name: category for category, name, _, _ in operations}
    inner_n: dict[str, int] = {name: n for _, name, n, _ in operations}

    for round_id in range(1, ROUNDS + 1):
        for category, name, n, fn in operations:
            us = time_op(fn, n)
            grouped[name].append(us)
            raw_rows.append(
                {
                    "round": round_id,
                    "category": category,
                    "operation": name,
                    "inner_iterations": n,
                    "mean_us": us,
                }
            )

    summary_rows = []
    summary_json = {
        "meta": {
            "rounds": ROUNDS,
            "payload": "256-byte message for cryptographic primitives",
            "platform": platform.platform(),
            "python": platform.python_version(),
            "note": "Entries are repeated SHA-256 operations along a Merkle-style path; no live ledger, storage I/O, consensus, or finality is measured.",
        },
        "results": {},
    }
    for name, values in grouped.items():
        s = summarize(values)
        summary_json["results"][name] = {
            "category": categories[name],
            "inner_iterations": inner_n[name],
            **s,
        }
        summary_rows.append(
            {
                "category": categories[name],
                "operation": name,
                "rounds": ROUNDS,
                "inner_iterations": inner_n[name],
                "mean_us": f"{s['mean_us']:.4f}",
                "std_us": f"{s['std_us']:.4f}",
                "median_us": f"{s['median_us']:.4f}",
                "min_us": f"{s['min_us']:.4f}",
                "max_us": f"{s['max_us']:.4f}",
            }
        )

    raw_csv = OUT / "bench_30_rounds_raw.csv"
    with raw_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["round", "category", "operation", "inner_iterations", "mean_us"])
        w.writeheader()
        w.writerows(raw_rows)

    summary_csv = OUT / "bench_30_rounds_summary.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "category",
                "operation",
                "rounds",
                "inner_iterations",
                "mean_us",
                "std_us",
                "median_us",
                "min_us",
                "max_us",
            ],
        )
        w.writeheader()
        w.writerows(summary_rows)

    summary_json_path = OUT / "bench_30_rounds_summary.json"
    summary_json_path.write_text(json.dumps(summary_json, indent=2), encoding="utf-8")

    md = OUT / "bench_30_rounds_summary.md"
    with md.open("w", encoding="utf-8") as f:
        f.write("# 30-Round Benchmark Summary\n\n")
        f.write("All values are microseconds per operation, summarized across 30 independent outer rounds.\n\n")
        f.write("| Category | Operation | Mean us | Std us | Median us |\n")
        f.write("|---|---|---:|---:|---:|\n")
        for row in summary_rows:
            f.write(
                f"| {row['category']} | {row['operation']} | {row['mean_us']} | {row['std_us']} | {row['median_us']} |\n"
            )

    print(f"raw={raw_csv}")
    print(f"summary={summary_csv}")
    print(f"json={summary_json_path}")


if __name__ == "__main__":
    main()
