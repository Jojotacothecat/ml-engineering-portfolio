# name-pronunciation

## Problem
Goal = given a name, produce its pronunciation.

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
LLM call via local open-weight models (`qwen2.5:7b`,`qwen2.5:14b`,`qwen3.6:27b`) served by Ollama,
reached through its OpenAI-compatible API (`http://localhost:11434/v1`). Provider is therefore swappable:
one `base_url` change points the same code at OpenAI/Anthropic instead.

Chosen local because (1) free — no per-token billing, and (2) privacy:
customer names never leave the machine for a third-party API, which matters
for the real business use case (PII/compliance).

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
We compared 3 local models and find that IPA accuracy improves monotonically with size (CER 0.52 → 0.43 → 0.32), but the most accurate model's reasoning mode makes it operationally impractical for batch use — leaving the mid-size non-reasoning model as the best practical pick — while a naive dictionary+LLM hybrid *reduced* accuracy rather than improving it.

| Method                 | Overall IPA CER | Note                                         |
|------------------------|-----------------|----------------------------------------------|
| qwen2.5:7b             | 0.52            | weak                                         |
| qwen2.5:14b            | 0.43            | fast, non-reasoning                          |
| qwen3.6:27b            | 0.32            | best accuracy; reasoning mode impractical    |
| CMUdict + 27b (hybrid) | 0.38            | dictionary HURT overall                      |

1. **Capacity helps, monotonically** (0.52 → 0.43 → 0.32 across 7b/14b/27b).
   This revises a phase-1 claim: 27b largely *cracked* Nguyen (1.00 → ~0.00),
   so "unrecoverable from spelling" was premature — a capable model derives it.

2. **Reasoning isn't free.** 27b is a reasoning model; its mandatory thinking
   made batch evaluation operationally impractical (minutes/name, unbounded
   output, KV-cache/SWA pressure). For a bounded, high-throughput lookup, the
   non-reasoning 14b is the better *operational* choice despite ~0.11 higher CER.
   Model selection = accuracy AND operational fit.

3. **The naive hybrid reduced accuracy (0.32 → 0.38).** CMUdict *has* entries for
   transliterated names but they're anglicized/spelling-based, so presence-based
   routing overrode the LLM's correct answers (Nguyen 0.00 → 1.33). It also
   mismatched IPA conventions on easy names (control 0.05 → 0.13). It helped only
   where the LLM was weak on common names (arabic 0.62→0.33, spanish, multisyllable).
   Coverage-based routing is too aggressive; a confidence/convention-aware router
   is required.

4. **Confidence remains miscalibrated** (~flat 0.6–0.75 regardless of correctness),
   so it cannot yet gate a smarter hybrid. A rigorous reliability-diagram / ECE
   analysis is the natural next step.

## Limitations

- **Gold labels are unverified drafts** — absolute CER is soft. Relative
  comparisons (27b > 14b > 7b) are robust; the exact 0.32 is not.
- **Metric approximates.** Character-level CER on IPA is a proxy for true
  phoneme error rate; differing-but-valid IPA transcription conventions
  inflate it.
- **Small set** (38 names) — directional, not statistically powered.
- **Respelling not scored** (deferred to human accept/reject).


## Status
Complete
