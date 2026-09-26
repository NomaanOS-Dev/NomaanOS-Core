# Contributing

Thank you for contributing to NomaanOS-Core.

## Before opening a pull request

- Keep changes focused and explain security implications.
- Add or update tests for changed behavior.
- Run the repository validation commands from `README.md`.
- Run `python -m compileall .` and `git diff --check`.
- Never commit credentials, private keys, generated caches, or real forensic data.

Security-sensitive changes require a clear threat model, failure behavior, and reviewer attention. Do not describe an unimplemented control as verified or compliant.

## Pull requests

Use a descriptive title, identify affected components, document test results, and call out backward-incompatible changes. Maintainers may request additional review for execution, cryptography, identity, or evidence-chain changes.
