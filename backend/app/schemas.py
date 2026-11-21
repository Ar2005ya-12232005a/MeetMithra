from pydantic import BaseModel, Field


class Decision(BaseModel):
    text: str
    quote: str
    confidence: float = Field(ge=0, le=1)
    at_sec: float | None = None
    needs_review: bool = False


class ActionItem(BaseModel):
    task: str
    owner: str | None = None
    due_date: str | None = None
    quote: str
    confidence: float = Field(ge=0, le=1)
    at_sec: float | None = None
    needs_review: bool = False


class Extraction(BaseModel):
    summary: str
    decisions: list[Decision]
    action_items: list[ActionItem]