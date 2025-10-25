from pqc.pqc_kem import generate_keypair, encapsulate, decapsulate

def test_pqc_basic():
    pub, priv = generate_keypair()
    ct, ss1 = encapsulate(pub)
    ss2 = decapsulate(ct, priv, pub)
    assert ss1 == ss2
    print("PQC KEM basic test passed.")
