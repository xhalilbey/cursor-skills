# Upsonic API Decision Reference

Use this reference for implementation details after selecting the architecture in `SKILL.md`. Verify APIs against the installed Upsonic version because the framework changes frequently.

Checked against official Upsonic documentation on 2026-06-11.

## Primitive Selection

### Direct

Use `Direct` for one model transformation without agent memory or tool orchestration.

```python
from pydantic import BaseModel
from upsonic import Direct, Task


class Result(BaseModel):
    answer: str
    confidence: float


direct = Direct(model=local_model)
result = direct.do(Task(description="Classify this record.", response_format=Result))
```

Official docs: https://docs.upsonic.ai/concepts/direct-llm-call/overview

### Agent and Task

Use `Agent` with a narrowly described `Task` for bounded tool use or reusable role configuration.

```python
from upsonic import Agent, Task

agent = Agent(model=local_model, name="Invoice Extractor")
task = Task(
    description="Extract invoice payment terms and cite the supporting text.",
    context=[invoice_path],
)
result = agent.do(task)
```

Attach tools to `Task` when only one task needs them. Attach tools to `Agent` only when every task should see them.

Official docs:

- https://docs.upsonic.ai/concepts/agents/overview
- https://docs.upsonic.ai/concepts/tasks/overview
- https://docs.upsonic.ai/concepts/tools/advanced/adding-tools

### Task Chaining

Use previous `Task` objects as context for explicit, short pipelines.

```python
extract = Task("Extract relevant evidence", context=[document_path])
extractor.do(extract)

normalize = Task(
    "Normalize the evidence into the application schema",
    context=[extract],
    response_format=ApplicationSchema,
)
normalizer.do(normalize)
```

For branching, loops, durable state, or complex retries, move orchestration to `StateGraph`.

Official docs: https://docs.upsonic.ai/concepts/tasks/context-management/adding-tasks-to-other-tasks-as-context

### StateGraph

Use `upsonic.graphv2.StateGraph` for explicit state and control flow.

```python
from typing_extensions import TypedDict
from upsonic.graphv2 import END, START, StateGraph


class WorkflowState(TypedDict):
    raw: str
    normalized: dict
    needs_review: bool


builder = StateGraph(WorkflowState)
builder.add_node("extract", extract_node)
builder.add_node("normalize", normalize_node)
builder.add_edge(START, "extract")
builder.add_edge("extract", "normalize")
builder.add_edge("normalize", END)
graph = builder.compile()
```

Keep nodes small. A node may be deterministic Python, `Direct`, or an `Agent` task. Use a checkpointer when execution must survive restarts.

Official docs: https://docs.upsonic.ai/concepts/stategraph/overview

### AutonomousAgent

Use `AutonomousAgent` for open-ended, iterative filesystem or shell work in a restricted workspace. Do not use it for a known banking or fintech decision flow that can be expressed as code.

```python
from upsonic import AutonomousAgent, Task

agent = AutonomousAgent(model=local_model, workspace=workspace_path)
result = agent.do(Task("Research the logs and identify likely anomaly causes"))
```

Official docs: https://docs.upsonic.ai/concepts/autonomous-agent/overview

### Team

Use `Team` only when specialists need dynamic routing, coordination, or independent expertise. Prefer fixed graphs for fixed sequences.

Available modes include sequential, coordinate, and route. Coordinate mode requires a leader model.

Official docs:

- https://docs.upsonic.ai/concepts/team/overview
- https://docs.upsonic.ai/concepts/team/choosing-right-team-mode

### Skills

Upsonic skills package reusable instructions, scripts, references, and assets. Agents see summaries first and load details progressively.

```python
from upsonic.skills import LocalSkills, Skills

skills = Skills(
    loaders=[LocalSkills("./company-skills")],
    auto_select=True,
    max_skills=3,
)
```

Attach a skill collection at task scope when only that task needs it. Keep `max_skills` low for local models. Enable strict dependency checks for controlled production skill sets, and apply skill safety policies when loading untrusted or remote skills.

Official docs:

- https://docs.upsonic.ai/concepts/skills/overview
- https://docs.upsonic.ai/concepts/skills/skill-format
- https://docs.upsonic.ai/concepts/skills/advanced/overview
- https://docs.upsonic.ai/concepts/skills/advanced/safety

## Local Model Providers

### Ollama

```python
from upsonic.models.ollama import OllamaModel, OllamaModelSettings

model = OllamaModel(
    model_name="llama3.2",
    settings=OllamaModelSettings(max_tokens=1024, temperature=0.1),
)
```

Set `OLLAMA_BASE_URL`, commonly `http://localhost:11434/v1/`.

Official docs: https://docs.upsonic.ai/concepts/llm-support/providers/ollama

### vLLM

```python
from upsonic.models.vllm import VLLMModel, VLLMModelSettings

model = VLLMModel(
    model_name="Qwen/Qwen2.5-7B-Instruct",
    settings=VLLMModelSettings(max_tokens=1024, temperature=0.1),
)
```

Set `VLLM_BASE_URL`, commonly `http://localhost:8000/v1`.

Official docs: https://docs.upsonic.ai/concepts/llm-support/providers/vllm

### Outlines

Use `OutlinesModel` when local structured generation is more important than tool use. Current Upsonic documentation states that Outlines supports JSON schema and JSON object output but not tool calls.

Official docs: https://docs.upsonic.ai/concepts/llm-support/providers/outlines

## Reliability Defaults

- Use Pydantic response models at the normalization or application boundary.
- Keep extraction output flexible enough to preserve evidence and ambiguity.
- Prefer task-scoped tools and skills.
- Set explicit timeouts and bounded retries.
- Use cache only for inputs whose result is safe to reuse.
- Add graph persistence for durable workflows.
- Use HITL approval before high-impact side effects.
- Record metrics and traces per stage.
- Run accuracy, reliability, and performance evaluations on the production model configuration.

Official docs:

- https://docs.upsonic.ai/concepts/evals/overview
- https://docs.upsonic.ai/concepts/agents/advanced/reliability-and-retries
- https://docs.upsonic.ai/concepts/hitl/overview
- https://docs.upsonic.ai/concepts/agents/metrics

## Version Discipline

Before editing production code:

1. Read the installed version from the lockfile or `importlib.metadata.version("upsonic")`.
2. Inspect existing imports and tests.
3. Confirm new APIs in that version's package or official docs.
4. Avoid silently upgrading Upsonic while implementing an unrelated agent change.
5. Add a focused test for the selected provider, response schema, and tool path.
