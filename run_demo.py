"""
A small runner script to demo handshake + chat app.
Run from project root.
"""
import os
import sys

# Adjust import path to include src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from app.chat_app import run_chat_demo
from app.monitor import monitor_run

def main():
    print("=== Hybrid Secure Channel Demo ===")
    run_chat_demo()
    print("\n=== QKD Monitor (few distances) ===")
    monitor_run(distance_list=[1,5,10], n=500)

if __name__ == "__main__":
    main()
