from app.schemas import ActionItem, Decision, Extraction
from app.trust import verify_quotes

SEGMENTS = [
    {"start_sec": 0.0, "end_sec": 5.0, "text": "Namaste sabko, shuru karte hain."},
    {"start_sec": 5.0, "end_sec": 12.0, "text": "ok toh final hai, budget 50k se upar nahi jayega"},
    {"start_sec": 12.0, "end_sec": 18.0, "text": "Priya, tum kal tak report share kar dena"},
]


def make(quote_decision, quote_task):
    return Extraction(
        summary="s",
        decisions=[Decision(text="Cap budget", quote=quote_decision, confidence=0.9)],
        action_items=[ActionItem(task="Share report", owner="Priya", quote=quote_task, confidence=0.9)],
    )


def test_real_quotes_pass_and_get_timestamps():
    result, report = verify_quotes(make("budget 50k se upar nahi jayega", "Priya, tum kal tak report share kar dena"), SEGMENTS)
    assert report["failed"] == 0
    assert result.decisions[0].at_sec == 5.0
    assert result.action_items[0].at_sec == 12.0


def test_fake_quote_is_flagged():
    result, report = verify_quotes(make("budget 50k se upar nahi jayega", "Rahul ko laptop kharidna hai kal subah"), SEGMENTS)
    assert report["failed"] == 1
    assert result.action_items[0].needs_review is True
    assert result.action_items[0].confidence <= 0.3
    assert result.decisions[0].needs_review is False