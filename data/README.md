# data/ — synthetic records and ground-truth labels

This directory covers how AuditPilot obtains its evaluation data: generating
Synthea synthetic patient records and then **injecting labeled coding errors**
into them.

## Why we inject errors

[Synthea](https://github.com/synthetichealth/synthea) produces *internally
consistent* records — the ICD-10 / CPT codes it emits already agree with the
conditions and encounters it simulated. That is exactly what makes it unusable
as-is for an error-detection task: there is nothing to detect and nothing to
label.

So AuditPilot deliberately mutates a copy of each claim, recording the mutation
as a **ground-truth label**. A claim is either left clean or has exactly one
injected error of a known type, giving us a supervised detection dataset.

> ⚠️ Metrics computed on this data measure performance against *our* synthetic
> error distribution, not real payer claims. See the caveat in the top-level
> [README](../README.md).

## Generating Synthea records (notes)

> TODO: pin a Synthea release and capture exact commands/seed for reproducibility.

1. Install Synthea (requires Java). Use the release JAR or build from source:
   https://github.com/synthetichealth/synthea
2. Generate a population with a fixed seed (FHIR or CSV export), e.g.:
   ```bash
   java -jar synthea-with-dependencies.jar -p 1000 -s 12345 \
        --exporter.fhir.export true
   ```
3. Place raw output under `data/synthea_output/` (git-ignored).
4. A loader (TODO) parses encounters into the internal `Claim` shape consumed by
   the graph: billed ICD-10 + CPT codes plus the associated clinical note text.

## Error injection

`inject_errors.py` takes clean claims and produces a labeled dataset under
`data/labeled/` (git-ignored). Supported error types:

| Type | What it does |
|------|--------------|
| `upcoding` | Replace a billed code with a higher-acuity/-reimbursement code the note does not support. |
| `unsupported_procedure` | Add a CPT procedure code with no corresponding documentation in the note. |
| `missing_documentation` | Remove the note text that justifies an otherwise-correctly-billed diagnosis. |

Each injected record carries a label describing the mutation (original code,
mutated code, error type, and the span touched) so the eval harness can score
detections.

## Directory contents (planned)

```
data/
├── README.md             # this file
├── inject_errors.py      # error-injection CLI (stub)
├── synthea_output/       # raw Synthea export        (git-ignored)
├── processed/            # parsed clean claims       (git-ignored)
└── labeled/              # claims + injected labels  (git-ignored)
```
