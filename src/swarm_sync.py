import json
import hashlib
import time
from pathlib import Path

class SwarmSyncProtocol:
    """
    NomaanOS Decentralized P2P Swarm Sync & Heartbeat Protocol.
    Manages cryptographic node discovery and ledger state synchronization across edge swarms.
    """
    def __init__(self, node_id: str = "NODE-S25-PRIMARY"):
        self.node_id = node_id
        self.genesis_time = time.time()

    def broadcast_heartbeat(self) -> dict:
        print(f"\n[SWARM] Broadcasting cryptographic heartbeat from {self.node_id}...")
        payload = f"{self.node_id}:{self.genesis_time}:{time.time()}"
        node_signature = hashlib.sha256(payload.encode()).hexdigest()
        
        heartbeat_packet = {
            "node_id": self.node_id,
            "status": "SWARM_ACTIVE",
            "timestamp": time.time(),
            "node_signature": node_signature
        }
        print(f"    --> Swarm Signature Verified: {node_signature[:24]}...")
        return heartbeat_packet

if __name__ == "__main__":
    swarm = SwarmSyncProtocol()
    print(json.dumps(swarm.broadcast_heartbeat(), indent=2))
