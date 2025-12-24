from enum import Enum

class UPAPStage(str, Enum):
    UPLOADED = "uploaded"
    ARCHIVED = "archived"
    PROCESSED = "processed"
    PUBLISHED = "published"


UPAP_ALLOWED_TRANSITIONS = {
    UPAPStage.UPLOADED: {UPAPStage.ARCHIVED},
    UPAPStage.ARCHIVED: {UPAPStage.PROCESSED},
    UPAPStage.PROCESSED: {UPAPStage.PUBLISHED},
    UPAPStage.PUBLISHED: set(),
}


class UPAPViolation(Exception):
    pass


def assert_upap_transition(current_stage: UPAPStage, target_stage: UPAPStage):
    if target_stage not in UPAP_ALLOWED_TRANSITIONS[current_stage]:
        raise UPAPViolation(
            f"UPAP violation: cannot transition from "
            f"{current_stage.value} to {target_stage.value}"
        )
