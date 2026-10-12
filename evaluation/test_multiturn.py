import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.conversation.context import build_contextual_query


history = [
    {
        "role": "user",
        "content": "Can I get a refund?"
    },
    {
        "role": "assistant",
        "content": "Refunds depend on TaskFlow's refund policy."
    }
]

follow_up = "What if I cancelled yesterday?"

query = build_contextual_query(
    follow_up,
    history,
)

print(query)