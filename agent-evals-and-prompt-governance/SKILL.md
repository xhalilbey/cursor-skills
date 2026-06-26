---
name: agent-evals-and-prompt-governance
description: Design, implement, review, and operate evaluations and release governance for production AI agents and prompts. Use for golden datasets, regression tests, prompt/model/tool versioning, structured-output validation, retrieval grounding, tool-call correctness, memory quality, routing and fallback evaluation, cost/latency budgets, canary releases, rollback gates, and comparing agent versions with reproducible evidence.
---

# Agent Evals and Prompt Governance

Treat prompts, models, retrieval settings, tool schemas, and routing rules as one versioned behavioral release. Do not declare improvement from anecdotal examples or aggregate scores alone.

Use `agent-builder` for agent architecture and implementation. Use this skill to define how behavior is measured, compared, released, monitored, and rolled back.

Read [references/eval-design.md](references/eval-design.md) when selecting metrics, datasets, or release gates.

## Workflow

1. Define the behavior contract.
   - Inputs and source of truth
   - Required output or action
   - Allowed abstention and fallback
   - Forbidden side effects
   - Latency and cost limits
   - Evidence required for correctness

2. Inventory the release surface.
   - System/task prompts and templates
   - Model and effort settings
   - Tool names, schemas, permissions, and timeouts
   - Retrieval/index/filter configuration
   - Memory extraction and lifecycle rules
   - Deterministic routing, retries, and fallbacks

3. Build a versioned dataset.
   - Include happy paths, edge cases, adversarial inputs, historical failures, and realistic distributions.
   - Keep immutable case IDs and provenance.
   - Separate development, regression, and blind holdout sets.
   - Prevent generated outputs from silently becoming their own ground truth.

4. Choose metrics by failure mode.
   - Exact/schema validation for deterministic contracts
   - Precision/recall for extraction and routing
   - Citation support and retrieval coverage for grounded answers
   - Tool selection, argument correctness, side-effect success, and unnecessary-call rate
   - Duplicate, ordering, supersession, and stale-state rates for memory
   - P50/P95 latency, token use, and monetary cost
   - Human review for high-impact ambiguity

5. Compare candidate and baseline.
   - Run both on the same immutable cases.
   - Report per-slice deltas and regressions, not only averages.
   - Preserve raw outputs, traces, tool calls, model/config versions, and failures.
   - Require repeated runs when model variance can change the decision.

6. Gate release.
   - Block on hard safety or contract failures.
   - Set explicit maximum regression by critical slice.
   - Canary with stable assignment and observable rollback criteria.
   - Keep the previous known-good release immediately recoverable.

7. Monitor production.
   - Sample real failures into a review queue.
   - Add confirmed failures to the regression set after independent labeling.
   - Detect distribution drift, fallback growth, cost growth, and model/provider changes.

## Non-Negotiable Rules

- Never use an LLM judge as the sole gate for deterministic correctness.
- Never compare versions on different datasets or changed scoring code without labeling the comparison invalid.
- Never optimize a single aggregate score while critical slices regress.
- Never log secrets, raw credentials, or unnecessary personal data in traces.
- Never update golden labels merely to make the candidate pass.
- Keep prompt text and evaluation criteria independently reviewable.

## Deliverables

Produce the smallest set needed:

- behavior contract,
- dataset manifest,
- metric and slice table,
- baseline-versus-candidate report,
- failure taxonomy,
- release gate,
- canary and rollback plan,
- production monitoring plan.

## Verification

Before sign-off, confirm:

- every case has stable provenance and an immutable ID,
- scoring is deterministic where expected,
- raw evidence can reproduce the aggregate report,
- critical slices meet their thresholds,
- cost and latency stay within budget,
- the rollback target is known and tested,
- newly discovered failures become durable regression cases.
