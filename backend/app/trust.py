from rapidfuzz import fuzz

from .schemas import Extraction


def _norm(text: str) -> str:
    return " ".join(text.lower().split())


def find_quote(quote: str, segments: list[dict], max_window: int = 3):
    """Best fuzzy match of the quote over 1..max_window consecutive segments."""
    q = _norm(quote)
    best_score, best_start = 0.0, None
    for w in range(1, max_window + 1):  # smaller windows first, so ties pick the tightest
        for i in range(len(segments)):
            chunk = segments[i : i + w]
            score = fuzz.partial_ratio(q, _norm(" ".join(s["text"] for s in chunk)))
            if score > best_score:
                best_score, best_start = score, chunk[0]["start_sec"]
    return best_score, best_start


def verify_quotes(extraction: Extraction, segments: list[dict], threshold: float = 85.0):
    """Return (checked extraction, report). Unsupported quotes get needs_review and low confidence."""
    checked = extraction.model_copy(deep=True)
    total = failed = 0
    for item in [*checked.decisions, *checked.action_items]:
        total += 1
        score, start = find_quote(item.quote, segments)
        if score >= threshold:
            item.at_sec = start
        else:
            failed += 1
            item.needs_review = True
            item.confidence = min(item.confidence, 0.3)
    report = {"total": total, "failed": failed, "fail_rate": failed / total if total else 0.0}
    return checked, report