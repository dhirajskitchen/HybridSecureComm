"""
Simple file transfer demo: encrypt file content and write encrypted blob to disk,
then decrypt using same session key.
"""

from hybrid.handshake import perform_handshake
from hybrid.secure_channel import encrypt_message, decrypt_message

def run_file_transfer_demo(input_path: str, out_enc_path: str, out_dec_path: str):
    keys, info = perform_handshake(qkd_params={'n': 300, 'distance_km': 2.0})
    client_key = keys['client_key']
    with open(input_path, 'rb') as f:
        data = f.read()
    enc = encrypt_message(client_key, data, associated_data=b'filetransfer')
    # write ciphertext & nonce
    with open(out_enc_path, 'wb') as f:
        f.write(enc['nonce'] + enc['ciphertext'])
    # decrypt (simulate receiver)
    with open(out_enc_path, 'rb') as f:
        blob = f.read()
    nonce = blob[:12]
    ciphertext = blob[12:]
    dec = decrypt_message(client_key, nonce, ciphertext, associated_data=b'filetransfer')
    with open(out_dec_path, 'wb') as f:
        f.write(dec)
    print("File transferred & decrypted successfully.")
