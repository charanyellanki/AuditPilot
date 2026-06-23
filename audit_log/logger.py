"""State-machine decision logging.

Every claim run moves through a fixed sequence of states; this utility records
each transition as an append-only event so any decision (auto-clear / escalate)
can be reconstructed and defended after the fact. This is the compliance backbone
of the system — the trail must be complete and tamper-evident.

Status: scaffold — state machine + logger contract only, no persistence yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AuditState(str, Enum):
    """Lifecycle states a claim passes through during validation.

    Distinct from graph.state.AuditState (the data payload); this is the
    decision-logging state machine.
    """

    RECEIVED = "received"
    RETRIEVED = "retrieved"
    VALIDATED = "validated"
    GROUNDED = "grounded"
    TRIAGED = "triaged"
    AUTO_CLEARED = "auto_cleared"
    ESCALATED = "escalated"
    FAILED = "failed"


# Allowed transitions; used to reject out-of-order / invalid logging.
ALLOWED_TRANSITIONS: dict[AuditState, set[AuditState]] = {
    AuditState.RECEIVED: {AuditState.RETRIEVED, AuditState.FAILED},
    AuditState.RETRIEVED: {AuditState.VALIDATED, AuditState.FAILED},
    AuditState.VALIDATED: {AuditState.GROUNDED, AuditState.FAILED},
    AuditState.GROUNDED: {AuditState.TRIAGED, AuditState.FAILED},
    AuditState.TRIAGED: {AuditState.AUTO_CLEARED, AuditState.ESCALATED, AuditState.FAILED},
    AuditState.AUTO_CLEARED: set(),
    AuditState.ESCALATED: set(),
    AuditState.FAILED: set(),
}


@dataclass
class AuditEvent:
    """A single recorded transition."""

    claim_id: str
    from_state: AuditState | None
    to_state: AuditState
    timestamp: str = ""              # ISO-8601 UTC; set at record time
    payload: dict[str, Any] = field(default_factory=dict)


class AuditLogger:
    """Append-only logger that enforces the transition state machine."""

    def __init__(self, claim_id: str, log_dir: str | None = None) -> None:
        """Initialize a logger for one claim run.

        # TODO: resolve log_dir from AUDIT_LOG_DIR; open an append-only sink
        #       (JSONL per claim_id). Consider hash-chaining events for
        #       tamper-evidence.
        """
        self.claim_id = claim_id
        self._current: AuditState | None = None
        raise NotImplementedError

    def record(self, to_state: AuditState, **payload: Any) -> AuditEvent:
        """Validate and append a transition to `to_state`.

        # TODO: assert to_state is in ALLOWED_TRANSITIONS[self._current];
        #       timestamp, append to the sink, advance self._current.
        """
        raise NotImplementedError

    def history(self) -> list[AuditEvent]:
        """Return the recorded events for this claim in order.

        # TODO: read back the claim's events from the sink.
        """
        raise NotImplementedError
