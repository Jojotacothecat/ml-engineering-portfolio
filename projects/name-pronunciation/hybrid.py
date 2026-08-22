import pronouncing
from pronounce import pronounce as llm_pronounce, Pronunciation

ARPA_TO_IPA = {
    # vowels
    "AA":"ɑ", "AE":"æ", "AH":"ʌ", "AO":"ɔ", "AW":"aʊ", "AY":"aɪ",
    "EH":"ɛ", "ER":"ɝ", "EY":"eɪ", "IH":"ɪ", "IY":"i", "OW":"oʊ",
    "OY":"ɔɪ", "UH":"ʊ", "UW":"u",
    # consonants
    "B":"b", "CH":"tʃ", "D":"d", "DH":"ð", "F":"f", "G":"ɡ", "HH":"h",
    "JH":"dʒ", "K":"k", "L":"l", "M":"m", "N":"n", "NG":"ŋ", "P":"p",
    "R":"r", "S":"s", "SH":"ʃ", "T":"t", "TH":"θ", "V":"v", "W":"w",
    "Y":"j", "Z":"z", "ZH":"ʒ",
}


def to_ipa(p):
    return "ə" if p == "AH0" else ARPA_TO_IPA[p.rstrip("012")]

def dict_lookup(name: str) -> Pronunciation | None:
    phones = pronouncing.phones_for_word(name.lower())
    if not phones:
        return None
    arpa = phones[0].split()

    ipa = "".join(to_ipa(p) for p in arpa)
    return Pronunciation(ipa=f"/{ipa}/", respelling="", confidence=1.0, notes="dict")