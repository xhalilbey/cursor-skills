# Evaluation Design

## Evaluation Layers

| Layer | Example checks |
| --- | --- |
| Contract | schema validity, required fields, forbidden fields |
| Semantic | extraction precision/recall, answer correctness |
| Grounding | supported claims, citation coverage, retrieval miss rate |
| Tools | correct tool, arguments, authorization, side-effect result |
| Memory | duplicate facts, supersession, identity joins, stale state |
| Routing | selected model/agent/lane, fallback reason, unnecessary escalation |
| Operations | latency, timeout, retry count, token and monetary cost |
| Safety | unauthorized actions, secret exposure, prompt injection resistance |

## Dataset Structure

Each case should record:

```json
{
  "case_id": "stable-id",
  "source": "production-failure|synthetic|expert-authored",
  "input": {},
  "expected": {},
  "constraints": [],
  "slice_tags": [],
  "labeler": "independent-owner",
  "label_version": "v1"
}
```

Store large payloads by content hash when duplication would be expensive. Keep private data minimized and access-controlled.

## Release Gate Template

```text
Hard gates:
- 100% schema validity
- 0 unauthorized side effects
- 0 secret exposure
- 100% pass on critical regression cases

Quality gates:
- no critical slice regresses by more than the agreed delta
- overall primary metric improves or remains within tolerance
- retrieval/citation support meets target

Operational gates:
- p95 latency within budget
- average cost within budget
- timeout and fallback rates within limits
```

Thresholds must come from product risk and baseline evidence, not generic defaults.

## Judge Use

Use an LLM judge only when:

- the rubric is explicit,
- examples calibrate score boundaries,
- a human-reviewed sample measures judge agreement,
- judge model and prompt versions are pinned,
- deterministic checks run separately.

Inspect disagreement cases. A high judge average can hide unsupported claims, style bias, or preference for longer answers.

## Variance

For non-deterministic workloads:

- repeat representative cases,
- report confidence intervals or pass-frequency distributions,
- distinguish flaky cases from consistently bad cases,
- avoid declaring small deltas meaningful without enough samples.

## Production Feedback Loop

```text
production trace
  -> privacy filter
  -> failure triage
  -> independent label
  -> regression dataset
  -> candidate comparison
  -> release gate
  -> canary
  -> monitoring
```

Do not automatically ingest user feedback or model outputs as labels.
