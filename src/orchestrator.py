import json
from src.engine import NoseExec
from src.agent_bridge import AIAgentBridge

class NomaanOSOrchestrator:
    """
    Master Pipeline: AI Intent -> Sentinel Proxy -> Fail-Closed Execution -> Audit
    """
    def __init__(self):
        self.bridge = AIAgentBridge()
        self.exec_engine = NoseExec(["echo", "uname", "ls"])

    def process_request(self, natural_language_intent: str, raw_command: list) -> dict:
        print(f"\n[ORCHESTRATOR] Received Intent: '{natural_language_intent}'")
        
        # Step 1: AI Intent Check via Sentinel Bridge
        intent_check = self.bridge.parse_llm_intent(natural_language_intent)
        if intent_check["action"] == "HALT":
            return {
                "pipeline_status": "BLOCKED_AT_INTENT_LAYER",
                "details": intent_check
            }
        
        # Step 2: Fail-Closed Execution
        exec_result = self.exec_engine.execute(raw_command)
        return {
            "pipeline_status": "SUCCESS" if exec_result["status"] == "SUCCESS" else "BLOCKED_AT_EXEC_LAYER",
            "execution_details": exec_result
        }

if __name__ == "__main__":
    os_core = NomaanOSOrchestrator()
    
    # Test 1: Malicious intent
    res1 = os_core.process_request("List directory contents", ["ls"])
    print("Test 1 Result:", json.dumps(res1, indent=2))
