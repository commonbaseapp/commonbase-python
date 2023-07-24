from typing import Any, Generator
import json
import requests
import sseclient
from commonbase.completion_response import CompletionResponse
from commonbase.exceptions import CommonbaseException


class Completion:
    @classmethod
    def _send_completion_request(
        cls,
        project_id,
        prompt,
        api_key=None,
        chat_context=None,
        user_id=None,
        truncate_variable=None,
        provider_config=None,
        stream=False,
    ) -> requests.Response:
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
            "stream": stream,
        }
        data = {k: v for k, v in data.items() if v is not None}
        return requests.post(
            "https://api.commonbase.com/completions",
            stream=stream,
            json=data,
            headers={"Accept": "text/event-stream"} if stream else None,
        )

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
    ) -> CompletionResponse:
        response = Completion._send_completion_request(
            project_id=project_id,
            prompt=prompt,
            api_key=api_key,
            chat_context=chat_context,
            user_id=user_id,
            truncate_variable=truncate_variable,
            provider_config=provider_config,
            stream=False,
        )

        json = response.json()

        if "error" in json:
            raise CommonbaseException(json)

        return CompletionResponse(response.json())

    @classmethod
    def stream(
        cls,
        project_id,
        prompt,
        api_key=None,
        chat_context=None,
        user_id=None,
        truncate_variable=None,
        provider_config=None,
    ) -> Generator[CompletionResponse, Any, None]:
        response = Completion._send_completion_request(
            project_id=project_id,
            prompt=prompt,
            api_key=api_key,
            chat_context=chat_context,
            user_id=user_id,
            truncate_variable=truncate_variable,
            provider_config=provider_config,
            stream=True,
        )
        client = sseclient.SSEClient(response)

        for event in client.events():
            yield CompletionResponse(json.loads(event.data))
