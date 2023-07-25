from typing import Literal, Sequence
from dataclasses import dataclass, asdict


@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class ChatContext:
    messages: Sequence[ChatMessage]

    def _to_dict(self) -> dict:
        return asdict(self)
