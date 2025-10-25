"""
Secure channel using AES-GCM via cryptography library.
Provides simple encrypt/decrypt using derived symmetric keys.
"""

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_message(key: bytes, plaintext: bytes, associated_data: bytes=b'') -> dict:
    """
    Returns dict with nonce & ciphertext.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data)
    return {'nonce': nonce, 'ciphertext': ct}

def decrypt_message(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes=b'') -> bytes:
    aesgcm = AESGCM(key)
    pt = aesgcm.decrypt(nonce, ciphertext, associated_data)
    return pt
