# name-pronunciation

## Problem
One paragraph: support specialists in Salesforce look up how to say
customer names. Goal = given a name, produce its pronunciation.

## Scope / boundary
What this IS: a function `pronounce(name) -> Pronunciation`.
What this is NOT: the UI integration (explicitly out of scope).

## Contract
The interface + output schema (ipa, respelling, confidence, notes).
This is the promise the rest of the system depends on.

## Approach
LLM call (openAI). Baseline = dictionary lookup (CMUdict).
Note the ladder: baseline first, LLM must beat it to justify cost.

## Correctness policy
most-common-US

## Evaluation
Gold set in data/gold.csv (~3000 names, hard cases included).
Metrics: phoneme error rate for IPA; human accept/reject for respelling.

## Status
phase-1 scratch
