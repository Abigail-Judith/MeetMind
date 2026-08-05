import json

from app.services.gemini_service import ask_ai


def extract_tasks(history: str):
    prompt = f"""
You are an AI meeting assistant.

From the following meeting conversation, extract every actionable task.

Return ONLY valid JSON.

Format:

[
    {{
        "person": "...",
        "task": "...",
        "deadline": "..."
    }}
]

If no deadline is mentioned, use:

"Not specified"

Conversation:

{history}
"""

    print("===== HISTORY =====")
    print(history)

    response = ask_ai(prompt)

    print("===== GEMINI RESPONSE =====")
    print(response)

    response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(response)