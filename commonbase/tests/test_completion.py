import os
import pytest
import commonbase


def test_no_project_id():
    with pytest.raises(AssertionError):
        commonbase.Completion.create(project_id=None, prompt="xxx")


def test_no_prompt():
    with pytest.raises(AssertionError):
        commonbase.Completion.create(project_id="xxx", prompt=None)


def test_invalid_project_id():
    with pytest.raises(commonbase.CommonbaseException):
        commonbase.Completion.create(project_id="", prompt="Hello")


def test_completion_prompt():
    result = commonbase.Completion.create(
        project_id=os.getenv("CB_PROJECT_ID"), prompt="Hello"
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
        project_id=os.getenv("CB_PROJECT_ID"),
        prompt="Please return the string '123abc' to me without the quotes.",
    )

    assert result.completed and result.choices[0].text.strip() == "123abc"


def test_completion_stream():
    response_count = 0

    for response in commonbase.Completion.stream(
        project_id=os.getenv("CB_PROJECT_ID"),
        prompt="Tell me about artificial intelligence.",
    ):
        assert len(response.choices) > 0 and response.choices[0].text is not None
        response_count += 1

    assert response_count > 0
