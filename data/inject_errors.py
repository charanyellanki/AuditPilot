"""Inject labeled coding errors into clean Synthea-derived claims.

Synthea records are internally consistent (codes already match the note), so we
mutate a copy of each claim to create a supervised error-detection dataset. Each
mutation is recorded as ground-truth so the eval harness can score detections.

See data/README.md for the rationale and the Synthea generation steps.

Run as a module:

    python -m data.inject_errors --in data/processed --out data/labeled --rate 0.4

Status: scaffold — signatures and contracts only, no implementation yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class ErrorType(str, Enum):
    """Supported synthetic coding-error categories."""

    UPCODING = "upcoding"
    UNSUPPORTED_PROCEDURE = "unsupported_procedure"
    MISSING_DOCUMENTATION = "missing_documentation"


@dataclass
class Claim:
    """A single claim consumed by the agent graph.

    Attributes:
        claim_id: Stable identifier for the claim.
        icd10_codes: Billed diagnosis codes.
        cpt_codes: Billed procedure codes.
        clinical_note: Free-text clinical documentation backing the claim.
    """

    claim_id: str
    icd10_codes: list[str]
    cpt_codes: list[str]
    clinical_note: str


@dataclass
class ErrorLabel:
    """Ground-truth description of an injected error (empty if claim is clean)."""

    error_type: ErrorType | None = None
    original_code: str | None = None
    mutated_code: str | None = None
    # Character span in the clinical note that was added/removed/edited, if any.
    affected_span: tuple[int, int] | None = None
    notes: str = ""


@dataclass
class LabeledClaim:
    """A (possibly mutated) claim paired with its ground-truth label."""

    claim: Claim
    label: ErrorLabel = field(default_factory=ErrorLabel)

    @property
    def is_clean(self) -> bool:
        return self.label.error_type is None


def inject_upcoding(claim: Claim) -> LabeledClaim:
    """Swap a billed code for a higher-acuity code the note does not support.

    # TODO: pick a target code from an upcoding crosswalk (e.g. unspecified ->
    #       severe, or a higher-paying DRG-adjacent code) and record the swap.
    """
    raise NotImplementedError


def inject_unsupported_procedure(claim: Claim) -> LabeledClaim:
    """Add a CPT procedure code with no supporting documentation in the note.

    # TODO: select a plausible-but-undocumented procedure code and append it
    #       without adding any justifying note text.
    """
    raise NotImplementedError


def inject_missing_documentation(claim: Claim) -> LabeledClaim:
    """Remove the note text that justifies an otherwise-correct diagnosis.

    # TODO: locate the sentence(s) supporting a billed ICD-10 code and strip
    #       them, recording the removed span as the label.
    """
    raise NotImplementedError


# Dispatch table mapping each error type to its injector.
INJECTORS = {
    ErrorType.UPCODING: inject_upcoding,
    ErrorType.UNSUPPORTED_PROCEDURE: inject_unsupported_procedure,
    ErrorType.MISSING_DOCUMENTATION: inject_missing_documentation,
}


def load_clean_claims(input_dir: Path) -> list[Claim]:
    """Load parsed clean claims from `input_dir`.

    # TODO: read processed Synthea claims (JSONL) into Claim objects.
    """
    raise NotImplementedError


def build_labeled_dataset(
    claims: list[Claim],
    error_rate: float = 0.4,
    seed: int = 12345,
) -> list[LabeledClaim]:
    """Return a labeled dataset: ~`error_rate` of claims get one injected error.

    Args:
        claims: Clean input claims.
        error_rate: Fraction of claims to mutate; the rest stay clean.
        seed: RNG seed for reproducible error selection.

    # TODO: deterministically choose which claims to mutate and which error
    #       type each gets (roughly balanced across ErrorType), then dispatch
    #       through INJECTORS.
    """
    raise NotImplementedError


def write_labeled_dataset(dataset: list[LabeledClaim], output_dir: Path) -> None:
    """Persist labeled claims (claim + ground-truth label) to `output_dir`.

    # TODO: serialize to JSONL with a schema_version for forward compatibility.
    """
    raise NotImplementedError


def main() -> None:
    """CLI entry point.

    # TODO: argparse for --in/--out/--rate/--seed; wire load -> build -> write.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
