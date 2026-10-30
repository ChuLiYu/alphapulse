# AI design, trust boundaries and evaluation

Status: target design except for the existing isolated monitoring PoC. [Agent evidence](../agents/EVIDENCE.md) records what that PoC actually does. No portfolio RAG or automated investment decision system is implemented.

## Appropriate tasks

1. Explain a deterministic valuation/risk/mandate result by quoting its rule ID, snapshot, as-of date and actual tool values.
2. Draft an operations break summary from versioned reconciliation evidence, with links to the underlying records.
3. Summarize permission-filtered, licensed research with source chunks and dates; abstain when support is missing or inconsistent.

AI outputs are drafts for human review. There is no prediction-quality or alpha-generation claim. Calculation, mandate checks and approval transitions stay in typed deterministic application code.

## Data and action controls

- Authorize the user and portfolio **before** retrieval and again at each tool boundary. Filter storage/vector queries, not only the final model response. Partition caches by authorization context; revoke access on permission changes.
- Retrieved news, PDFs and tool content are untrusted data. Embedded instructions cannot change system policy or tool rights. Never allow arbitrary URLs, shell, unrestricted SQL, trade writes, approval, limit edits or secret access.
- Tools return typed evidence envelopes with record/version IDs, as-of time, source and explicit data quality. Invalid or missing evidence yields an abstention, not invented values or mock success.
- Validate model output against a schema. Citations must resolve to retrieved, authorized chunks; generated numbers must match tool evidence. Distinguish factual summary, inference and uncertainty in the UI.
- Minimize retained content, redact secrets/client identifiers, and define retention/deletion and provider data handling before hosted inference. Access-scoped tracing must not expose restricted source text to logs.
- Bound tool count, tokens, timeout, concurrency and retry budgets. Model/prompt/embedding versions and evaluation dataset revisions are recorded with each release; failure falls back to a deterministic evidence view.

## Evaluation gate

Create reviewed synthetic cases before integration: correct evidence, missing/stale marks, contradictory sources, unauthorized portfolio, malicious document instructions, forged citations, model timeout, malformed tool calls and sensitive content extraction attempts.

Measure task completion separately from correctness. Release requires: no unauthorized retrieval/action in adversarial fixtures; exact numerical grounding for displayed financial facts; every factual citation resolves to supporting authorized evidence; missing evidence produces abstention; failures preserve the deterministic workflow. Record sample size, error cases and human rubric alongside citation support rate, numeric consistency, latency, tokens and cost. Passing a small fixture set does not prove universal safety or reliability.

Do not substitute an LLM judge for financial or authorization oracles. Human review of interpretation remains necessary. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) informs risk identification and evaluation; this project makes no certification claim.
