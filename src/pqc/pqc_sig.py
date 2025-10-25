"""
Simple signature interface using Ed25519 from cryptography.
In real deployment, use PQC signatures (e.g., Dilithium). This module provides authentication for demo.
"""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

def generate_signature_keypair():
    sk = Ed25519PrivateKey.generate()
    pk = sk.public_key()
    return sk, pk

def sign(sk, message: bytes) -> bytes:
    return sk.sign(message)

def verify(pk, message: bytes, signature: bytes) -> bool:
    try:
        pk.verify(signature, message)
        return True
    except Exception:
        return False

def serialize_public_key(pk) -> bytes:
    return pk.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)

def deserialize_public_key(data: bytes):
    return Ed25519PublicKey.from_public_bytes(data)
