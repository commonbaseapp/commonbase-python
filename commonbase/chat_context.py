from typing import Literal, NotRequired, TypedDict, Optional


class FunctionCallMessage(TypedDict):
    name: str
    arguments: Optional[str]


class RegularChatMessage(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str | None
    function_call: NotRequired[FunctionCallMessage]


class FunctionChatMessage(TypedDict):
    role: Literal["function"]
    name: str
    content: str


class FunctionCallConfigName(TypedDict):
    name: str


class ChatFunction(TypedDict):
    name: str
    description: str
    parameters: object


ChatMessage = RegularChatMessage | FunctionChatMessage
FunctionCallConfig = Literal["none", "auto"] | FunctionCallConfigName
