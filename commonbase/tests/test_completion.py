import os
import pytest
import commonbase


def test_create_no_project_id():
    with pytest.raises(AssertionError):
        commonbase.Completion.create(project_id=None, prompt="")  # type: ignore


def test_stream_no_project_id():
    with pytest.raises(AssertionError):
        for _ in commonbase.Completion.stream(project_id=None, prompt=""):  # type: ignore
            pass


def test_create_no_prompt():
    with pytest.raises(AssertionError):
        commonbase.Completion.create(project_id="", prompt=None)  # type: ignore


def test_stream_no_prompt():
    with pytest.raises(AssertionError):
        for _ in commonbase.Completion.stream(project_id="", prompt=None):  # type: ignore
            pass


def test_create_invalid_project_id():
    with pytest.raises(commonbase.CommonbaseException):
        commonbase.Completion.create(project_id="", prompt="Hello")


def test_stream_invalid_project_id():
    with pytest.raises(commonbase.CommonbaseException):
        for _ in commonbase.Completion.stream(project_id="", prompt="Hello"):
            pass


def test_completion_prompt():
    result = commonbase.Completion.create(
        project_id=os.getenv("CB_PROJECT_ID") or "", prompt="Hello"
    )

    assert result.completed
    assert result.invocation_id is not None
    assert result.project_id is not None
    assert result.type == "text" or result.type == "chat"
    assert result.model is not None
    assert len(result.choices) > 0

    choice = result.choices[0]

    assert choice.text is not None
    assert choice.index >= 0
    assert choice.finish_reason is not None


def test_completion_response():
    result = commonbase.Completion.create(
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="Please return the string '123abc' to me without the quotes.",
    )

    assert result.completed and result.choices[0].text.strip() == "123abc"


def test_completion_stream():
    response_count = 0

    for response in commonbase.Completion.stream(
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="Tell me about artificial intelligence.",
    ):
        assert len(response.choices) > 0 and response.choices[0].text is not None
        response_count += 1

    assert response_count > 0


def test_completion_context():
    context = commonbase.ChatContext(
        [
            commonbase.ChatMessage(role="user", content="Where is Berlin located?"),
            commonbase.ChatMessage(role="assistant", content="In the EU."),
            commonbase.ChatMessage(role="user", content="What country?"),
        ]
    )

    result = commonbase.Completion.create(
        project_id=os.getenv("CB_PROJECT_ID") or "",
        prompt="You help people with geography.",
        chat_context=context,
        provider_config=commonbase.ProviderConfig(
            provider="cb-openai-eu", params=commonbase.OpenAIParams(type="chat")
        ),
    )

    assert result.completed and "germany" in result.choices[0].text.lower()
