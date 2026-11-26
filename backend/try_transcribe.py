import sys

from app.extract import extract
from app.transcribe import transcribe
from app.trust import verify_quotes

segments = transcribe(sys.argv[1])
for s in segments:
    print(f"[{s['start_sec']:.1f}] {s['text']}")

checked, report = verify_quotes(extract(segments), segments)
print(checked.model_dump_json(indent=2))
print(report)