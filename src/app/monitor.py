"""
Simple monitor that prints QKD metrics for experiments.
"""

from qkd.bb84_sim import run_bb84

def monitor_run(distance_list=[1,5,10,20], n=800):
    results = []
    for d in distance_list:
        key, metrics = run_bb84(n=n, distance_km=d)
        results.append((d, metrics))
        qber = metrics.get('qber_est')
        qber_str = f"{qber:.3f}" if qber is not None else "N/A"
        print(f"Distance {d} km -> sift_len={metrics.get('sift_len')}, qber={qber_str}, prob_reach={metrics.get('prob_reach'):.6f}")

    return results
