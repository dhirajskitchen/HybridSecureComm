"""
Simple policy constants for handshake behavior and thresholds.
"""

QKD_QBER_MAX = 0.10   # abort if QBER estimate > 10%
FALLBACK_TO_PQC_ONLY = False  # if True, allow PQC-only sessions when QKD fails
REKEY_INTERVAL_SECONDS = 3600  # rekey every hour by default
