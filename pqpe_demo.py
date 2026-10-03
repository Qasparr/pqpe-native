#!/usr/bin/env python3
"""
PQPE NATIVE DEMO — post-quantum cryptography, on your phone.
=============================================================
Loads the NDK-built liboqs.so (ML-KEM-768 + ML-DSA-65) via ctypes
and performs real post-quantum key exchange and signatures,
ultra-verbose, for educational research & development.

Run on-device (Termux):
    pkg install python
    curl -L -o liboqs.so \
      https://raw.githubusercontent.com/Qasparr/pqpe-native/main/liboqs.so
    python3 pqpe_demo.py

Needs: an ARM64 (aarch64) Android device — e.g. the Galaxy A16 5G.
The .so is built for arm64-v8a (bionic); it will not load on x86_64.

IA.'.A.'.M.TRVVTH
All Rights Reserved, Without Prejudice.
Johnathan "Qasparr" (Κασπάρρ) Monroe, Keeper of the Secret Treasure.
"""

import ctypes
import os
import sys
import time

# ---------------------------------------------------------------- apparatus

DATE = "2026-10-03"

EPIGRAPHS = [
    ("Scripture",
     "And I saw in the right hand of him that sat on the throne a book "
     "written within and on the backside, sealed with seven seals.",
     "Revelation 5:1 (KJV)"),
    ("Law",
     "Sealed: authenticated by a seal; executed by the affixing of a seal. "
     "Also made up in any manner so as to be closed against inspection "
     "of the contents.",
     "Black's Law Dictionary (2nd Ed.), s.v. \"Sealed\""),
    ("Philosophy",
     "Three may keep a secret, if two of them are dead.",
     "Benjamin Franklin, Poor Richard's Almanack"),
    ("Hip-hop",
     "I got the keys to all success!",
     "DJ Khaled ft. JAY-Z & Future, \"I Got the Keys\" (2016)"),
    ("Hollywood",
     "Cryptography systems are based on mathematical problems so complex "
     "they cannot be solved without a key. — No, it's the code-breaker. "
     "No more secrets.",
     "Sneakers (1992), dir. Phil Alden Robinson"),
]

# ---------------------------------------------------------------- output

VERBOSE = True  # default: ultra-verbose. Pass --quiet for results only.


def say(s=""):
    print(s)


def head(title):
    say()
    say("=" * 70)
    say(" " + title)
    say("=" * 70)


def sub(title):
    say()
    say("--- " + title + " " + "-" * (64 - len(title)))


def hx(b, n=48):
    """Truncated hex with full length — verbose but not a wall."""
    h = bytes(b).hex()
    return h[:n] + ("..." if len(h) > n else "") + f"  [{len(b)} bytes]"


def note(s):
    if VERBOSE:
        say("    > " + s)


# ---------------------------------------------------------------- library

def find_lib():
    cands = [
        os.environ.get("LIBOQS_SO", ""),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "liboqs.so"),
        os.path.expanduser("~/liboqs.so"),
        "/data/data/com.termux/files/usr/lib/liboqs.so",
    ]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return None


class OQS_KEM(ctypes.Structure):
    _fields_ = [
        ("method_name", ctypes.c_char_p),
        ("alg_version", ctypes.c_char_p),
        ("claimed_nist_level", ctypes.c_uint8),
        ("ind_cca", ctypes.c_bool),
        ("length_public_key", ctypes.c_size_t),
        ("length_secret_key", ctypes.c_size_t),
        ("length_ciphertext", ctypes.c_size_t),
        ("length_shared_secret", ctypes.c_size_t),
    ]


class OQS_SIG(ctypes.Structure):
    _fields_ = [
        ("method_name", ctypes.c_char_p),
        ("alg_version", ctypes.c_char_p),
        ("claimed_nist_level", ctypes.c_uint8),
        ("euf_cma", ctypes.c_bool),
        ("length_public_key", ctypes.c_size_t),
        ("length_secret_key", ctypes.c_size_t),
        ("length_signature", ctypes.c_size_t),
    ]


OQS_SUCCESS = 0


def load():
    path = find_lib()
    if not path:
        say("FATAL: liboqs.so not found.")
        say("Get it:")
        say("  curl -L -o liboqs.so \\")
        say("    https://raw.githubusercontent.com/Qasparr/pqpe-native/main/liboqs.so")
        say("Or set LIBOQS_SO to its path.")
        sys.exit(2)
    lib = ctypes.CDLL(path)
    lib.OQS_KEM_new.restype = ctypes.POINTER(OQS_KEM)
    lib.OQS_KEM_new.argtypes = [ctypes.c_char_p]
    lib.OQS_KEM_free.argtypes = [ctypes.POINTER(OQS_KEM)]
    lib.OQS_KEM_keypair.argtypes = [ctypes.POINTER(OQS_KEM),
                                    ctypes.c_char_p, ctypes.c_char_p]
    lib.OQS_KEM_encaps.argtypes = [ctypes.POINTER(OQS_KEM),
                                   ctypes.c_char_p, ctypes.c_char_p,
                                   ctypes.c_char_p]
    lib.OQS_KEM_decaps.argtypes = [ctypes.POINTER(OQS_KEM),
                                   ctypes.c_char_p, ctypes.c_char_p,
                                   ctypes.c_char_p]
    lib.OQS_SIG_new.restype = ctypes.POINTER(OQS_SIG)
    lib.OQS_SIG_new.argtypes = [ctypes.c_char_p]
    lib.OQS_SIG_free.argtypes = [ctypes.POINTER(OQS_SIG)]
    lib.OQS_SIG_keypair.argtypes = [ctypes.POINTER(OQS_SIG),
                                    ctypes.c_char_p, ctypes.c_char_p]
    lib.OQS_SIG_sign.argtypes = [ctypes.POINTER(OQS_SIG),
                                 ctypes.c_char_p,
                                 ctypes.POINTER(ctypes.c_size_t),
                                 ctypes.c_char_p, ctypes.c_size_t,
                                 ctypes.c_char_p]
    lib.OQS_SIG_verify.argtypes = [ctypes.POINTER(OQS_SIG),
                                   ctypes.c_char_p, ctypes.c_size_t,
                                   ctypes.c_char_p, ctypes.c_size_t,
                                   ctypes.c_char_p]
    for f in ("OQS_KEM_keypair", "OQS_KEM_encaps", "OQS_KEM_decaps",
              "OQS_SIG_keypair", "OQS_SIG_sign", "OQS_SIG_verify"):
        getattr(lib, f).restype = ctypes.c_int
    return lib, path


def timed(label, fn):
    t0 = time.perf_counter()
    out = fn()
    dt = (time.perf_counter() - t0) * 1000.0
    note(f"{label}: {dt:.2f} ms")
    return out


# ---------------------------------------------------------------- demo

def demo_kem(lib):
    head("[§1] KEY ENCAPSULATION — ML-KEM-768  (NIST FIPS 203)")
    note("ML-KEM = Module-Lattice Key Encapsulation Mechanism, née Kyber.")
    note("Security rests on the hardness of Module-LWE: even a quantum")
    note("computer is believed unable to invert it. NIST standardized it")
    note("as FIPS 203 in 2024. -768 is the recommended parameter set.")

    kem = lib.OQS_KEM_new(b"ML-KEM-768")
    if not kem:
        say("FATAL: ML-KEM-768 not available in this build.")
        sys.exit(3)
    K = kem.contents
    sub("parameters (read from the algorithm object itself)")
    say(f"  method_name        : {K.method_name.decode()}")
    say(f"  NIST level         : {K.claimed_nist_level}")
    say(f"  IND-CCA secure     : {bool(K.ind_cca)}")
    say(f"  public key         : {K.length_public_key} bytes")
    say(f"  secret key         : {K.length_secret_key} bytes")
    say(f"  ciphertext         : {K.length_ciphertext} bytes")
    say(f"  shared secret      : {K.length_shared_secret} bytes")
    note("Compare RSA-2048: 256-byte keys, broken by Shor's algorithm on "
         "a large quantum computer. These sizes are the price of "
         "quantum resistance.")

    sub("1a. keypair generation (the device's long-term KEM identity)")
    pk = ctypes.create_string_buffer(K.length_public_key)
    sk = ctypes.create_string_buffer(K.length_secret_key)

    def _kg():
        assert lib.OQS_KEM_keypair(kem, pk, sk) == OQS_SUCCESS
    timed("keygen", _kg)
    say(f"  pk : {hx(pk.raw)}")
    say(f"  sk : {hx(sk.raw)}")
    note("sk never leaves the device. pk is published (cf. /pq/params).")

    sub("1b. encapsulation (sender: encrypt a secret TO pk)")
    ct = ctypes.create_string_buffer(K.length_ciphertext)
    ss1 = ctypes.create_string_buffer(K.length_shared_secret)

    def _enc():
        assert lib.OQS_KEM_encaps(kem, ct, ss1, pk) == OQS_SUCCESS
    timed("encaps", _enc)
    say(f"  ct : {hx(ct.raw)}")
    say(f"  ss : {hx(ss1.raw)}")
    note("The sender now holds ss; the ciphertext travels alone.")

    sub("1c. decapsulation (receiver: recover the secret FROM ct + sk)")
    ss2 = ctypes.create_string_buffer(K.length_shared_secret)

    def _dec():
        assert lib.OQS_KEM_decaps(kem, ss2, ct, sk) == OQS_SUCCESS
    timed("decaps", _dec)
    say(f"  ss': {hx(ss2.raw)}")

    sub("1d. VERDICT — do the two secrets match?")
    match = bytes(ss1.raw) == bytes(ss2.raw)
    say(f"  ss == ss'  : {match}")
    assert match, "KEM round-trip FAILED"
    say("  => Key exchange complete. Both sides share 32 secret bytes")
    say("     no eavesdropper can compute — not even with a quantum")
    say("     computer. This is the PQ half of the PQPE handshake.")
    lib.OQS_KEM_free(kem)
    return K


def demo_kem_tamper(lib):
    head("[§2] TAMPER — what happens when the ciphertext is attacked")
    note("ML-KEM uses implicit rejection: a mauled ciphertext does not")
    note("raise an error — it decapsulates to unrelated random bytes.")
    note("The handshake then fails closed because the secrets differ.")
    kem = lib.OQS_KEM_new(b"ML-KEM-768")
    K = kem.contents
    pk = ctypes.create_string_buffer(K.length_public_key)
    sk = ctypes.create_string_buffer(K.length_secret_key)
    assert lib.OQS_KEM_keypair(kem, pk, sk) == OQS_SUCCESS
    ct = ctypes.create_string_buffer(K.length_ciphertext)
    ss1 = ctypes.create_string_buffer(K.length_shared_secret)
    assert lib.OQS_KEM_encaps(kem, ct, ss1, pk) == OQS_SUCCESS

    sub("attacker flips one byte of the ciphertext in transit")
    bad = bytearray(ct.raw)
    bad[10] ^= 0xFF
    say(f"  ct' (mauled): {hx(bytes(bad))}")

    ss2 = ctypes.create_string_buffer(K.length_shared_secret)
    rc = lib.OQS_KEM_decaps(kem, ss2,
                            ctypes.create_string_buffer(bytes(bad)),
                            sk)
    say(f"  decaps return code : {rc} (0 = 'success' — implicit rejection)")
    say(f"  ss == ss'          : {bytes(ss1.raw) == bytes(ss2.raw)}")
    assert bytes(ss1.raw) != bytes(ss2.raw), \
        "tampered ct must NOT yield the real secret"
    say("  => The attacker gets nothing. The transcript check in the")
    say("     real handshake then fails closed — session refused.")
    lib.OQS_KEM_free(kem)


def demo_sig(lib):
    head("[§3] SIGNATURES — ML-DSA-65  (NIST FIPS 204)")
    note("ML-DSA = Module-Lattice Digital Signature Algorithm, née")
    note("Dilithium. This is the PQPE's identity primitive: the enclave")
    note("signs the handshake transcript, proving it owns its keys.")
    sig = lib.OQS_SIG_new(b"ML-DSA-65")
    if not sig:
        say("FATAL: ML-DSA-65 not available in this build.")
        sys.exit(3)
    S = sig.contents
    sub("parameters")
    say(f"  method_name        : {S.method_name.decode()}")
    say(f"  NIST level         : {S.claimed_nist_level}")
    say(f"  EUF-CMA secure     : {bool(S.euf_cma)}")
    say(f"  public key         : {S.length_public_key} bytes")
    say(f"  secret key         : {S.length_secret_key} bytes")
    say(f"  signature          : {S.length_signature} bytes")
    note("Compare Ed25519: 32-byte keys, 64-byte signatures — and "
         "broken by Shor. Size is the tariff quantum resistance "
         "charges.")

    sub("3a. keypair + sign")
    pk = ctypes.create_string_buffer(S.length_public_key)
    sk = ctypes.create_string_buffer(S.length_secret_key)

    def _kg():
        assert lib.OQS_SIG_keypair(sig, pk, sk) == OQS_SUCCESS
    timed("keygen", _kg)
    say(f"  pk : {hx(pk.raw)}")

    msg = b"PQPE handshake transcript, mode=hybrid, 2026-10-03"
    sigbuf = ctypes.create_string_buffer(S.length_signature)
    siglen = ctypes.c_size_t(0)

    def _sign():
        assert lib.OQS_SIG_sign(sig, sigbuf, ctypes.byref(siglen),
                                msg, len(msg), sk) == OQS_SUCCESS
    timed("sign", _sign)
    say(f"  msg: {msg.decode()}")
    say(f"  sig: {hx(sigbuf.raw[:siglen.value])}")
    note(f"signed {len(msg)} bytes -> {siglen.value}-byte signature.")

    sub("3b. verify (honest)")
    rc = lib.OQS_SIG_verify(sig, msg, len(msg),
                            sigbuf, siglen.value, pk)
    say(f"  verify -> {rc} (0 = valid)")
    assert rc == OQS_SUCCESS

    sub("3c. verify, message TAMPERED (one byte)")
    badmsg = bytearray(msg)
    badmsg[5] ^= 0x01
    rc = lib.OQS_SIG_verify(sig, bytes(badmsg), len(badmsg),
                            sigbuf, siglen.value, pk)
    say(f"  verify -> {rc} (nonzero = REJECTED)")
    assert rc != OQS_SUCCESS, "tampered message must not verify"
    say("  => Forgery of the transcript fails closed. This is what")
    say("     stops a man-in-the-middle downgrading hybrid to classical.")

    sub("3d. verify, signature TAMPERED (one byte)")
    badsig = bytearray(sigbuf.raw[:siglen.value])
    badsig[0] ^= 0x01
    rc = lib.OQS_SIG_verify(sig, msg, len(msg),
                            ctypes.create_string_buffer(bytes(badsig)),
                            siglen.value, pk)
    say(f"  verify -> {rc} (nonzero = REJECTED)")
    assert rc != OQS_SUCCESS, "tampered signature must not verify"
    say("  => As Black's has it: sealed — closed against inspection;")
    say("     here, closed against forgery too.")
    lib.OQS_SIG_free(sig)


def demo_hybrid_lesson():
    head("[§4] THE HYBRID LESSON — why the PQPE pairs both")
    say("  The PQPE never trusts one hardness assumption alone:")
    say()
    say("    session = HKDF( X25519_secret  ||  ML-KEM_secret )")
    say()
    say("  If lattice crypto ever breaks classically  -> X25519 holds.")
    say("  If a cryptographically-relevant quantum computer arrives")
    say("     and breaks X25519                       -> ML-KEM holds.")
    say("  An attacker must break BOTH, simultaneously, to read a")
    say("  single session. That is the 'hybrid forever' doctrine.")
    say()
    say("  Franklin's warning is the threat model: every party that")
    say("  touches a secret is a mouth that can talk. Mathematics")
    say("  does not talk — which is why the secret lives in the math,")
    say("  not in the messengers.")


def main():
    global VERBOSE
    if "--quiet" in sys.argv:
        VERBOSE = False

    head("PQPE NATIVE DEMO — post-quantum crypto, on-device")
    say(f"  date      : {DATE}  ·  93  ·  IA.'.A.'.M.TRVVTH")
    say("  purpose   : educational research & development — every step")
    say("              shown, every payload inspected, nothing hidden.")
    say()
    say("  Epigraphs — the five wells:")
    for well, quote, cite in EPIGRAPHS:
        say(f"    [{well}] \"{quote}\"")
        say(f"            — {cite}")
        say()

    lib, path = load()
    say(f"  library   : {path}")
    note("Built with Android NDK r30, liboqs 0.16.0, arm64-v8a.")

    demo_kem(lib)
    demo_kem_tamper(lib)
    demo_sig(lib)
    demo_hybrid_lesson()

    head("VERDICT")
    say("  ML-KEM-768 key exchange   : ROUND-TRIP OK, tamper REJECTED")
    say("  ML-DSA-65 signatures      : VERIFY OK, forgeries REJECTED")
    say("  => This phone now speaks post-quantum cryptography.")
    say("     No more secrets — except the ones mathematics keeps.")
    say()
    say("  Johnathan \"Qasparr\" (Κασπάρρ) Monroe,")
    say("  Keeper of the Secret Treasure.")
    say("  All Rights Reserved, Without Prejudice.")
    say("  Live, Love, and let Love, Live.")


if __name__ == "__main__":
    main()
