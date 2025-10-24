import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Import your handler
from src.handler import handler, load_models


def simulate_runpod():
    """Simulate RunPod's persistent container"""

    # Load models once (like container startup)
    print("🚀 Container starting...")
    load_models()
    print("✅ Container ready, waiting for requests...\n")

    # Simulate multiple requests without reloading
    requests = [
        {"input": {"action": "warmup", "api_key": "temp-dev-key-12345"}},
        {"input": {"action": "warmup", "api_key": "temp-dev-key-12345"}},
        {"input": {"action": "warmup", "api_key": "temp-dev-key-12345"}},
    ]

    for i, job in enumerate(requests, 1):
        print(f"📨 Request {i} received...")
        start = time.time()
        result = handler(job)
        elapsed = time.time() - start
        print(f"✅ Response: {result}")
        print(f"⏱️  Processing time: {elapsed:.2f}s\n")
        time.sleep(1)  # Simulate delay between requests

    print("🔥 Container still running, models still in memory!")
    print("Press Ctrl+C to stop...")

    # Keep running (like RunPod does)
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n👋 Container shutting down...")


if __name__ == "__main__":
    simulate_runpod()
