from pronounce import pronounce, MODEL
import pandas as pd
from jiwer import cer

gold = pd.read_csv('data/gold.csv')

records = []

def normalize_ipa(s: str) -> str:
    s = s.strip().lower()
    for ch in ("/", "[", "]", ".", " ", "ˈ", "ˌ", "\u0361"):
        s = s.replace(ch, "")
    return s

for _,row in gold.iterrows():
    pred = pronounce(row['name'])
    ipa_cer = cer(normalize_ipa(row["ipa"]), normalize_ipa(pred.ipa))
    if pred.ipa == ['ambiguous'] or pred.confidence <= 0.2:
        ipa_cer = None
    records.append(
        {"name":       row["name"],
        "category":   row["category"],
        "gold_ipa":   row["ipa"],
        "pred_ipa":   pred.ipa,
        "ipa_cer":    ipa_cer,     
        "confidence": pred.confidence,
        "gold_respell": row["respelling"],
        "pred_respell": pred.respelling,    
        }
    )

results = pd.DataFrame(records)
print(f"Overall IPA CER: {round(results['ipa_cer'].mean(),3)}")

print("IPA CER by category:")
print(results.groupby('category')['ipa_cer'].mean().sort_values(ascending=False))
results.to_csv(f'artifacts/{MODEL}_eval.csv')

