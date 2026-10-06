# Contributing to NomaanOS-Core

Thanks for contributing.

## Scope

This repository is an experimental research project. Contributions should be clear, focused, and easy to review.

## Before opening a pull request

- keep the change narrow and easy to reason about
- update docs when behavior or setup changes
- run relevant validation commands locally
- avoid committing secrets, private keys, or captured forensic data

## Minimum validation

Run the most relevant checks before opening a PR:

```bash
python -m py_compile nomaanos.py api_server.py tui_dashboard.py
pytest -q
```

## Pull request expectations

- include a short summary of what changed and why
- explain the security or operational impact
- call out any limitations or caveats
- note if the change is experimental or partial

## Security-sensitive changes

Any change affecting runtime execution, telemetry, or audit integrity should include a brief note on:

- threat model assumptions
- expected failure behavior
- risk surface or constraints

## Review standard

Contributions should be reviewed with the same caution expected for any security-adjacent or local execution code.
