import operator
from typing import Annotated, Any, TypedDict


def merge_fields(left: dict[str, str], right: dict[str, str]) -> dict[str, str]:
    merged = dict(left)
    merged.update(right)
    return merged


class OnboardingState(TypedDict, total=False):
    thread_id: str
    messages: Annotated[list[dict[str, str]], operator.add]
    platform: str | None
    fields: Annotated[dict[str, str], merge_fields]
    missing_fields: list[str]
    invalid_fields: list[str]
    attempts: int
    ticket_result: dict[str, Any] | None
    reply: str
