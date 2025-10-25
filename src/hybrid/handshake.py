"""
Handshake orchestration: run PQC KEM (simulated) and QKD (simulator) in sequence
and derive session keys via hybrid KDF.
"""

from pqc.pqc_kem import generate_keypair, encapsulate, decapsulate
from qkd.bb84_sim import run_bb84
from .kdf import derive_session_keys

def perform_handshake(qkd_params=None):
    # PQC part
    pub, priv = generate_keypair()
    ct, ss_pqc = encapsulate(pub)
    # On receiver side decapsulate (simulated)
    ss_pqc_receiver = decapsulate(ct, priv, pub)
    assert ss_pqc == ss_pqc_receiver  # simulated property

    # QKD part (simulate)
    if qkd_params is None:
        qkd_params = {}
    ss_qkd, metrics = run_bb84(**qkd_params)
    if ss_qkd is None:
        raise RuntimeError("QKD produced no key (too much loss).")

    # Hybrid KDF
    keys = derive_session_keys(ss_pqc, ss_qkd)
    handshake_info = {
        'pqc_pub': pub,
        'pqc_ct': ct,
        'qkd_metrics': metrics
    }
    return keys, handshake_info
