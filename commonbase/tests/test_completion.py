import os
import commonbase

from ..tests import get_project_id


def test_no_project_id():
    result = commonbase.Completion.create(projectId=None)

    assert "error" in result


def test_no_prompt_or_variables():
    result = commonbase.Completion.create(projectId=os.getenv("CB_PROJECT_ID"))

    assert "error" in result


def test_completion_prompt():
    result = commonbase.Completion.create(
        projectId=os.getenv("CB_PROJECT_ID"), prompt="Hello"
    )

    assert result["completed"] == True and len(result["choices"]) > 0


def test_completion_variables():
    result = commonbase.Completion.create(
        projectId=os.getenv("CB_PROJECT_ID"),
        variables={
            "user_name": "Brandon",
            "project_name": "test",
        },
    )

    assert result["completed"] == True and len(result["choices"]) > 0
