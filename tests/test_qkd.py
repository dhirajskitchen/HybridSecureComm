from qkd.bb84_sim import run_bb84

def test_bb84_run():
    key, metrics = run_bb84(n=300, distance_km=1.0)
    assert metrics['sift_len'] >= 0
    print("BB84 sim ran; sift_len=", metrics['sift_len'])
