name: Bug report
about: Report a reproducible issue in NomaanOS-Core
labels: bug
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug.
  - type: textarea
    id: description
    attributes:
      label: Bug description
      description: What happened and what did you expect?
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Reproduction steps
      description: Provide the steps to reproduce the issue.
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, and relevant setup information.
      required: true
