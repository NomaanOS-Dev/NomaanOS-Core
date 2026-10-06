name: Bug report
about: Report a reproducible bug in NomaanOS-Core
title: ""
labels: bug
assignees: ""

body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug. Please provide the details below.

  - type: textarea
    id: description
    attributes:
      label: Bug description
      description: What happened, and what did you expect?
      placeholder: Describe the bug
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Reproduction steps
      description: Tell us how to reproduce the issue.
      placeholder: 1. Run ...\n2. See error ...
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, commit/hash, and relevant configuration.
      placeholder: Ubuntu 22.04, Python 3.11, commit abc123
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs / console output
      description: Paste logs or errors if available.
      render: shell
