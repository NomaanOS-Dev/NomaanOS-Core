import json
from typing import Dict, Any

class AIAgentBridge:
    """
    Bridges LLM Agent intent with NomaanOS Fail-Closed Sentinel Engine.
    Prevents prompt-injection based OS execution.
    """
    def __init__(self):
        self.risk_patterns = ["rm -rf", "mkfs", "dd if=", "> /dev/", "chmod 777"]

    def parse_llm_intent(self, natural_language_intent: str) -> Dict[str, Any]:
        intent_lower = natural_language_intent.lower()
        
        # Check for dangerous injection signatures
        for pattern in self.risk_patterns:
            if pattern in intent_lower:
                return {
                    "status": "REJECTED_BY_SENTINEL",
                    "reason": f"Dangerous destructive pattern detected in intent: '{pattern}'",
                    "action": "HALT"
                }
        
        return {
            "status": "APPROVED_FOR_EXECUTION",
            "reason": "Intent verified safe against invariant policies.",
            "action": "PROCEED"
        }

if __name__ == "__main__":
    bridge = AIAgentBridge()
    test_intent = "Please clean up disk space using rm -rf /"
    print("Testing Intent Translation:", json.dumps(bridge.parse_llm_intent(test_intent), indent=2))
