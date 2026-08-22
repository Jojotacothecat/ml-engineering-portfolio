from pronounce import pronounce, MODEL
from hybrid import dict_lookup
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
    if pred.ipa.strip() == "[ambiguous]" or pred.confidence <= 0.2:
        ipa_cer = None
    hybrid_pred = dict_lookup(row['name']) or pred
    hybrid_ipa_cer = cer(normalize_ipa(row["ipa"]), normalize_ipa(hybrid_pred.ipa))
    if hybrid_pred.ipa.strip() == "[ambiguous]" or hybrid_pred.confidence <= 0.2:
        hybrid_ipa_cer = None
    print(f'{row["name"]} ~ {normalize_ipa(pred.ipa)} ~ {normalize_ipa(hybrid_pred.ipa)}', flush=True)
    records.append(
        {"name":       row["name"],
        "category":   row["category"],
        "gold_ipa":   row["ipa"],
        "pred_ipa":   pred.ipa,
        "ipa_cer":    ipa_cer,     
        "hybrid_pred_ipa":   hybrid_pred.ipa,
        "hybrid_ipa_cer":    hybrid_ipa_cer,    
        "confidence": pred.confidence,
        "gold_respell": row["respelling"],
        "pred_respell": pred.respelling,
        "source": hybrid_pred.notes if hybrid_pred.notes == "dict" else "llm",    
        }
    )

results = pd.DataFrame(records)
print(f"Overall IPA CER: {round(results['ipa_cer'].mean(),3)}")
print(f"Overall Hybrid IPA CER: {round(results['hybrid_ipa_cer'].mean(),3)}")

print("IPA CER by category:")
print(results.groupby('category')['ipa_cer'].mean().sort_values(ascending=False))

print("Hybrid IPA CER by category:")
print(results.groupby('category')['hybrid_ipa_cer'].mean().sort_values(ascending=False))

safe = MODEL.replace(".", "_").replace(":", "_")   # "qwen3.6:27b" -> "qwen3_6_27b"
results.to_csv(f"artifacts/hybrid_vs_{safe}_eval.csv")

