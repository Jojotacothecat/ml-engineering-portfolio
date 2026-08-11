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

Baseline = dictionary lookup (CMUdict); the model must beat it to justify itself.

## Correctness policy
most-common-US

## Evaluation
Gold set in data/gold.csv (38 names, hard cases included).
Metrics: Character level CER for IPA; human accept/reject for respelling.

## Status
phase-1 scratch
