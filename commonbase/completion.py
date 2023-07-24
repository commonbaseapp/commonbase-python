import requests
from commonbase.completion_response import CompletionResponse
from commonbase.exceptions import CommonbaseException


class Completion:
    @classmethod
    def create(
        cls,
        project_id,
        prompt,
        api_key=None,
        chat_context=None,
        user_id=None,
        truncate_variable=None,
        provider_config=None,
    ):
        assert project_id is not None
        assert prompt is not None

        data = {
            "projectId": project_id,
            "prompt": prompt,
            "apiKey": api_key,
            "context": chat_context,
            "userId": user_id,
            "truncateVariable": truncate_variable,
            "providerConfig": provider_config,
        }
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.post("https://api.commonbase.com/completions", json=data)

        json = response.json()

        if "error" in json:
            raise CommonbaseException(json)

        return CompletionResponse(response.json())
