Write-Host "=== OCR + Archive Arama Iyilestirmesi Baslatiliyor ===" -ForegroundColor Cyan

# 1. RapidFuzz kurulumu
Write-Host "? rapidfuzz kuruluyor..."
pip install rapidfuzz -q

# 2. text_normalizer.py olusturuluyor
Write-Host "? text_normalizer.py olusturuluyor..."
@'
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
'@ | Set-Content "backend/services/upap/process/text_normalizer.py" -Encoding UTF8

# 3. fuzzy_matcher.py olusturuluyor
Write-Host "? fuzzy_matcher.py olusturuluyor..."
@'
from rapidfuzz import fuzz, process

class FuzzyMatcher:
    @staticmethod
    def match(query: str, candidates: list, limit: int = 5) -> list:
        results = process.extract(query, candidates, scorer=fuzz.token_set_ratio, limit=limit)
        return [{"candidate": c, "score": s} for c, s, _ in results]
'@ | Set-Content "backend/services/upap/process/fuzzy_matcher.py" -Encoding UTF8

# 4. archive_router search endpoint'i ekleniyor
Write-Host "? archive_router.py search endpoint ekleniyor..."
@'
from fastapi import APIRouter
from backend.services.upap.process.text_normalizer import TextNormalizer
from backend.services.upap.process.fuzzy_matcher import FuzzyMatcher

router = APIRouter()

@router.post("/search")
def search_archive(query: str):
    # Basit örnek: arsiv kayitlarini bir listeden okuyoruz (gerçek sistemde DB olacak)
    records = ["pink floyd the wall", "beatles abbey road", "nirvana nevermind", "radiohead ok computer"]
    query_clean = TextNormalizer.clean(query)
    results = FuzzyMatcher.match(query_clean, records)
    return {"query": query, "results": results}
'@ | Set-Content "backend/api/v1/archive_router.py" -Encoding UTF8

# 5. process_stage.py güncelleniyor
Write-Host "? process_stage.py güncelleniyor..."
@'
from backend.services.upap.process.text_normalizer import TextNormalizer
from backend.services.upap.process.fuzzy_matcher import FuzzyMatcher

class ProcessStage:
    name = "process"

    def validate_input(self, context: dict):
        if "ocr_text" not in context:
            raise ValueError("Missing 'ocr_text' in context")

    def run(self, context: dict) -> dict:
        ocr_text = context.get("ocr_text", "")
        normalized = TextNormalizer.clean(ocr_text)
        candidates = context.get("candidate_titles", [])
        matches = FuzzyMatcher.match(normalized, candidates)
        context["normalized_ocr_text"] = normalized
        context["matches"] = matches
        return context
'@ | Set-Content "backend/services/upap/process/process_stage.py" -Encoding UTF8

# 6. Server baslatiliyor
Write-Host "? Server baslatiliyor..."
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
