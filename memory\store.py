from typing import Any, Optional
from datetime import datetime
import json


class ConversationMemory:
    """Simple in-memory store for agent conversation history."""

    def __init__(self, max_messages: int = 50):
        self.messages: list[dict] = []
        self.max_messages = max_messages
        self.metadata: dict = {"created_at": datetime.utcnow().isoformat()}

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content, "ts": datetime.utcnow().isoformat()})
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def get_history(self) -> list[dict]:
        return self.messages

    def clear(self) -> None:
        self.messages = []

    def to_json(self) -> str:
        return json.dumps({"metadata": self.metadata, "messages": self.messages}, indent=2)
