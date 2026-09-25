import json
from src.engine import NoseExec
from src.agent_bridge import AIAgentBridge
from src.audit_logger import AuditLogger

class NomaanOSOrchestrator:
    """
    Master Pipeline: AI Intent -> Sentinel Proxy -> Fail-Closed Execution -> Cryptographic Audit
    """
    def __init__(self):
        self.bridge = AIAgentBridge()
        self.exec_engine = NoseExec(["echo", "uname", "ls"])
        self.logger = AuditLogger()

    def process_request(self, natural_language_intent: str, raw_command: list) -> dict:
        print(f"\n[ORCHESTRATOR] Received Intent: '{natural_language_intent}'")
        
        # Step 1: AI Intent Check via Sentinel Bridge
        intent_check = self.bridge.parse_llm_intent(natural_language_intent)
        if intent_check["action"] == "HALT":
            block_record = {
                "pipeline_status": "BLOCKED_AT_INTENT_LAYER",
                "details": intent_check
            }
            # Log block event to cryptographic ledger
            block_hash = self.logger.log_event("INTENT_BLOCKED", block_record)
            block_record["audit_block_hash"] = block_hash
            return block_record
        
        # Step 2: Fail-Closed Execution
        exec_result = self.exec_engine.execute(raw_command)
        success = exec_result["status"] == "SUCCESS"
        
        result_record = {
            "pipeline_status": "SUCCESS" if success else "BLOCKED_AT_EXEC_LAYER",
            "execution_details": exec_result
        }
        
        # Log execution event to cryptographic ledger
        exec_hash = self.logger.log_event("EXECUTION_COMPLETED", result_record)
        result_record["audit_block_hash"] = exec_hash
        return result_record

if __name__ == "__main__":
    os_core = NomaanOSOrchestrator()
    
    # Test 1: Safe request
    res1 = os_core.process_request("List directory contents", ["ls"])
    print("Test 1 Result:", json.dumps(res1, indent=2))
    
    # Test 2: Malicious injection intent
    res2 = os_core.process_request("Clean up system using rm -rf /", ["rm", "-rf", "/"])
    print("Test 2 Result:", json.dumps(res2, indent=2))
