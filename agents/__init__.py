"""The four AuditPilot agents, one module each.

retrieval_agent   -> pull relevant coding guidance from ChromaDB
validation_agent  -> check each billed code against the clinical note
grounding_verifier-> quote-grounded LLM-as-judge; drop ungrounded findings
triage_agent      -> risk-score and route (auto-clear vs. escalate)

Each agent exposes a `run(state: AuditState) -> dict` node function suitable for
registration with the LangGraph in `graph.build_graph`.
"""
