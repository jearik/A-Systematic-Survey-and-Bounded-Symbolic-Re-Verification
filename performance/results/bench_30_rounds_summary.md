# Thirty-round host micro-benchmark summary

Values are microseconds per operation across 30 repeated outer samples. These samples are not independent devices or network experiments.

| Category | Operation | Mean us | SD us | Median us | Min us | Max us |
|---|---|---:|---:|---:|---:|---:|
| crypto | SHA-256 (256 B) | 1.147563 | 0.043266 | 1.134000 | 1.071400 | 1.247850 |
| crypto | HMAC-SHA256 (256 B) | 1.681928 | 0.065599 | 1.658925 | 1.590300 | 1.819450 |
| crypto | AES-128-GCM encrypt (256 B) | 0.603877 | 0.035755 | 0.590250 | 0.564050 | 0.712950 |
| crypto | AES-128-GCM decrypt (256 B) | 0.641438 | 0.104491 | 0.616300 | 0.577950 | 1.158250 |
| crypto | ECDSA-P256 sign | 19.536422 | 1.012829 | 19.181000 | 18.342667 | 22.282000 |
| crypto | ECDSA-P256 verify | 50.630122 | 1.997665 | 50.045000 | 48.348000 | 55.439667 |
| crypto | ECDH-P256 shared secret | 37.753267 | 1.411301 | 37.515333 | 35.820667 | 40.754000 |
| crypto | ECC-P256 key generation | 12.633875 | 1.295566 | 12.211875 | 11.621250 | 17.051250 |
| crypto | X25519 shared secret | 23.085583 | 0.909673 | 22.811833 | 22.013000 | 26.021333 |
| crypto | RSA-2048 sign | 421.620267 | 13.388873 | 422.289000 | 400.258000 | 453.430000 |
| crypto | RSA-2048 verify | 17.184489 | 1.105777 | 16.947833 | 15.985333 | 19.846000 |
| hash_path | Merkle-style hash-path lookup N=1 | 0.845077 | 0.054081 | 0.820450 | 0.790200 | 0.968700 |
| hash_path | Merkle-style hash-path update N=1 | 2.154570 | 0.076743 | 2.139050 | 2.038200 | 2.343600 |
| hash_path | Merkle-style hash-path lookup N=10 | 2.635497 | 0.104880 | 2.631850 | 2.493200 | 2.968800 |
| hash_path | Merkle-style hash-path update N=10 | 4.062887 | 0.311643 | 3.967350 | 3.804900 | 5.441200 |
| hash_path | Merkle-style hash-path lookup N=50 | 3.902013 | 0.202870 | 3.871000 | 3.634000 | 4.320100 |
| hash_path | Merkle-style hash-path update N=50 | 5.328410 | 0.283817 | 5.295950 | 4.949900 | 6.281400 |
| hash_path | Merkle-style hash-path lookup N=100 | 4.463183 | 0.191976 | 4.443650 | 4.198500 | 4.955400 |
| hash_path | Merkle-style hash-path update N=100 | 6.066840 | 0.844655 | 5.890600 | 5.573800 | 10.372400 |
| hash_path | Merkle-style hash-path lookup N=200 | 5.167520 | 0.643880 | 5.046700 | 4.773800 | 8.433600 |
| hash_path | Merkle-style hash-path update N=200 | 6.653283 | 0.561912 | 6.483750 | 6.183000 | 8.570700 |
| hash_path | Merkle-style hash-path lookup N=500 | 5.761297 | 0.491926 | 5.632100 | 5.353800 | 7.367800 |
| hash_path | Merkle-style hash-path update N=500 | 7.212803 | 0.413241 | 7.133850 | 6.696900 | 8.923100 |
| hash_path | Merkle-style hash-path lookup N=1000 | 6.234393 | 0.233687 | 6.219400 | 5.926700 | 6.707300 |
| hash_path | Merkle-style hash-path update N=1000 | 7.834383 | 0.434534 | 7.658450 | 7.375200 | 9.213600 |
