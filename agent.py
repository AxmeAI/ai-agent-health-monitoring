"""
Example: AI agent with AXME mesh health monitoring.

Starts automatic heartbeat and reports metrics as it processes tasks.
"""

from axme import AxmeClient, AxmeClientConfig
import os
import time
import random

client = AxmeClient(AxmeClientConfig(api_key=os.environ["AXME_API_KEY"]))

# Start automatic heartbeat (background thread, every 30 seconds)
client.mesh.start_heartbeat(interval_seconds=30)

print("Heartbeat started. Agent visible at mesh.axme.ai")
print("Press Ctrl+C to stop (simulates crash).\n")

tasks_processed = 0

try:
    while True:
        # Simulate processing a task
        task_id = f"ORDER-{random.randint(1000, 9999)}"
        print(f"Processing {task_id}...")

        # Simulate work (1-3 seconds)
        latency = random.uniform(1, 3)
        time.sleep(latency)

        # Randomly simulate failure (10% chance)
        if random.random() < 0.1:
            print(f"  Failed: {task_id}")
            client.mesh.report_metric(success=False, latency_ms=latency * 1000)
        else:
            tasks_processed += 1
            cost = random.uniform(0.01, 0.05)
            client.mesh.report_metric(success=True, latency_ms=latency * 1000, cost_usd=cost)

        print(f"  Done. Total processed: {tasks_processed}")

except KeyboardInterrupt:
    client.mesh.stop_heartbeat()
    print("\nAgent stopped. Heartbeat will stop. Status will become UNREACHABLE.")
