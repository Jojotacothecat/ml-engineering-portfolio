# Transformer Propensity (WIP)

## Problem Statement
In this project, we develop a propensity model to predict how likely a customer is going to make a purchase in the following 7 days. Specifically, 
- Predict P(Customer Purchase within 7 days of Obs date)
- Obs date: every monday
- Production output: One score per customer every monday morning
- Label Window: 7 days after observation date
- Feature Window: the prior T=8 weekly activity snapshots. Feature window ends at the obs date; label window starts after it.
- Out of Time Split:  weeks 1-20 in-time, 28-30 OOT. 7-week gap mimicking deployment lag. OOT gets read once, at the end, never during tuning.
- In Time Split: by customer_id ` hash(customer_id) % 100 < 15`

## Methodology
We will compare two methodologies, a simple xgboost vs a sequential transformer. 

## Data
We will simulate the data ourselves. 

## Note
Currently everything lives in scratch.ipynb — tiny scale, end to end.
Refactor into src/ + notebooks/ once the skeleton runs clean.