"""
Privacy amplification using SHA-256 based HKDF-style reduction.
Given a reconciled bitstring (list of 0/1), derive a shorter secure key.
"""

import hashlib
import hmac
from math import ceil

def bits_to_bytes(bits):
    b = bytearray(ceil(len(bits)/8))
    for i, bit in enumerate(bits):
        if bit:
            byte_idx = i // 8
            bit_idx = 7 - (i % 8)
            b[byte_idx] |= (1 << bit_idx)
    return bytes(b)

def derive_key_from_bits(bits, out_len=32, salt=b''):
    """
    Produce out_len bytes from bitstring using HKDF-like construction with HMAC-SHA256.
    """
    ikm = bits_to_bytes(bits)
    # HKDF-Extract
    if not salt:
        salt = bytes([0]*32)
    prk = hmac.new(salt, ikm, hashlib.sha256).digest()
    # HKDF-Expand
    okm = b''
    t = b''
    counter = 1
    while len(okm) < out_len:
        t = hmac.new(prk, t + b'\x00' + bytes([counter]), hashlib.sha256).digest()
        okm += t
        counter += 1
    return okm[:out_len]
