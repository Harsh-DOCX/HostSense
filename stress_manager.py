import re
import json
from pathlib import Path

from config import (
    ALLOWED_TOPICS,
    INTENT_WORDS,
    LIFE_LIMIT,
    NEUTRAL_MESSAGES,
    RECOVERY_REQUIRED,
)


class StressManager:
    """Tracks per-user stress and lives with JSON persistence."""

    def __init__(self, storage_path: str) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.sessions = self._load()

    def _default_session(self) -> dict:
        return {
            "lives": LIFE_LIMIT,
            "stress": 0,
            "recovery": 0,
            "notice_sent": False,
            "exhausted": False,
        }

    def _load(self) -> dict:
        if not self.storage_path.exists():
            return {}

        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

        sessions = {}
        for user_id, user_data in data.items():
            session = self._default_session()
            if isinstance(user_data, dict):
                for key in session:
                    if key in user_data:
                        session[key] = user_data[key]
            sessions[user_id] = session
        return sessions

    def _save(self) -> None:
        temp_file = self.storage_path.with_suffix(".tmp")
        temp_file.write_text(
            json.dumps(self.sessions, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )
        temp_file.replace(self.storage_path)

    def init_user(self, user_id: str) -> None:
        self.sessions[user_id] = self._default_session()
        self._save()

    def get_user(self, user_id: str) -> dict:
        if user_id not in self.sessions:
            self.init_user(user_id)
        return self.sessions[user_id]

    def set_flag(self, user_id: str, key: str, value: bool) -> None:
        user = self.get_user(user_id)
        user[key] = value
        self._save()

    def reset_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        user["lives"] = LIFE_LIMIT
        user["stress"] = 0
        user["recovery"] = 0
        user["exhausted"] = False
        self._save()

    def delete_user(self, user_id: str) -> None:
        if user_id in self.sessions:
            del self.sessions[user_id]
            self._save()

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
                    self._save()
                    return "valid_reset"

                self._save()
                return "valid_recovery"

            self._save()
            return "valid"

        user["stress"] += 1

        if user["exhausted"]:
            self._save()
            return "exhausted_invalid"

        user["lives"] -= 1
        if user["lives"] <= 0:
            user["lives"] = 0
            user["exhausted"] = True
            user["recovery"] = 0
            self._save()
            return "life_exhausted"

        self._save()
        return "invalid"
