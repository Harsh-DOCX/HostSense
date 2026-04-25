def build_prompt(user_msg: str, stress: int, history: list[dict] | None = None) -> str:
    tone_map = {
        0: "Friendly, helpful, and professional.",
        1: "Slightly sarcastic and mildly annoyed, but still helpful and respectful.",
        2: "Irritated and blunt, but safe and non-abusive.",
        3: "Strict, direct, and no-nonsense. Keep responses concise.",
    }

    tone = tone_map.get(min(stress, 3), tone_map[3])
    history = history or []

    conversation_block = "No previous chat history."
    if history:
        formatted_history = []
        for item in history:
            role = item.get("role", "user").capitalize()
            content = item.get("content", "").strip()
            if content:
                formatted_history.append(f"{role}: {content}")
        if formatted_history:
            conversation_block = "\n".join(formatted_history)

    return f"""
You are a Discord chatbot that ONLY answers questions about servers, hosting, VPS, cloud, and infrastructure.

RULES:
- Stay strictly on topic.
- If a question is unrelated, refuse briefly and redirect to hosting/infrastructure topics.
- Never provide abusive, hateful, harassing, or insulting language.
- Keep responses technically accurate, concise, and practical.

TONE:
{tone}

PREVIOUS CONVERSATION (same user only):
{conversation_block}

USER QUESTION:
{user_msg}

Return one direct answer with actionable guidance.
""".strip()
