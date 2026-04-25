import re

from config import (
    ALLOWED_TOPICS,
    INTENT_WORDS,
    LIFE_LIMIT,
    NEUTRAL_MESSAGES,
    RECOVERY_REQUIRED,
)


class StressManager:
    """Tracks per-user stress, lives, and recovery in memory for the current bot session."""

    def __init__(self) -> None:
        self.sessions = {}

    def init_user(self, user_id: str) -> None:
        self.sessions[user_id] = {
            "lives": LIFE_LIMIT,
            "stress": 0,
            "recovery": 0,
            "notice_sent": False,
            "exhausted": False,
        }

    def get_user(self, user_id: str) -> dict:
        if user_id not in self.sessions:
            self.init_user(user_id)
        return self.sessions[user_id]

    def is_valid_query(self, message: str) -> bool:
        normalized = message.lower()
        matched_keywords = []
        for keyword in ALLOWED_TOPICS:
            if re.search(rf"\b{re.escape(keyword)}\b", normalized):
                matched_keywords.append(keyword)

        if not matched_keywords:
            return False

        # Intent words like "how/why/fix" should not validate by themselves.
        return any(keyword not in INTENT_WORDS for keyword in matched_keywords)

    def is_neutral_message(self, message: str) -> bool:
        normalized = message.lower().strip()
        return normalized in NEUTRAL_MESSAGES

    def handle(self, user_id: str, message: str) -> str:
        user = self.get_user(user_id)

        if self.is_neutral_message(message):
            return "neutral"

        if self.is_valid_query(message):
            if user["exhausted"]:
                user["recovery"] += 1

                if user["recovery"] >= RECOVERY_REQUIRED:
                    user["lives"] = LIFE_LIMIT
                    user["stress"] = 0
                    user["recovery"] = 0
                    user["exhausted"] = False
                    return "valid_reset"

                return "valid_recovery"

            return "valid"

        user["stress"] += 1

        if user["exhausted"]:
            return "exhausted_invalid"

        user["lives"] -= 1
        if user["lives"] <= 0:
            user["lives"] = 0
            user["exhausted"] = True
            user["recovery"] = 0
            return "life_exhausted"

        return "invalid"
