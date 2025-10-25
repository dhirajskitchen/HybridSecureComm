"""
BB84 simulator.
- Alice generates bits and bases
- Bob chooses random bases and measures subject to channel model
- Sifting, QBER computation, basic error correction and privacy amplification
"""

import numpy as np
from .channel_model import simulate_detection
from .error_correction import reconcile
from .privacy_amplification import derive_key_from_bits

def generate_random_bits_and_bases(n):
    bits = np.random.randint(0,2,size=n).tolist()
    bases = np.random.randint(0,2,size=n).tolist()  # 0=Z,1=X
    return bits, bases

def measure_bit(source_bit, source_basis, measure_basis, prob_reach, detector_eff=0.1, dark_count=1e-5):
    # if no click, return None
    click, came_from_photon = simulate_detection(prob_reach, detector_eff, dark_count)
    if not click:
        return None  # loss/no detection
    if came_from_photon:
        # If bases match, perfect; if bases differ, random
        if source_basis == measure_basis:
            return source_bit
        else:
            return np.random.randint(0,2)
    else:
        # dark count => random result
        return np.random.randint(0,2)

def run_bb84(n=1000, distance_km=10.0, attenuation_db_per_km=0.2, detector_eff=0.1, dark_count=1e-5):
    """
    Run BB84 and return final key bytes (after EC+PA) and metrics.
    """
    # compute channel reach probability (very simplified)
    total_loss_db = attenuation_db_per_km * distance_km
    prob_reach = 10 ** (-total_loss_db / 10.0)  # very coarse
    # generate
    a_bits, a_bases = generate_random_bits_and_bases(n)
    b_bases = np.random.randint(0,2,size=n).tolist()
    b_results = []
    for i in range(n):
        r = measure_bit(a_bits[i], a_bases[i], int(b_bases[i]), prob_reach, detector_eff, dark_count)
        b_results.append(r)
    # sifting
    sift_indices = [i for i in range(n) if a_bases[i] == b_bases[i] and b_results[i] is not None]
    alice_sift = [a_bits[i] for i in sift_indices]
    bob_sift = [b_results[i] for i in sift_indices]
    if len(alice_sift) == 0:
        return None, {'sift_len':0}
    # estimate QBER: compare small sample
    sample_size = max(1, min(50, len(alice_sift)//10))
    sample_idx = np.random.choice(len(alice_sift), sample_size, replace=False)
    sample_errors = sum(1 for si in sample_idx if alice_sift[si] != bob_sift[si])
    qber_est = sample_errors / sample_size
    # remove sample bits from sequences (they would be revealed)
    for idx in sorted(sample_idx, reverse=True):
        del alice_sift[idx]
        del bob_sift[idx]
    # error correction
    bob_corr, leakage = reconcile(alice_sift, bob_sift, block_size=16)
    # privacy amplification
    final_key = derive_key_from_bits(alice_sift, out_len=32, salt=b'bb84-salt')
    metrics = {
        'sift_len': len(alice_sift),
        'qber_est': qber_est,
        'leakage_bits': leakage,
        'distance_km': distance_km,
        'prob_reach': prob_reach
    }
    return final_key, metrics
