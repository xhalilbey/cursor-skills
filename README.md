# cursor-skills

A curated library of agent skills for Cursor, Codex and Claude. Each folder holds a
`SKILL.md` (YAML frontmatter with `name` and `description`, then instructions) plus
optional `references/`, `scripts/` and `assets/`.

## Using a skill

Copy or symlink the folder into your tool's skills directory, for example:

```bash
ln -s "$PWD/senior-frontend" ~/.cursor/skills/senior-frontend
```

## Index

<!-- INDEX:START -->
_52 skills._

### Skills

| Skill | What it does |
| --- | --- |
| [`agent-builder`](agent-builder/SKILL.md) | Design, implement, review, and debug production AI agents with Upsonic, especially local-model workflows using Agent, Task, Direct, StateGraph, Skills, Team, A… |
| [`agent-designer`](agent-designer/SKILL.md) | Use when the user asks to design a multi-agent system, pick an orchestration pattern (supervisor/swarm/pipeline), generate tool schemas for agents, or evaluate… |
| [`agent-evals-and-prompt-governance`](agent-evals-and-prompt-governance/SKILL.md) | Design, implement, review, and operate evaluations and release governance for production AI agents and prompts. |
| [`agent-workflow-designer`](agent-workflow-designer/SKILL.md) | Design production-grade multi-agent workflows with clear pattern choice (sequential, parallel, hierarchical), handoff contracts, failure handling, and cost/con… |
| [`ai-security`](ai-security/SKILL.md) | Use when assessing AI/ML systems for prompt injection, jailbreak vulnerabilities, model inversion risk, data poisoning exposure, or agent tool abuse. |
| [`api-design-reviewer`](api-design-reviewer/SKILL.md) | Comprehensive REST API design review with automated linting, breaking-change detection, and design scorecards. |
| [`api-test-suite-builder`](api-test-suite-builder/SKILL.md) | Use when the user asks to generate API tests, create integration test suites, test REST endpoints, or build contract tests. |
| [`codebase-onboarding`](codebase-onboarding/SKILL.md) | Analyze a codebase and generate onboarding documentation for engineers, tech leads, and contractors. |
| [`content-creator`](content-creator/SKILL.md) | Deprecated redirect skill that routes legacy 'content creator' requests to the correct specialist. |
| [`copywriting`](copywriting/SKILL.md) | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, o… |
| [`database-designer`](database-designer/SKILL.md) | Use when the user asks to design database schemas, plan data migrations, optimize queries, choose between SQL and NoSQL, or model data relationships. |
| [`define-goal`](define-goal/SKILL.md) | Help the user define a concrete, measurable goal before starting work, especially when they ask to use the goal tool, create a goal, set an objective, clarify… |
| [`dependency-auditor`](dependency-auditor/SKILL.md) | Audit and manage dependencies across multi-language projects. |
| [`distributed-systems-investigator`](distributed-systems-investigator/SKILL.md) | Diagnose and verify failures across distributed event pipelines, queues, consumer groups, workers, APIs, databases, vector stores, analytics stores, retries, d… |
| [`env-secrets-manager`](env-secrets-manager/SKILL.md) | Manage environment-variable hygiene and secrets safety across local development and production. |
| [`experiment-designer`](experiment-designer/SKILL.md) | Use when planning product experiments, writing testable hypotheses, estimating sample size, prioritizing tests, or interpreting A/B outcomes with practical sta… |
| [`incident-commander`](incident-commander/SKILL.md) | Comprehensive incident response framework from detection through resolution and post-incident review. |
| [`landing-page-generator`](landing-page-generator/SKILL.md) | Generates high-converting landing pages as complete Next.js/React (TSX) components with Tailwind CSS. |
| [`llm-cost-optimizer`](llm-cost-optimizer/SKILL.md) | Use proactively whenever LLM API costs come up -- or should. |
| [`nextjs-app-router`](nextjs-app-router/SKILL.md) | Build, modify, review, or debug production Next.js applications, especially App Router projects using Server Components, Client Components, Server Actions, rou… |
| [`observability-designer`](observability-designer/SKILL.md) | Design production-ready observability strategies combining metrics, logs, and traces. |
| [`page-cro`](page-cro/SKILL.md) | When the user wants to optimize, improve, or increase conversions on any marketing page — including homepage, landing pages, pricing pages, feature pages, or b… |
| [`pr-review-expert`](pr-review-expert/SKILL.md) | Use when the user asks to review pull requests, analyze code changes, check for security issues in PRs, or assess code quality of diffs. |
| [`product-analytics`](product-analytics/SKILL.md) | Use when defining product KPIs, building metric dashboards, running cohort or retention analysis, or interpreting feature adoption trends across product stages. |
| [`prompt-governance`](prompt-governance/SKILL.md) | Use when managing prompts in production at scale: versioning prompts, running A/B tests on prompts, building prompt registries, preventing prompt regressions,… |
| [`rag-architect`](rag-architect/SKILL.md) | Use when the user asks to design a RAG pipeline, choose a chunking strategy or embedding model, pick a vector database, or evaluate retrieval quality (precisio… |
| [`runbook-generator`](runbook-generator/SKILL.md) | Generate operational runbooks from a service name — deployment, incident response, maintenance, and rollback workflows. |
| [`senior-frontend`](senior-frontend/SKILL.md) | Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. |
| [`senior-fullstack`](senior-fullstack/SKILL.md) | Fullstack development toolkit with project scaffolding for Next.js, FastAPI, MERN, and Django stacks, code quality analysis with security and complexity scorin… |
| [`senior-security`](senior-security/SKILL.md) | Use when the user asks for STRIDE threat modeling, DREAD risk scoring, data-flow-diagram threat analysis, or a quick secret scan — or when a security request n… |
| [`skill-security-auditor`](skill-security-auditor/SKILL.md) | Security audit and vulnerability scanner for AI agent skills before installation. |
| [`stripe-integration-expert`](stripe-integration-expert/SKILL.md) | Production-grade Stripe integrations: subscriptions with trials and proration, one-time payments, usage-based billing, checkout sessions, idempotent webhook ha… |
| [`web-security-review`](web-security-review/SKILL.md) | Review, design, or implement security-sensitive web, mobile backend, API, auth, database, storage, webhook, payment, Supabase, Next.js, Cloud Run, or agent-too… |

### cursor-builtin

| Skill | What it does |
| --- | --- |
| [`automate`](cursor-builtin/automate/SKILL.md) | Use this skill to create Cursor Automations. |
| [`babysit`](cursor-builtin/babysit/SKILL.md) | Keep a PR merge-ready by triaging comments, resolving clear conflicts, and fixing CI in a loop. |
| [`canvas`](cursor-builtin/canvas/SKILL.md) | A Cursor Canvas is a live React app that the user can open beside the chat. |
| [`create-hook`](cursor-builtin/create-hook/SKILL.md) | Create Cursor hooks. |
| [`create-rule`](cursor-builtin/create-rule/SKILL.md) | Create Cursor rules for persistent AI guidance. |
| [`create-skill`](cursor-builtin/create-skill/SKILL.md) | Create Cursor Agent Skills. |
| [`create-subagent`](cursor-builtin/create-subagent/SKILL.md) | Create custom subagents for specialized AI tasks. |
| [`loop`](cursor-builtin/loop/SKILL.md) | Run a prompt or skill in this session on a recurring or variable interval (e.g. /loop 5m /foo). |
| [`migrate-to-skills`](cursor-builtin/migrate-to-skills/SKILL.md) | Convert 'Applied intelligently' Cursor rules (.cursor/rules/*.mdc) and slash commands (.cursor/commands/*.md) to Agent Skills format (.cursor/skills/). |
| [`onboard`](cursor-builtin/onboard/SKILL.md) | Use /onboard for a focused Cursor onboarding flow that learns basic preferences, picks a first goal, and routes the user to the right next action. |
| [`review`](cursor-builtin/review/SKILL.md) | Review code changes with the Bugbot or Security Review subagent. |
| [`review-bugbot`](cursor-builtin/review-bugbot/SKILL.md) | Review code changes with Bugbot subagent. |
| [`review-security`](cursor-builtin/review-security/SKILL.md) | Review code changes with Security Review subagent. |
| [`sdk`](cursor-builtin/sdk/SKILL.md) | Guide users building apps, scripts, CI pipelines, or automations on top of the Cursor SDK - TypeScript (`@cursor/sdk`) or Python (`cursor-sdk` / `cursor_sdk`). |
| [`shell`](cursor-builtin/shell/SKILL.md) | Runs the rest of a /shell request as a literal shell command. |
| [`split-to-prs`](cursor-builtin/split-to-prs/SKILL.md) | Split current work into small reviewable PRs. |
| [`statusline`](cursor-builtin/statusline/SKILL.md) | Configure a custom status line in the CLI. |
| [`update-cli-config`](cursor-builtin/update-cli-config/SKILL.md) | View and modify Cursor CLI configuration settings in ~/.cursor/cli-config.json. |
| [`update-cursor-settings`](cursor-builtin/update-cursor-settings/SKILL.md) | Modify Cursor/VSCode user settings in settings.json. |

<!-- INDEX:END -->

## Contributing

1. Add a folder whose name matches the `name` in its `SKILL.md`.
2. Run `python3 scripts/validate_skills.py`.
3. Run `python3 scripts/build_readme.py` to refresh the index above.
