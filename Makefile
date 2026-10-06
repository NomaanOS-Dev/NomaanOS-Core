# NomaanOS-Core

## Development workflow

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-dev.txt
```

### Run tests

```bash
pytest -q
```

### Lint and compile checks

```bash
python -m py_compile nomaanos.py api_server.py tui_dashboard.py
ruff check .
```

### Standard local validation

```bash
python nomaanos.py --status
python nomaanos.py telemetry
python nomaanos.py chain-verify
```

### Docker

```bash
docker compose up --build
```
