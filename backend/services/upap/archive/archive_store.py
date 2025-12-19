# UPAP Archive Store
# Single-process, in-memory
# No external persistence

_ARCHIVED = set()

class ArchiveStore:
    def mark_archived(self, record_id: str):
        _ARCHIVED.add(record_id)

    def is_archived(self, record_id: str) -> bool:
        return record_id in _ARCHIVED


# Functional helpers (used by publish stage)
def mark_archived(record_id: str):
    _ARCHIVED.add(record_id)

def is_archived(record_id: str) -> bool:
    return record_id in _ARCHIVED