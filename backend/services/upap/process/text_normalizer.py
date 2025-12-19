import re
import unicodedata

class TextNormalizer:
    @staticmethod
    def clean(text: str) -> str:
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if not unicodedata.combining(c))
        text = text.lower().strip()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    @staticmethod
    def normalize_metadata(meta: dict) -> dict:
        return {k: TextNormalizer.clean(v) if isinstance(v, str) else v for k, v in meta.items()}
