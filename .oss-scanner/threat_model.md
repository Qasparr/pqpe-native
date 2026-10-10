# Threat model — pqpe-native

> "The first principle is that you must not fool yourself — and you are the
> easiest person to fool." — Richard Feynman, *Cargo Cult Science* (1974)

*Date: 2026-10-10 — 93 — Johnathan 'Qasparr' (Κασπάρρ) Monroe,
Keeper of the Secret Treasure. All Rights Reserved, Without Prejudice.*

## What this project is

`pqpe-native` is the native post-quantum crypto core for the PQPE
(Post-Quantum Private Enclave): liboqs **0.16.0**, built with Android NDK
**r30** for **arm64-v8a** (`android-34`), minimal algorithm set —
**ML-KEM-512/768/1024** (NIST FIPS 203) and **ML-DSA-44/65/87**
(NIST FIPS 204). Consumed via `dlopen` or JNI. PQPE's wire choices are the
bold pair: **ML-KEM-768** for key establishment, **ML-DSA-65** for enclave
identity. The hybrid pairing (X25519+ML-KEM-768 / Ed25519+ML-DSA-65) lives
in the PQPE service layer above this library; this `.so` is the pure
post-quantum core.

Doctrine (his red-pen ruling, 2026-10-05): **no fake crypto ships, ever.**
A finding that this build silently downgrades, substitutes classical-only
primitives, or mislabels what it implements is to be treated as
**critical** — it violates the project's founding rule, not just a bug
class.

## Where untrusted input enters

1. **Peer-supplied cryptographic material** — public keys, ciphertexts, and
   signatures handed to `OQS_KEM_decaps` / `OQS_SIG_verify` by remote
   parties. This is the primary attack surface: malformed inputs must fail
   closed (decaps implicit rejection, verify rejection), never leak key
   material or panic the host.
2. **The dlopen/JNI boundary** — the host app supplies key material and
   message buffers. The library must not trust buffer lengths it did not
   derive from the algorithm's own `length_*` fields.
3. **The build supply chain** — the NDK tarball and the liboqs source
   tarball. Both are SHA1-pinned in `.oss-scanner/Dockerfile`; a mismatch
   fails the build loudly. Findings of *unpinned or drifting* fetches are
   in scope and welcome.

## Severity guidance (how he rates reports)

- **Critical:** memory-safety violation or key-recovery in KEM decaps /
  SIG verify paths; silent algorithm downgrade or mislabeling (the
  no-fake-crypto rule); build fetches that can be redirected or
  substituted without detection.
- **High:** side-channel leakage of key material reachable from the
  documented API; integer issues in length handling at the JNI/dlopen
  boundary.
- **Medium:** robustness failures that fail open instead of closed;
  missing validation the API contract implies.
- **Low / informational:** issues confined to `pqpe_demo.py` (the
  educational Termux demo — it is documentation, not shipped code);
  style, dead code, or theoretical concerns with no reachable path.

## Out of scope

- The **prebuilt `liboqs.so` at the repo root** — it is a convenience copy
  of a build artifact. The source build in the Dockerfile is canonical;
  audit the source, not the copy.
- **Android OS / bionic libc** itself, and the NDK toolchain's internals
  (Google's code, not his).
- `liboqs` **upstream** algorithmic internals *as mathematics* — but
  findings in the vendored 0.16.0 *code as built here* are in scope, and
  anything confirmed should also go upstream to open-quantum-safe.

## Report preferences

Reproducer + explanation + candidate patch, as the scanner provides.
Severity assessed against the guidance above, not against a generic
scanner default. He triages every finding through TRVVTH — run the
reproducer before trusting the label.
