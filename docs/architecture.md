# Architecture

```mermaid
flowchart LR
  M[Controlled model proposer] --> I[Versioned improver state]
  I --> C[SQL candidates]
  C --> S[Non-root Docker sandbox]
  D[Checksum-verified TLC Parquet] --> S
  A[Frozen evaluator authority] --> S
  S --> L[Append-only evidence ledger]
  L --> R[Meta revision and conditional memory]
  R --> I
  H[Held-out February workload] -->|once after freeze| S
```

The proposer cannot read the repository, raw data or protected evaluator. Evaluated SQL runs with no network, a read-only filesystem, fixed CPU/memory/time budgets and an allowlisted SQL grammar. The host verifies authority hashes before every container run. Development and selection tasks drive search; held-out tasks are mounted only for the single final evaluation of a frozen run.
