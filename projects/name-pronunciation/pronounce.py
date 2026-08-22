from openai import OpenAI
from pydantic import BaseModel

MODEL = "qwen3.6:27b"

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

class Pronunciation(BaseModel):
    ipa: str
    respelling: str
    confidence: float
    notes: str

def pronounce(name: str) -> Pronunciation:
    completion = client.chat.completions.parse(
        model = MODEL,
        temperature=0,   
        messages=[
            {"role": "system", 
             "content": "/no_think\n give me the pronunciation of the given name, use the most-common-US version of pronunciation, I want both IPA and respelling, and it should return low confidence and a note when a name is ambiguous or has no standard pronunciation (for example, X Æ A-12)"},
            {"role": "user", "content": name},
        ],
        response_format=Pronunciation,
        extra_body={"think": False}
    )
    return completion.choices[0].message.parsed

if __name__ == "__main__":
    print(pronounce("Nguyen")) 