"""
Example: Monitor agent health via AXME mesh.

Lists all registered agents and their current health status.
Run this while agent.py is running, then kill agent.py
and run this again to see the status change to UNREACHABLE.
"""

from axme import AxmeClient, AxmeClientConfig
import os

client = AxmeClient(AxmeClientConfig(api_key=os.environ["AXME_API_KEY"]))

print("AXME Mesh - Agent Health Status")
print("=" * 60)

agents = client.mesh.list_agents()

if not agents:
    print("No agents registered.")
else:
    # Summary
    statuses = {}
    for agent in agents:
        statuses[agent.status] = statuses.get(agent.status, 0) + 1

    print(f"\nTotal agents: {len(agents)}")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    print(f"\n{'Name':<25} {'Machine':<15} {'Status':<15} {'Last Seen'}")
    print("-" * 70)

    for agent in agents:
        machine = agent.metadata.get("machine", "unknown")
        print(f"{agent.name:<25} {machine:<15} {agent.status:<15} {agent.last_heartbeat}")

        if agent.status == "unreachable":
            print(f"  >>> ALERT: {agent.name} is unreachable!")
        elif agent.status == "degraded":
            reason = agent.metadata.get("reason", "unknown")
            print(f"  >>> WARNING: {agent.name} is degraded ({reason})")

print("\n" + "=" * 60)
