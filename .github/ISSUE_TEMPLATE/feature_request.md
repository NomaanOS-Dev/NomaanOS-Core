name: Feature request
about: Suggest a capability or enhancement for NomaanOS-Core
title: ""
labels: enhancement
assignees: ""

body:
  - type: markdown
    attributes:
      value: |
        Suggest a useful enhancement for the project.

  - type: textarea
    id: problem
    attributes:
      label: Problem or use case
      description: What need are you trying to satisfy?
      placeholder: Example: better offline telemetry for mobile devices
    validations:
      required: true

  - type: textarea
    id: proposal
    attributes:
      label: Proposal
      description: Describe the proposed design or behavior.
      placeholder: Describe the idea
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: List other approaches you examined.
      placeholder: None
