# Module Contract

## Module

Name the module, feature, or workflow this contract covers.

## Source Issue

Link to the GitHub issue or problem representation.

## Tracker

Link to the tracker issue, if any.

## Owning Layer

State which project layer owns the truth for this contract.

## Internal Project Area

Choose the primary internal project area from `docs/internal_project_map.md`.
Use `N/A / unclear` only when the classification is genuinely ambiguous and
explain the ambiguity.

Future AI Integration is deferred vocabulary only. Naming it does not authorize
OpenAI or model-provider runtime integration, AI coaching evaluation, AI-owned
parser truth, AI-owned analytics truth, hidden-card truth, gameplay correctness
truth, or strategic certainty.

## Truth Owner

Name the layer or artifact that owns truth for the fields, behavior, workflow
state, or documentation vocabulary covered by this contract.

## Bridge-Code Status

Choose one:

- `not_bridge_code`
- `bridge_code`
- `shared_support`
- `ambiguous_pending_follow_up`
- `deferred_future_boundary`

For bridge-code work, name the source internal project area, consuming internal
project area, allowed data flow, forbidden reverse-flow, and protected surfaces
touched or explicitly not touched.

## Files Owned By This Contract

- TODO

## Public Interface

List the functions, classes, scripts, environment variables, sheet tabs,
columns, payload fields, docs artifacts, or workflow surfaces that other code
or agents may depend on.

## Inputs

For each input, include type, source, required fields, optional fields, and
example values.

## Outputs

For each output, include type, destination, field names, row shape, artifact
shape, and whether the value is provisional or final.

## Invariants

Rules that must always stay true.

- TODO

## Error Behavior

Describe what should happen on malformed input, missing source data, partial
workbook state, webhook failure, unavailable external data, contract ambiguity,
or conflicting workflow instructions.

## Side Effects

List files written, runtime state touched, webhooks posted, workbook tabs
updated, caches refreshed, issues created, PRs opened, or trackers updated.

## Dependency Order

If multiple files or layers change together, list the required edit order.

1. TODO

## Compatibility

Name any legacy names, bridge code, old tabs, old fields, old artifact shapes,
or migration behavior that must remain supported.

## Tests Required

List focused unit, integration, replay, Apps Script, workbook-visible,
documentation, or lifecycle checks.

```bash

```

## Acceptance Criteria

- TODO

## Next Workflow Action

Next role:

Pasteable prompt:

```text

```

```yaml
workflow_handoff:
  repository: ""
  repository_url: ""
  issue: ""
  tracker: ""
  completed_thread: "B"
  next_thread: "C"
  source_artifact: ""
  target_artifact: ""
  risk_tier: ""
  base_branch: ""
  target_branch: ""
  branch: ""
  validation:
    - ""
  stop_conditions:
    - ""
```
