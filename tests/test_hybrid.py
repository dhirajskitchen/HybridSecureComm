from hybrid.handshake import perform_handshake

def test_handshake():
    keys, info = perform_handshake(qkd_params={'n':200, 'distance_km':1.0})
    assert 'client_key' in keys and len(keys['client_key']) == 32
    print("Hybrid handshake produced session keys.")
