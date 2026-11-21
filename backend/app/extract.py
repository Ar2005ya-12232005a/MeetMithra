from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate

from .llm import get_llm
from .schemas import Extraction

PROMPTS = Path(__file__).parent / "prompts"


def format_transcript(segments: list[dict]) -> str:
    return "\n".join(f"[{s['start_sec']:.1f}] {s['text']}" for s in segments)


def build_extractor(version: str = "v1", model: str | None = None):
    rules = (PROMPTS / f"extraction_{version}.txt").read_text(encoding="utf-8")
    prompt = ChatPromptTemplate.from_messages([("system", rules), ("human", "{transcript}")])
    return prompt | get_llm(model).with_structured_output(Extraction)


def extract(segments: list[dict], version: str = "v1", model: str | None = None) -> Extraction:
    return build_extractor(version, model).invoke({"transcript": format_transcript(segments)})