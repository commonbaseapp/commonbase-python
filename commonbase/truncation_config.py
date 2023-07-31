from typing import Literal, Optional
from dataclasses import dataclass


@dataclass
class TruncationConfig:
    strategy: Literal["truncate_head", "truncate_tail", "off"]
    granularity: Optional[Literal["word", "line"]] = None
    max_prompt_tokens: Optional[int] = None
    name: Optional[str] = None

    def _as_json(self) -> dict:
        json = {
            "strategy": self.strategy,
            "granularity": self.granularity,
            "maxPromptTokens": self.max_prompt_tokens,
            "name": self.name,
        }
        return {k: v for (k, v) in json.items() if v is not None}
