# NomaanOS Sentinel Proxy: Public Red-Team Challenge

## Overview
The **NomaanOS-Core** execution engine relies on a fail-closed architecture (`shell=False`, strict allowlists, and `shlex` sanitization) to decouple AI agent intent from system-level execution.

## The Challenge
Can you bypass the `NomaanOS` Sentinel Proxy and execute un-whitelisted binaries or achieve command injection via natural language intent translation?

### Rules of Engagement
1. Fork the `NomaanOS-Core` repository.
2. Attempt to exploit or bypass `src/engine.py` using malformed command vectors.
3. If you successfully execute a disallowed binary, open an issue with proof-of-concept (PoC) under the `Security Vulnerability` template.

*Architect: Nomaan Khan | IHFC-IITD Scholar*
