"""
HKDF-based hybrid KDF combining PQC and QKD secrets.
"""

import hmac
import hashlib

def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if salt is None or len(salt)==0:
        salt = bytes([0]*32)
    return hmac.new(salt, ikm, hashlib.sha256).digest()

def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    okm = b''
    t = b''
    counter = 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:length]

def derive_session_keys(ss_pqc: bytes, ss_qkd: bytes, transcript_hash: bytes=b'', out_len=32):
    """
    Combine ss_pqc and ss_qkd by concatenation and HKDF(SHA256) to produce session key material.
    Returns a dict with 'client_key' and 'server_key'.
    """
    ikm = ss_pqc + ss_qkd
    prk = hkdf_extract(transcript_hash, ikm)
    key_material = hkdf_expand(prk, b"hybrid session keys", out_len*2)
    return {
        'client_key': key_material[:out_len],
        'server_key': key_material[out_len:out_len*2]
    }
