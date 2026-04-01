"""
Example: AI agent with AXME mesh health monitoring.

This agent registers in the mesh, starts automatic heartbeat,
and reports health status as it processes tasks.
"""

from axme import AxmeClient, AxmeClientConfig
import os
import time
import random

client = AxmeClient(AxmeClientConfig(api_key=os.environ["AXME_API_KEY"]))

# Register this agent in the AXME mesh
client.mesh.register(
    agent_uri="agent://myorg/production/order-processor",
    metadata={
        "machine": os.environ.get("HOSTNAME", "local"),
        "version": "1.4.2",
        "role": "order-processing",
    },
)

# Start automatic heartbeat (background thread, every 30 seconds)
client.mesh.start_heartbeat(interval_seconds=30)

print("Agent registered and heartbeat started.")
print("Press Ctrl+C to stop (simulates crash).\n")

tasks_processed = 0

try:
    while True:
        # Simulate processing a task
        task_id = f"ORDER-{random.randint(1000, 9999)}"
        print(f"Processing {task_id}...")

        # Simulate work (1-3 seconds)
        time.sleep(random.uniform(1, 3))

        # Randomly simulate degraded state (10% chance)
        if random.random() < 0.1:
            print(f"  Warning: {task_id} took longer than expected")
            client.mesh.report_status("degraded", metadata={
                "last_task": task_id,
                "reason": "high_latency",
                "queue_depth": random.randint(50, 200),
            })
        else:
            tasks_processed += 1
            client.mesh.report_status("healthy", metadata={
                "last_task": task_id,
                "tasks_processed": tasks_processed,
                "queue_depth": random.randint(0, 20),
            })

        print(f"  Done. Total processed: {tasks_processed}")

except KeyboardInterrupt:
    print("\nAgent stopped. Heartbeat will stop. Status will become UNREACHABLE.")
