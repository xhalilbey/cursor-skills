# Investigation Playbook

## Boundary Evidence Matrix

| Boundary | Required evidence | Common false positive |
| --- | --- | --- |
| API ingress | request ID, accepted status, normalized event | HTTP 2xx without durable publish |
| Producer | topic, partition, offset or delivery confirmation | producer call returned without flush/ack |
| Kafka | partition key, high watermark, group lag, owner | total queue depth without per-partition view |
| Worker | claim timestamp, attempt, outcome, offset commit | process is running |
| Canonical store | committed row/version and idempotency result | audit log says write attempted |
| Analytics store | source event and audit row | aggregate count hides missing identities |
| Vector index | point ID, payload filters, embedding/version | collection count increased |
| Retrieval | exact filters, ranking inputs, returned fact IDs | semantic answer appears plausible |

## Failure Patterns

### Ack before durability

Ingress returns success before broker acknowledgement or before a durable outbox write. Prove whether accepted requests survive process termination.

### Commit before side effect

The consumer commits an offset before canonical persistence completes. A crash creates permanent loss without lag.

### Side effect before commit

The write succeeds but the offset is not committed. Reprocessing is safe only when the write is idempotent.

### Cross-store partial success

Supabase succeeds while ClickHouse or Qdrant fails. Define which store is canonical and how reconciliation repairs derived stores.

### Partition-key drift

Related events receive different keys before and after identity resolution. Ordering guarantees then apply to the wrong entity.

### Poison-event retry loop

A deterministic failure repeatedly blocks a partition. Verify attempt limits, dead-letter publication, and offset progression.

### Shutdown loss

Workers stop accepting work but exit before in-flight writes, producer flushes, or commits finish.

### Hidden success

Data exists but retrieval filters use stale tenant, workspace, state, lifecycle, or identity values.

## Minimal Test Ladder

1. One deterministic event.
2. Duplicate delivery of the same event.
3. Two ordered events for one entity.
4. Interleaved events for independent entities.
5. Forced transient storage failure.
6. Forced worker termination between write and commit.
7. Replay from the last safe offset.
8. End-to-end retrieval validation.
