"""
Simple CLI chat demo that uses handshake and secure_channel to send a message
from Alice -> Bob locally in-process for demo purposes.
"""

from hybrid.handshake import perform_handshake
from hybrid.secure_channel import encrypt_message, decrypt_message

def run_chat_demo():
    print("Starting handshake (simulated PQC + QKD)...")
    keys, info = perform_handshake(qkd_params={'n': 200, 'distance_km': 5.0})
    print("Handshake complete. QKD metrics:", info['qkd_metrics'])
    client_key = keys['client_key']
    server_key = keys['server_key']
    # Alice encrypts a message with client_key
    plaintext = b"Hello Bob, this is a hybrid-secure message!"
    enc = encrypt_message(client_key, plaintext, associated_data=b'chat')
    print("Alice sent ciphertext:", enc['ciphertext'][:24], "...")
    # Bob decrypts with same key (in our sim server_key==client_key derivation is symmetric)
    pt = decrypt_message(client_key, enc['nonce'], enc['ciphertext'], associated_data=b'chat')
    print("Bob received (decrypted):", pt.decode())
