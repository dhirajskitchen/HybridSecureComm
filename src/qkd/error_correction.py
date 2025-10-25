"""
A lightweight error correction reconciliation:
This is a toy, not a production Cascade/LDPC. It uses parity-check blocks
and reveals block parity to locate errors and correct single-bit errors.
"""

import hashlib

def block_parity(bits, block_size):
    blocks = [bits[i:i+block_size] for i in range(0, len(bits), block_size)]
    parities = [sum(b)%2 for b in blocks]
    return parities

def reconcile(alice_bits, bob_bits, block_size=16, max_rounds=4):
    """
    Simple iterative parity-based reconciliation.
    Returns corrected bob_bits and leakage in bits (parity bits revealed).
    """
    n = min(len(alice_bits), len(bob_bits))
    alice = alice_bits[:n]
    bob = bob_bits[:n]
    leakage = 0
    for _ in range(max_rounds):
        par_a = block_parity(alice, block_size)
        par_b = block_parity(bob, block_size)
        leakage += len(par_a)
        # For each differing parity try to correct a single bit by flipping each bit and checking parity match
        blocks = [list(range(i, min(i+block_size, n))) for i in range(0, n, block_size)]
        for bi, (pa, pb) in enumerate(zip(par_a, par_b)):
            if pa != pb:
                idxs = blocks[bi]
                # try flipping each bit in bob block to see which fixes parity (this corrects only single-bit errors)
                fixed = False
                for idx in idxs:
                    bob[idx] = 1 - bob[idx]
                    if sum(bob[i] for i in idxs) % 2 == pa:
                        fixed = True
                        break
                    else:
                        bob[idx] = 1 - bob[idx]
                # If not fixed, proceed (multiple errors)
    return bob, leakage
