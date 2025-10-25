"""
Channel model for QKD: models channel loss (attenuation), detection efficiency and dark counts.
"""

import numpy as np

def transmit_photon(prob_reach):
    """Return True if a photon arrives (survives loss) based on prob_reach."""
    return np.random.rand() < prob_reach

def simulate_detection(prob_reach, detector_efficiency=0.1, dark_count_rate=1e-5):
    """
    Returns whether detector registers a click, and whether that click came from a real photon.
    - prob_reach: probability photon reaches detector (after channel loss)
    - detector_efficiency: probability detector clicks if photon arrives
    - dark_count_rate: probability of a dark count per time slot
    """
    # Real photon detection
    real_click = (np.random.rand() < prob_reach) and (np.random.rand() < detector_efficiency)
    # Dark count independent
    dark_click = (np.random.rand() < dark_count_rate)
    click = real_click or dark_click
    came_from_photon = real_click and not dark_click
    return click, came_from_photon
