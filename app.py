"""Gradio demo entry point.

HuggingFace Spaces expects a root-level `app.py` that launches the UI. This
exposes a single-claim playground: paste billed ICD-10/CPT codes + a clinical
note, run the agent graph, and view the findings, grounding status, risk score,
and the auto-clear/escalate decision.

Run locally:

    python app.py

Status: scaffold — UI shell only; the pipeline call is a TODO.
"""

from __future__ import annotations

import os

# A short sample to pre-fill the demo so reviewers see the expected input shape.
EXAMPLE_NOTE = (
    "TODO: drop in a de-identified, Synthea-derived clinical note here so the "
    "demo loads with a runnable example."
)
EXAMPLE_ICD10 = "E11.9"   # Type 2 diabetes mellitus without complications
EXAMPLE_CPT = "99214"     # Office/outpatient visit, established patient


def validate_claim(icd10_codes: str, cpt_codes: str, clinical_note: str) -> dict:
    """Run the agent graph for one claim and return a UI-friendly result.

    Args:
        icd10_codes: Comma-separated ICD-10 codes from the UI.
        cpt_codes: Comma-separated CPT codes from the UI.
        clinical_note: Free-text clinical documentation.

    Returns:
        A dict rendered as JSON in the UI (decision, risk_score, findings).

    # TODO: parse code lists, build the initial AuditState, invoke
    #       graph.get_graph(), and shape the output for display.
    """
    raise NotImplementedError


def build_ui():
    """Construct the Gradio Blocks interface.

    # TODO: inputs (two textboxes for codes + a notes textarea, Validate button),
    #       outputs (JSON for findings/decision, a Markdown grounding summary),
    #       and a clearly visible "synthetic data / scaffold" disclaimer.
    """
    import gradio as gr

    with gr.Blocks(title="AuditPilot") as demo:
        gr.Markdown(
            "# 🩺 AuditPilot\n"
            "Validate whether billed ICD-10/CPT codes are supported by the "
            "clinical note.\n\n"
            "> **Scaffold:** pipeline not yet implemented. Synthetic data only."
        )
        # TODO: add input/output components and wire the Validate button to
        #       validate_claim.
    return demo


def main() -> None:
    """Launch the demo. Honors $PORT for HF Spaces / Docker."""
    demo = build_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )


if __name__ == "__main__":
    main()
