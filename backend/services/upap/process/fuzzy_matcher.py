from rapidfuzz import fuzz, process

class FuzzyMatcher:
    @staticmethod
    def match(query: str, candidates: list, limit: int = 5) -> list:
        results = process.extract(query, candidates, scorer=fuzz.token_set_ratio, limit=limit)
        return [{"candidate": c, "score": s} for c, s, _ in results]
