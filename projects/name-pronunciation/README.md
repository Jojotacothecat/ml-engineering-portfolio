# name-pronunciation

## Problem
Support specialists in Salesforce look up how to say
customer names. Goal = given a name, produce its pronunciation.

## Scope / boundary
What this IS: a function `pronounce(name) -> Pronunciation`.
What this is NOT: training a model to produce pronunciations. 

## Contract
The interface + output schema (ipa, respelling, confidence, notes).
```
class Pronunciation(BaseModel):
    ipa: str
    respelling: str
    confidence: float
    notes: str
```

## Approach: Running locally (Ollama)
LLM call via a local open-weight model (`qwen2.5:7b`) served by Ollama,
reached through its OpenAI-compatible API (`http://localhost:11434/v1`). Provider is therefore swappable:
one `base_url` change points the same code at OpenAI/Anthropic instead.

Chosen local because (1) free — no per-token billing, and (2) privacy:
customer names never leave the machine for a third-party API, which matters
for the real Salesforce use case (PII/compliance).

### One-time setup
    brew install ollama           # install (or download the app from ollama.com)
    ollama pull qwen2.5:7b        # download the model (~4.7GB, cached in ~/.ollama/models)

### Every session
    ollama serve                  # start the local server (or just open the Ollama app)
    # server listens on 127.0.0.1:11434 and stays running — leave it in its own terminal

### Run the project (in a second terminal)
    uv run pronounce.py           # single name
    uv run evaluate.py            # full gold-set eval -> artifacts/

### Handy checks
    ollama list                              # models installed + sizes
    curl http://localhost:11434/v1/models    # confirm server is reachable
    du -sh ~/.ollama/models                  # disk used by models
    ollama rm qwen2.5:7b                      # remove a model

## Correctness policy
most-common-US

## Evaluation
Gold set in data/gold.csv (38 names, hard cases included).
Metrics: Character level CER for IPA; human accept/reject for respelling.

## Findings

Local open-weight LLMs can generate name → IPA, but neither tested model is
production-grade. Best local result: qwen2.5:14b at ~0.42 segmental IPA CER.

**Capacity helps — broadly.** Moving 7b → 14b lowered overall CER 0.52 → 0.42,
with dramatic gains where 7b was failing:
- Jennifer (a top-100 name): 0.75 → 0.00 — 7b produced "jeh-FRIN"; 14b nailed it.
- English surname traps (Cholmondeley, Featherstonehaugh): 0.83 → 0.44
- Initials: 0.83 → 0.50 · Non-Latin orthography: 0.54 → 0.31

**But a hard core resists scale.** Some categories were flat across both models:
- Transliteration where spelling doesn't determine sound — Nguyen: 1.00 → 1.00
- Spanish: 0.61 → 0.61

Nguyen stuck at 1.0 regardless of model size shows its pronunciation is not
recoverable from spelling ("win" from "Nguyen" is arbitrary/cultural). No LLM
scaling fixes this class — it needs a lookup. This is the evidence-based case
for a dictionary+LLM hybrid on non-derivable names.

**Confidence is miscalibrated.** Self-reported confidence sat at ~0.6–0.75
almost regardless of correctness (Jennifer wrong-but-0.75 on 7b; Smith
perfect-but-0.6). Unusable for triage as-is.

**One designed behavior worked:** both models correctly declined the
unpronounceable policy-breaker (X Æ A-12) with low confidence — the only
abstention in either run.

## Limitations

- **Gold labels are unverified drafts** — absolute CER is soft. Relative
  comparisons (14b > 7b) are robust; the exact 0.42 is not.
- **Metric approximates.** Character-level CER on IPA is a proxy for true
  phoneme error rate; differing-but-valid IPA transcription conventions
  inflate it.
- **Small set** (38 names) — directional, not statistically powered.
- **Respelling not scored** (deferred to human accept/reject).
- **Cost/latency not measured**; no dictionary baseline (so "does the LLM beat
  a free lookup?" is unanswered by design).

## Next steps (not in scope for phase 1)
Verify gold set · calibrate confidence · dict+LLM hybrid for non-derivable
names · measure latency/cost · deployment design (precompute IPA, store, serve).
## Status
phase-1 complete
