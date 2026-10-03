/* pqpe_test.c — functional test for the PQPE native liboqs build.
 *
 * dlopens liboqs.so and exercises the public shared-library API:
 *   OQS_KEM_new("ML-KEM-768") / OQS_SIG_new("ML-DSA-65")
 * (per-algorithm OQS_KEM_ml_kem_768_new-style constructors are intentionally
 *  hidden in liboqs shared builds — upstream marks only the generic
 *  string-dispatched constructors OQS_API; this is the documented way to
 *  consume liboqs via dlopen/JNI.)
 *
 * Then runs:
 *   KEM: keypair -> encaps -> decaps, shared secrets must match
 *   SIG: keypair -> sign -> verify OK, tampered message must FAIL verify
 *
 * Build (NDK clang, Android arm64):
 *   aarch64-linux-android34-clang pqpe_test.c -ldl -o pqpe_test
 * Run under emulation:
 *   qemu-aarch64 -L <ndk-sysroot> ./pqpe_test ./liboqs.so
 */
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Minimal mirrors of liboqs 0.16.0 struct layouts (field order matters). */
typedef int OQS_STATUS;
#define OQS_SUCCESS 0

typedef struct {
	const char *method_name;
	const char *alg_version;
	uint8_t claimed_nist_level;
	_Bool ind_cca;
	size_t length_public_key;
	size_t length_secret_key;
	size_t length_ciphertext;
	size_t length_shared_secret;
	size_t length_keypair_seed;
	size_t length_encaps_seed;
	OQS_STATUS (*keypair_derand)(uint8_t *, uint8_t *, const uint8_t *);
	OQS_STATUS (*keypair)(uint8_t *public_key, uint8_t *secret_key);
	OQS_STATUS (*encaps)(uint8_t *ciphertext, uint8_t *shared_secret,
	                     const uint8_t *public_key);
	OQS_STATUS (*decaps)(uint8_t *shared_secret, const uint8_t *ciphertext,
	                     const uint8_t *secret_key);
} OQS_KEM;

typedef struct {
	const char *method_name;
	const char *alg_version;
	uint8_t claimed_nist_level;
	_Bool euf_cma;
	_Bool suf_cma;
	_Bool sig_with_ctx_support;
	size_t length_public_key;
	size_t length_secret_key;
	size_t length_signature;
	OQS_STATUS (*keypair)(uint8_t *public_key, uint8_t *secret_key);
	OQS_STATUS (*sign)(uint8_t *signature, size_t *signature_len,
	                   const uint8_t *message, size_t message_len,
	                   const uint8_t *secret_key);
	OQS_STATUS (*verify)(const uint8_t *message, size_t message_len,
	                     const uint8_t *signature, size_t signature_len,
	                     const uint8_t *public_key);
} OQS_SIG;

static int fail(const char *msg) { printf("FAIL: %s\n", msg); return 1; }

int main(int argc, char **argv) {
	if (argc < 2) return fail("usage: pqpe_test <path/to/liboqs.so>");
	void *h = dlopen(argv[1], RTLD_NOW);
	if (!h) return fail(dlerror());

	OQS_KEM *(*kem_new)(const char *) = dlsym(h, "OQS_KEM_new");
	OQS_SIG *(*sig_new)(const char *) = dlsym(h, "OQS_SIG_new");
	void (*kem_free)(OQS_KEM *) = dlsym(h, "OQS_KEM_free");
	void (*sig_free)(OQS_SIG *) = dlsym(h, "OQS_SIG_free");
	if (!kem_new) return fail("OQS_KEM_new missing");
	if (!sig_new) return fail("OQS_SIG_new missing");

	/* ---- KEM round trip ---- */
	OQS_KEM *kem = kem_new("ML-KEM-768");
	if (!kem) return fail("ML-KEM-768 instantiate");
	printf("KEM: %s (pk=%zu sk=%zu ct=%zu ss=%zu)\n", kem->method_name,
	       kem->length_public_key, kem->length_secret_key,
	       kem->length_ciphertext, kem->length_shared_secret);
	uint8_t *pk = malloc(kem->length_public_key);
	uint8_t *sk = malloc(kem->length_secret_key);
	uint8_t *ct = malloc(kem->length_ciphertext);
	uint8_t *ss1 = malloc(kem->length_shared_secret);
	uint8_t *ss2 = malloc(kem->length_shared_secret);
	if (kem->keypair(pk, sk) != OQS_SUCCESS) return fail("kem keypair");
	if (kem->encaps(ct, ss1, pk) != OQS_SUCCESS) return fail("kem encaps");
	if (kem->decaps(ss2, ct, sk) != OQS_SUCCESS) return fail("kem decaps");
	if (memcmp(ss1, ss2, kem->length_shared_secret) != 0)
		return fail("KEM shared secrets differ");
	printf("KEM OK: encaps/decaps shared secrets match (%zu bytes)\n",
	       kem->length_shared_secret);
	if (kem_free) kem_free(kem);
	free(pk); free(sk); free(ct); free(ss1); free(ss2);

	/* ---- SIG round trip + tamper ---- */
	OQS_SIG *sig = sig_new("ML-DSA-65");
	if (!sig) return fail("ML-DSA-65 instantiate");
	printf("SIG: %s (pk=%zu sk=%zu sig=%zu)\n", sig->method_name,
	       sig->length_public_key, sig->length_secret_key,
	       sig->length_signature);
	uint8_t *spk = malloc(sig->length_public_key);
	uint8_t *ssk = malloc(sig->length_secret_key);
	uint8_t *sg = malloc(sig->length_signature);
	size_t sg_len = 0;
	const char *msg = "pqpe native core test vector";
	if (sig->keypair(spk, ssk) != OQS_SUCCESS) return fail("sig keypair");
	if (sig->sign(sg, &sg_len, (const uint8_t *)msg, strlen(msg), ssk) != OQS_SUCCESS)
		return fail("sig sign");
	if (sig->verify((const uint8_t *)msg, strlen(msg), sg, sg_len, spk) != OQS_SUCCESS)
		return fail("sig verify (valid sig rejected)");
	char tampered[64];
	memcpy(tampered, msg, strlen(msg) + 1);
	tampered[0] ^= 0x01;
	if (sig->verify((const uint8_t *)tampered, strlen(msg), sg, sg_len, spk) == OQS_SUCCESS)
		return fail("sig verify (tampered msg ACCEPTED)");
	printf("SIG OK: sign/verify pass, tampered message rejected (sig len %zu)\n", sg_len);
	if (sig_free) sig_free(sig);
	free(spk); free(ssk); free(sg);

	dlclose(h);
	printf("ALL TESTS PASSED\n");
	return 0;
}
