"""
pqc_kem.py — liboqs-backed KEM wrapper with fallback to simulated KEM.

This module attempts to use the official liboqs Python bindings (imported as `oqs`).
If `oqs` is unavailable, it falls back to the simple simulated KEM (for testing).
"""

import os
import hashlib

# Try to import real liboqs Python bindings
try:
    import oqs
    _HAS_OQS = True
except Exception:
    _HAS_OQS = False

# -------------------------
# Fallback (simulated KEM)
# -------------------------
if not _HAS_OQS:
    import hmac
    import os as _os
    def generate_keypair():
        """Fallback: generate random pub/priv bytes (not secure)."""
        pub = _os.urandom(64)
        priv = _os.urandom(64)
        return pub, priv

    def encapsulate(pub):
        """Fallback encapsulate: deterministic pseudo-ss from ct+pub."""
        ct = _os.urandom(80)
        ss = hashlib.sha256(ct + pub).digest()
        return ct, ss

    def decapsulate(ct, priv, pub=None):
        """Fallback decapsulate: reproduce same ss from ct+pub."""
        # Note: fallback requires pub passed in to match encapsulate
        return hashlib.sha256(ct + (pub or b'')).digest()

else:
    # -------------------------
    # Real liboqs-backed KEM
    # -------------------------
    # Choose a KEM mechanism. Kyber variants are common; pick a balanced one.
    # You can change this to 'Kyber512', 'Kyber768', 'Kyber1024' etc, depending on liboqs build.
    _KEM_NAME = "Kyber768"

    def _get_enabled_kems():
        try:
            return oqs.get_enabled_kem_mechanisms()
        except Exception:
            # older bindings might expose as oqs.get_enabled_kem_mechanisms or similar
            try:
                return oqs.KeyEncapsulation.get_enabled_kem_mechanisms()
            except Exception:
                return []

    # If chosen KEM not enabled, try to fallback to the first available KEM
    if _KEM_NAME not in _get_enabled_kems():
        enabled = _get_enabled_kems()
        if enabled:
            _KEM_NAME = enabled[0]
        else:
            # No available KEMs — fallback to simulated behavior
            _HAS_OQS = False
            import hmac
            import os as _os2
            def generate_keypair():
                pub = _os2.urandom(64)
                priv = _os2.urandom(64)
                return pub, priv
            def encapsulate(pub):
                ct = _os2.urandom(80)
                ss = hashlib.sha256(ct + pub).digest()
                return ct, ss
            def decapsulate(ct, priv, pub=None):
                return hashlib.sha256(ct + (pub or b'')).digest()
    if _HAS_OQS:
        def generate_keypair():
            """
            Generate a KEM keypair using liboqs.
            Returns (public_key_bytes, secret_key_bytes)
            """
            kem = oqs.KeyEncapsulation(_KEM_NAME)
            # generate_keypair() returns (pk, sk)
            pk, sk = kem.generate_keypair()
            # pk/sk are bytes
            return pk, sk

        def encapsulate(pub):
            """
            Encapsulate to a recipient public key `pub`.
            Returns (ciphertext_bytes, shared_secret_bytes).
            """
            # Create a transient kem object and encapsulate using the recipient's pubkey
            with oqs.KeyEncapsulation(_KEM_NAME) as kem:
                # encapsulate takes recipient public key and returns (ct, ss)
                ct, ss = kem.encapsulate(pub)
            return ct, ss

        def decapsulate(ct, priv, pub=None):
            """
            Decapsulate ciphertext `ct` using secret key `priv`.
            Returns shared_secret_bytes.
            Note: liboqs KeyEncapsulation.decapsulate expects the secret key to be loaded within the KEM object.
            Some liboqs Python wrappers accept passing the secret key; others require the internal kem object
            to have been used to generate the keypair. This wrapper handles the common case where decapsulate
            takes (ciphertext, secret_key).
            """
            # Many liboqs python bindings let you call decapsulate(ct, sk)
            try:
                with oqs.KeyEncapsulation(_KEM_NAME) as kem:
                    ss = kem.decapsulate(ct, priv)
                return ss
            except TypeError:
                # Older/newer wrappers might have different signatures.
                # Try the alternative: instantiate kem and set secret key via internal method (if available).
                # As a last resort, compute a hash-based placeholder (should not be used in real deployments).
                try:
                    # Some wrappers provide kem.import_secret_key or kem.generate_keypair() that returns both keys.
                    with oqs.KeyEncapsulation(_KEM_NAME) as kem:
                        # try using kem.decapsulate with secret key as keyword (some versions)
                        ss = kem.decapsulate(ciphertext=ct, secret_key=priv)
                        return ss
                except Exception:
                    # Fallback insecure: derive ss as hash(ct||priv)
                    return hashlib.sha256(ct + priv).digest()
