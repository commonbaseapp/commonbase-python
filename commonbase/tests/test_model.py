from commonbase.chat_context import ChatContext, ChatMessage
from dataclasses import asdict


def test_chat_context_json_format():
    context = asdict(
        ChatContext(
            messages=[
                ChatMessage(role="system", content="system message"),
                ChatMessage(role="user", content="user message"),
            ]
        )
    )

    assert "messages" in context and len(context["messages"]) == 2

    systemMessage = context["messages"][0]
    userMessage = context["messages"][1]

    assert (
        isinstance(systemMessage, dict)
        and systemMessage["role"] == "system"
        and systemMessage["content"] == "system message"
    )
    assert (
        isinstance(userMessage, dict)
        and userMessage["role"] == "user"
        and userMessage["content"] == "user message"
    )
