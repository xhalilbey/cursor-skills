---
name: distributed-systems-investigator
description: Diagnose and verify failures across distributed event pipelines, queues, consumer groups, workers, APIs, databases, vector stores, analytics stores, retries, dead-letter paths, and asynchronous consistency boundaries. Use for Kafka lag, missing events, duplicate processing, out-of-order writes, worker stalls, partial persistence, Supabase/Qdrant/ClickHouse divergence, throughput collapse, backpressure, and end-to-end data-loss investigations.
---

# Distributed Systems Investigator

Trace one concrete unit of work through the complete system before proposing a fix. Prefer event IDs, partition keys, correlation IDs, consumer offsets, durable rows, and timestamps over broad log searching.

Read [references/investigation-playbook.md](references/investigation-playbook.md) for the evidence matrix and failure patterns. When working in Sculptors Agent, also read the local service README and use its current topology and commands as the source of truth.

## Workflow

1. Define the expected journey.
   - Name the ingress, durable boundaries, queue topics, consumer groups, workers, stores, and final observable outcome.
   - Separate acknowledged delivery, durable persistence, processing completion, and derived-index visibility.

2. Choose a trace key.
   - Prefer an event ID plus tenant/workspace/entity identity and partition key.
   - Record the expected ordering and idempotency key.
   - Do not infer end-to-end success from HTTP success alone.

3. Inspect each boundary in order.
   - Ingress acceptance and validation
   - Producer publish and partition assignment
   - Broker offset and consumer-group ownership
   - Worker claim, retry, timeout, and commit behavior
   - Canonical database transaction
   - Analytics/audit persistence
   - Derived vector or search indexing
   - Final retrieval or user-facing response

4. Classify the first broken invariant.
   - Never-produced
   - Produced but unconsumed
   - Consumed but uncommitted
   - Committed before side effect
   - Partially persisted
   - Persisted but not indexed
   - Indexed with stale or wrong identity
   - Correct data hidden by retrieval/filtering

5. Reproduce at the smallest safe scale.
   - Start with one event, then a small ordered batch, then concurrency.
   - Preserve production partitioning and retry semantics.
   - Avoid cleanup or replay until evidence is captured.

6. Implement only after diagnosis when the user asked for a fix.
   - Add an invariant test that fails before the change.
   - Make the smallest change at the first broken boundary.
   - Verify retries, duplicates, ordering, shutdown, and partial failure.

## Evidence Standard

For every conclusion, identify:

- verified evidence,
- inference,
- missing evidence,
- alternative explanations,
- the command or artifact that would falsify the conclusion.

Do not call an incident resolved because queues are empty. Verify the final canonical and derived states for known trace keys.

## Safety

- Treat replay, topic reset, record deletion, consumer-group offset changes, and production writes as state-changing operations requiring explicit authority.
- Never print secrets or full sensitive payloads.
- Prefer read-only broker, database, and log inspection during diagnosis.
- Preserve unrelated local changes and existing operational artifacts.

## Verification

Use the repository's established checks. For Sculptors Agent, typical evidence includes targeted pytest cases, preflight checks, Kafka group/offset inspection, canonical Supabase rows, ClickHouse event/audit rows, Qdrant payload coverage, and the existing memory quality/e2e reports.
