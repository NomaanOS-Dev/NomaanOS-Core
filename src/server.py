from fastapi import FastAPI
from src.telemetry_dashboard import render_dashboard
from src.phoenix_engine import PhoenixEngine
from src.neural_lock import NeuralLock
from src.compliance_auditor import ComplianceAuditor
from src.orchestrator import NomaanOSOrchestrator

app = FastAPI(
    title="NomaanOS Sovereign AI Stack (SAS)",
    version="6.0.0",
    description="Fail-Closed Execution & Cryptographic Audit REST API"
)

@app.get("/")
def read_root():
    return {
        "status": "ONLINE",
        "system": "NomaanOS-Core v6.0",
        "architect": "Nomaan Khan (IHFC-IITD Scholar)"
    }

@app.get("/verify")
def verify_ledger():
    phoenix = PhoenixEngine()
    return phoenix.verify_and_heal()

@app.get("/lock")
def neural_lock():
    lock = NeuralLock()
    return lock.generate_attestation_token("REST_API_REQUEST")

@app.get("/audit")
def compliance_audit():
    auditor = ComplianceAuditor()
    return auditor.generate_compliance_report()

@app.post("/run")
def run_pipeline(intent: str, command: str):
    os_core = NomaanOSOrchestrator()
    cmd_list = command.split()
    return os_core.process_request(intent, cmd_list)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
