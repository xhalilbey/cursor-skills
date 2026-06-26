---
name: agent-builder
description: Design, implement, review, and debug production AI agents with Upsonic, especially local-model workflows using Agent, Task, Direct, StateGraph, Skills, Team, AutonomousAgent, MCP, Ollama, vLLM, or Outlines. Use for agent architecture, prompt and task decomposition, structured outputs, tool selection, avoiding unnecessary multi-agent or MCP complexity, local-model reliability, evaluations, retries, guardrails, and production readiness.
---

# Upsonic Agent Builder

Build narrow, observable workflows that match the model's capacity. Treat every agent, tool, MCP server, and prompt instruction as complexity that must earn its place.

Read [references/upsonic-api.md](references/upsonic-api.md) when implementation requires current Upsonic classes, imports, or provider-specific constraints.

## Core Principles

1. Separate business logic, not prompt text. Split stages when they have different goals, context, tools, output contracts, retry policies, permissions, or evaluation criteria.
2. Keep prompts small. Give each model call one well-defined cognitive job and only the context needed for that job.
3. Generate first, validate or normalize second. Do not force discovery, reasoning, policy checks, and final application formatting into one prompt.
4. Prefer software orchestration for known flows. Use typed state, ordinary functions, conditionals, queues, and validators when the next step is already known.
5. Use autonomy only where the path is genuinely open-ended, such as research or iterative workspace exploration.
6. Add multi-agent coordination or MCP only when it provides a concrete capability or isolation boundary.
7. Design for the deployed local model, not for cloud-model behavior observed during prototyping.

## Workflow

### 1. Inspect Before Designing

- Inspect the repository, installed Upsonic version, existing agent code, tests, model server, and deployment constraints.
- Use the installed package and project lockfile as the implementation source of truth. Consult official Upsonic docs when APIs are absent or ambiguous.
- Identify data sensitivity, side effects, latency limits, throughput, context limits, and hardware constraints.
- Preserve existing architecture unless it directly causes the reported failure.

### 2. Define the Case Contract

Write down:

- input and source of truth,
- required business result,
- acceptable uncertainty or abstention,
- side effects and approval boundaries,
- final machine contract,
- latency and cost budget,
- representative success and failure examples.

Do not start with agent count. Start with the case contract.

### 3. Map Cognitive and Deterministic Stages

Break the case into stages such as:

```text
ingest -> retrieve -> extract -> validate -> normalize -> decide -> act -> present
```

For each stage, classify it as:

- deterministic software,
- direct model call,
- tool-using task agent,
- open-ended autonomous work,
- human approval.

Keep deterministic transformations and routing in code. Use a model only where semantic judgment is required.

### 4. Choose the Smallest Upsonic Primitive

Use this order of preference:

| Problem shape | Default primitive |
| --- | --- |
| One semantic transform, no tools or memory | `Direct` + `Task` |
| One bounded task with a small tool set | `Agent` + `Task` |
| Known multi-step flow with branches, retries, or persistence | `StateGraph` |
| Open-ended research or workspace exploration | `AutonomousAgent` |
| Truly distinct specialists requiring dynamic coordination | `Team` |
| External capability exposed through a standard protocol | MCP tool |

Do not use `Team` to represent a fixed pipeline. A `StateGraph` or plain Python orchestration is usually clearer and more reliable.

### 5. Design Prompts by Layer

Keep these concerns separate:

- Agent role or goal: stable capability and behavior.
- Task description: one current objective.
- Tool schema and docstring: exact callable contract.
- Context: evidence needed for this task only.
- Response schema: machine-facing output contract.
- Policy and authorization: code, guardrails, or approval nodes.

Avoid long prompts that repeat schemas, tool descriptions, policies, and workflow instructions in multiple places.

Write task descriptions with:

```text
objective + relevant subject + evidence requirement + uncertainty behavior
```

Do not request hidden chain-of-thought. Give the model enough output budget to solve the task, then verify the observable answer and evidence.

### 6. Apply Generate-Then-Normalize

Use two stages when strict output pressure harms extraction or reasoning:

```python
from pydantic import BaseModel
from upsonic import Agent, Task


class AuthorityResult(BaseModel):
    person: str
    authority_type: str | None
    confidence: float
    evidence: list[str]


extractor = Agent(model=local_model, name="Authority Extractor")
normalizer = Agent(model=local_model, name="Authority Normalizer")

extract_task = Task(
    description=(
        "Find Mehmet's authority arrangement in the supplied signature circular. "
        "Return the relevant wording and supporting evidence. State when it is unclear."
    ),
    context=[document_path],
)
raw_result = extractor.do(extract_task)

normalize_task = Task(
    description="Normalize the extracted authority into the application contract.",
    context=[extract_task],
    response_format=AuthorityResult,
)
result = normalizer.do(normalize_task)
```

Prefer deterministic normalization when rules are explicit. Use a second model stage only when normalization itself requires semantic judgment.

### 7. Control Tool and Context Load

- Attach tools at task scope unless every task needs them.
- Give local models the smallest useful tool set. Similar or overlapping tools reduce selection reliability.
- Prefer native functions for internal APIs. Add MCP when remote discovery, interoperability, or an existing MCP ecosystem justifies its overhead.
- Load skills progressively and attach them at task scope when possible.
- Retrieve focused evidence instead of injecting entire documents or conversation histories.
- Keep untrusted retrieved content separated from instructions and validate all tool arguments server-side.

### 8. Engineer for Local Models

- Test the exact quantization, context size, chat template, and inference server used in production.
- Start with low temperature for extraction, classification, routing, and normalization.
- Verify tool calling and structured-output support for the selected provider. Outlines supports structured output but not tool calls.
- Reduce simultaneous constraints before increasing prompt detail.
- Keep schemas shallow, fields explicit, and optionality honest.
- Include `unknown`, `not_found`, confidence, and evidence where the business process permits uncertainty.
- Bound retries and vary the recovery strategy; do not repeat the same failing prompt indefinitely.
- Route hard or low-confidence cases to a stronger model or human review when available.

### 9. Add Production Controls

- Validate input and output with typed schemas.
- Make side-effecting tools idempotent and authorize them independently of the model.
- Require approval for irreversible, financial, legal, security-sensitive, or externally visible actions.
- Add timeouts, retry budgets, circuit breakers, and fallback behavior.
- Trace stage name, model, prompt version, tool calls, latency, parse failures, confidence, and final disposition without logging secrets.
- Keep model output as data; never execute generated code or commands without an explicit sandbox and policy.

### 10. Evaluate the Workflow

Build a case-specific evaluation set before broad rollout:

- normal cases,
- ambiguous cases,
- missing evidence,
- conflicting evidence,
- long or noisy documents,
- malformed tool results,
- prompt-injection content,
- repeated runs for consistency.

Measure per stage and end to end:

- task accuracy,
- schema-valid rate,
- evidence correctness,
- tool-call correctness,
- abstention quality,
- latency and resource use,
- retry and fallback rate.

Compare the simplest viable architecture against any proposed multi-agent design. Keep the more complex design only when the evaluation gain justifies its operational cost.

## Review Checklist

- Does each model call perform one coherent cognitive job?
- Is any deterministic logic still buried in a prompt?
- Is final formatting separated from discovery when constraints reduce quality?
- Can any agent, tool, skill, or MCP server be removed?
- Is `Team` being used where a graph or function pipeline is sufficient?
- Are tools scoped narrowly and validated outside the model?
- Are local-model capabilities tested rather than assumed?
- Are uncertainty, evidence, retries, fallbacks, and approvals explicit?
- Are stage-level evals and traces available?
- Does the implementation fail safely without silently inventing data?

## Common Failure Patterns

- One prompt performs retrieval, reasoning, policy enforcement, formatting, and action.
- Multiple agents exist only because the workflow has multiple steps.
- MCP wraps a simple internal function and adds no interoperability value.
- The model is asked to reproduce deterministic business rules from prose.
- A strict final JSON contract is imposed during difficult evidence discovery.
- Cloud-model prompts are copied to a smaller local model without re-evaluation.
- More instructions are added after every failure, creating conflicting constraints.
- Success is judged from a few demos instead of a repeatable case set.

When these appear, simplify the workflow before tuning the prompt.
