from app.extract import extract
from app.trust import verify_quotes

segments = [
    {"start_sec": 0.0, "end_sec": 5.0, "text": "Namaste sabko, aaj marketing campaign ka budget decide karna hai."},
    {"start_sec": 5.0, "end_sec": 12.0, "text": "ok toh final hai, budget 50k se upar nahi jayega"},
    {"start_sec": 12.0, "end_sec": 18.0, "text": "Priya, tum Friday tak revised budget sheet share kar dena"},
]

result = extract(segments)
checked, report = verify_quotes(result, segments)
print(checked.model_dump_json(indent=2))
print(report)