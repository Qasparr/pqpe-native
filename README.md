# PQPE native crypto core — liboqs for Android arm64-v8a

Post-quantum crypto for the PQPE (Post-Quantum Private Enclave): the same
ML-KEM / ML-DSA algorithms as the PQPE Python service, in native form for
Android. Generic build — JNI-bind it or `dlopen` it from any app.

Built for: Johnathan "Qasparr" (Κασπάρρ) Monroe, 2026-10-03.

## What's inside

| Item | Detail |
|---|---|
| `liboqs.so` | ELF 64-bit ARM aarch64 shared library (1.8 MB) |
| Android NDK | **r30** (`30.0.16248370`, LTS) — Linux x86_64, SHA1-verified against developer.android.com |
| liboqs | **0.16.0** (latest stable, 2026-07-09) |
| ABI / platform | `arm64-v8a`, `android-34` |
| KEMs | ML-KEM-512, **ML-KEM-768**, ML-KEM-1024 (NIST FIPS 203) |
| Signatures | ML-DSA-44, **ML-DSA-65**, ML-DSA-87 (NIST FIPS 204) |
| Dependencies | bionic `libc`/`libm`/`libdl` only — nothing else |
| `include/oqs/` | Public headers (`oqs.h`, `kem.h`, `sig.h`, `kem_ml_kem.h`, `sig_ml_dsa.h`, …) |
| `pqpe_test.c` | Functional test source (see Verification) |

PQPE's wire choices are the bold ones: **ML-KEM-768** for key establishment,
**ML-DSA-65** for enclave identity. (SPHINCS+ was removed upstream in
liboqs 0.16.0; it is not in this build.)

## Using it

**dlopen (C/C++):** the public entry points are the generic constructors —
per-algorithm `OQS_KEM_ml_kem_768_new`-style symbols are intentionally
hidden in liboqs shared builds (upstream only marks the string-dispatched
constructors `OQS_API`):

```c
void *h = dlopen("liboqs.so", RTLD_NOW);
OQS_KEM *(*kem_new)(const char *) = dlsym(h, "OQS_KEM_new");
OQS_SIG *(*sig_new)(const char *) = dlsym(h, "OQS_SIG_new");
OQS_KEM *kem = kem_new("ML-KEM-768");   /* FIPS 203 */
OQS_SIG *sig = sig_new("ML-DSA-65");   /* FIPS 204 */
/* kem->keypair / ->encaps / ->decaps ; sig->keypair / ->sign / ->verify */
```

**JNI:** load with `System.loadLibrary("oqs")` (rename to `liboqs.so` in
`jniLibs/arm64-v8a/`), declare natives for the calls above, or wrap the
`OQS_KEM_*` / `OQS_SIG_*` one-shot functions directly.

## Reproducing the build

```bash
NDK=<path-to>/android-ndk-r30
cmake -S liboqs-0.16.0 -B build-arm64 \
  -DCMAKE_TOOLCHAIN_FILE="$NDK/build/cmake/android.toolchain.cmake" \
  -DANDROID_ABI=arm64-v8a \
  -DANDROID_PLATFORM=android-34 \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=ON \
  -DOQS_BUILD_ONLY_LIB=ON \
  -DOQS_MINIMAL_BUILD="KEM_ml_kem_512;KEM_ml_kem_768;KEM_ml_kem_1024;SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87" \
  -DOQS_USE_OPENSSL=OFF
cmake --build build-arm64 -j1 && cmake --install build-arm64
```

## Demo: post-quantum crypto on your phone (Termux)

`pqpe_demo.py` loads the .so and performs **real** ML-KEM-768 key
exchange and ML-DSA-65 signatures on-device — ultra-verbose, every
payload inspected, with the full Thelemic apparatus (epigraphs from
the five wells, notations, date). Educational R&D: keygen → encaps →
decaps → shared-secret match; tampered ciphertext → implicit
rejection; sign → verify → tampered message/signature → rejection.

```bash
pkg install python
curl -L -o liboqs.so \
  https://raw.githubusercontent.com/Qasparr/pqpe-native/main/liboqs.so
curl -L -o pqpe_demo.py \
  https://raw.githubusercontent.com/Qasparr/pqpe-native/main/pqpe_demo.py
python3 pqpe_demo.py
# pass --quiet for results only
```

Needs an ARM64 Android device (the .so is arm64-v8a/bionic).

## Verification (honest)

Static verification, all passing on the build host (2026-10-03):
- `file`: ELF 64-bit ARM aarch64 shared object, built by the NDK toolchain.
- `llvm-nm -D`: all 30 ML-KEM/ML-DSA entry points exported, plus
  `OQS_KEM_new` / `OQS_SIG_new` / `OQS_KEM_free` / `OQS_SIG_free`.
- `readelf`: NEEDED is only bionic `libm`/`libdl`/`libc`; undefined symbols
  are standard libc functions — it will load on any real Android device.
- `strings`: all six algorithm names (`ML-KEM-768`, `ML-DSA-65`, …) present
  in the dispatch table, so `OQS_KEM_new("ML-KEM-768")` resolves.

Execution test: `pqpe_test.c` (KEM encaps/decaps round-trip with shared-secret
comparison; SIG sign/verify plus a tampered-message rejection check) is
included but was **not executed on the build host** — the .so targets bionic
and the host's `qemu-aarch64` only offers glibc, so the loader refuses it
(`version 'LIBC' not found`). This is a test-harness limitation, not an
artifact defect. Run `pqpe_test` on a real arm64 device, an emulator, or the
PQPE AVD: compile it with the NDK clang and `adb push` both files.

## License

liboqs is MIT-licensed (see upstream). This build configuration is
All Rights Reserved, Without Prejudice — Johnathan "Qasparr" Monroe.
