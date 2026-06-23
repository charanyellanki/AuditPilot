"""Evaluation harness.

Runs the compiled graph over the labeled dataset and reports three families of
metrics, logging runs + params + artifacts to MLflow:

  1. Precision@k    — of the top-k flagged coding errors, how many are real
                      (match an injected ground-truth label)?
  2. Grounding faithfulness — fraction of surfaced findings backed by a valid
                      verbatim source span (the guardrail's core promise).
  3. Business readout — estimated recovery dollars and human review-hours saved
                      at a given triage threshold (illustrative, synthetic data).

Run as a module:

    python -m eval.harness --dataset data/labeled --k 5 --threshold 0.5

Status: scaffold — signatures and contracts only, no implementation yet.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PrecisionAtK:
    k: int
    precision: float
    num_flagged: int
    num_true_positive: int


@dataclass
class GroundingReport:
    total_findings: int
    grounded_findings: int

    @property
    def faithfulness(self) -> float:
        """Share of findings that passed verbatim grounding (0 if none)."""
        return self.grounded_findings / self.total_findings if self.total_findings else 0.0


@dataclass
class BusinessReadout:
    """Illustrative business impact at a chosen operating point."""

    threshold: float
    estimated_recovery_usd: float        # $ exposure on correctly escalated claims
    review_hours: float                  # auditor hours implied by escalations
    review_hours_saved_vs_manual: float  # vs. reviewing 100% of claims


@dataclass
class EvalResults:
    precision_at_k: PrecisionAtK
    grounding: GroundingReport
    business: BusinessReadout


def load_labeled_dataset(path: str) -> list:
    """Load labeled claims (claim + ground-truth ErrorLabel) for scoring.

    # TODO: read data/labeled JSONL produced by data.inject_errors.
    """
    raise NotImplementedError


def run_pipeline(dataset: list) -> list:
    """Run the compiled graph over each claim, collecting per-claim outputs.

    # TODO: graph.build_graph.get_graph().invoke(initial_state) per claim;
    #       capture findings, rejected_findings, decision, risk_score.
    """
    raise NotImplementedError


def precision_at_k(predictions: list, labels: list, k: int) -> PrecisionAtK:
    """Compute precision@k of flagged errors vs. injected ground truth.

    # TODO: rank findings by confidence/risk, compare top-k to labels by
    #       (claim_id, code, error_type).
    """
    raise NotImplementedError


def grounding_faithfulness(predictions: list) -> GroundingReport:
    """Compute the grounded fraction across all surfaced findings.

    # TODO: count grounded vs. total findings emitted by the grounding verifier.
    """
    raise NotImplementedError


def business_readout(predictions: list, labels: list, threshold: float) -> BusinessReadout:
    """Translate detections into recovery-$ and review-hours at `threshold`.

    # TODO: apply per-claim dollar estimates + per-review hour cost; compare
    #       escalation volume against a review-everything baseline.
    """
    raise NotImplementedError


def evaluate(dataset_path: str, k: int = 5, threshold: float = 0.5) -> EvalResults:
    """Full evaluation: load -> run -> score, logging everything to MLflow.

    # TODO: wrap in mlflow.start_run(); log params (k, threshold, model ids),
    #       metrics (precision@k, faithfulness, $$ / hours), and artifacts
    #       (per-claim findings, confusion details).
    """
    raise NotImplementedError


def main() -> None:
    """CLI entry point.

    # TODO: argparse for --dataset/--k/--threshold; pretty-print EvalResults.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
