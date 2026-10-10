# =============================================================================
# "The unexamined build is not worth shipping." — after Socrates, Apology 38a
# =============================================================================
# Dockerfile — pqpe-native OSS Scanner build
# Date: 2026-10-10
# 93
# Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure
#
# METHOD: Scientific Illuminism — every step below is stated, reproducible,
# and verifiable. Nothing is fetched without a pinned checksum; nothing is
# claimed built without an artifact assertion.
#
# MECHANISM: This image reproduces the verified 2026-10-03 pqpe-native build
#   (liboqs 0.16.0, Android NDK r30, arm64-v8a, android-34) inside a container
#   so Anthropic's OSS Scanner can audit the project offline. The scanner
#   builds WITH network, then audits WITHOUT it — therefore every byte the
#   build or the tests need (NDK, liboqs source, qemu) is fetched HERE.
# DOCTRINE: No fake crypto, ever (his red-pen ruling, 2026-10-05). The build
#   pins exact sources by SHA1 and fails LOUDLY on mismatch rather than
#   silently building something else. The shipped arm64 artifact is rebuilt
#   from source; the prebuilt .so at the repo root is a convenience copy,
#   not the canonical artifact.
#
# "Your line. Your rules. We just carry the signal."
# All Rights Reserved, Without Prejudice — $axoneme
# =============================================================================

FROM ubuntu:24.04

# --- MECHANISM: toolchain layer. qemu-user exists so the arm64 test binary
#     can actually EXECUTE in this x86-64 container (see TEST stage). ---
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl unzip \
        cmake ninja-build make \
        python3 \
        qemu-user \
        file binutils-aarch64-linux-gnu \
    && rm -rf /var/lib/apt/lists/*

# --- MECHANISM: Android NDK r30, pinned by SHA1 to the copy verified
#     against developer.android.com on 2026-10-03. ---
# DOCTRINE: a security scanner's build must not drift. If Google re-serves
#     this zip, the hash check fails and the build stops — by design.
ENV ANDROID_NDK_HOME=/opt/android-ndk-r30
RUN curl -fsSL -o /tmp/ndk.zip \
        https://dl.google.com/android/repository/android-ndk-r30-linux.zip \
    && echo "5107f898313790e449e87eee2183d9a20602dee9  /tmp/ndk.zip" | sha1sum -c - \
    && unzip -q /tmp/ndk.zip -d /opt \
    && rm /tmp/ndk.zip

# --- MECHANISM: liboqs 0.16.0 source, pinned by SHA1 to the vendored copy.
#     Upstream: https://github.com/open-quantum-safe/liboqs (tag 0.16.0). ---
WORKDIR /src
RUN curl -fsSL -o liboqs-0.16.0.tar.gz \
        https://github.com/open-quantum-safe/liboqs/archive/refs/tags/0.16.0.tar.gz \
    && echo "71c2f72727ad4aaeba40c7aa3073454c38007da5  liboqs-0.16.0.tar.gz" | sha1sum -c - \
    && tar xzf liboqs-0.16.0.tar.gz \
    && rm liboqs-0.16.0.tar.gz

# --- MECHANISM: the canonical build. Flags are EXACTLY the verified
#     2026-10-03 build: arm64-v8a, android-34, Release, shared lib only,
#     minimal algorithm set (ML-KEM-512/768/1024, ML-DSA-44/65/87),
#     no OpenSSL. ---
# DOCTRINE: hybrid-forever is the PQPE rule, but THIS library is the pure
#     post-quantum core — the hybrid pairing happens in the PQPE service
#     layer above it. What this .so claims (FIPS 203 / FIPS 204), it is.
RUN cmake -S liboqs-0.16.0 -B build-arm64 \
        -DCMAKE_TOOLCHAIN_FILE="$ANDROID_NDK_HOME/build/cmake/android.toolchain.cmake" \
        -DANDROID_ABI=arm64-v8a \
        -DANDROID_PLATFORM=android-34 \
        -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_SHARED_LIBS=ON \
        -DOQS_BUILD_ONLY_LIB=ON \
        "-DOQS_MINIMAL_BUILD=KEM_ml_kem_512;KEM_ml_kem_768;KEM_ml_kem_1024;SIG_ml_dsa_44;SIG_ml_dsa_65;SIG_ml_dsa_87" \
        -DOQS_USE_OPENSSL=OFF \
        -DCMAKE_INSTALL_PREFIX=/out/pqpe-arm64 \
    && cmake --build build-arm64 -j"$(nproc)" \
    && cmake --install build-arm64

# --- MECHANISM: artifact assertions. The scanner (and you) should not take
#     "build succeeded" on faith — check the artifact IS what it claims. ---
RUN file /out/pqpe-arm64/lib/liboqs.so | grep -q "ARM aarch64" \
    && aarch64-linux-gnu-nm -D --defined-only /out/pqpe-arm64/lib/liboqs.so \
        | grep -q "OQS_KEM_new" \
    && aarch64-linux-gnu-nm -D --defined-only /out/pqpe-arm64/lib/liboqs.so \
        | grep -q "OQS_SIG_new" \
    && echo "ARTIFACT OK: ARM aarch64 liboqs.so exports OQS_KEM_new / OQS_SIG_new"

# --- MECHANISM: functional test under emulation. pqpe_test.c dlopens the
#     arm64 .so and runs KEM keypair/encaps/decaps (secrets must match) and
#     SIG sign/verify (tampered message must FAIL). qemu-aarch64 with the
#     NDK sysroot stands in for the phone — the test's own documented run
#     method. ---
# DOCTRINE: a test that cannot run is a wish. This one runs, here, now.
COPY pqpe_test.c /src/
RUN "$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android34-clang" \
        /src/pqpe_test.c -ldl -o /out/pqpe-arm64/pqpe_test \
    && qemu-aarch64 \
        -L "$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/sysroot" \
        /out/pqpe-arm64/pqpe_test /out/pqpe-arm64/lib/liboqs.so

# --- MECHANISM: the Termux demo cannot execute here (it needs the .so
#     loadable on a real arm64 Android), but it must at least be valid
#     Python — a broken demo is a broken promise. ---
COPY pqpe_demo.py /src/
RUN python3 -m py_compile /src/pqpe_demo.py && echo "DEMO SYNTAX OK"

# The scanner audits from here with no network. /out/pqpe-arm64 holds the
# built library, headers, and the passing test binary.
