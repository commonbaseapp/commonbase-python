from typing import Generator, Optional
import json
import requests
import sseclient
from commonbase.completion_response import CompletionResponse
from commonbase.exceptions import CommonbaseException
from commonbase.chat_context import ChatContext
from commonbase.provider_config import ProviderConfig


class Completion:
    @classmethod
    def _send_completion_request(
        cls,
        project_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        chat_context: Optional[ChatContext] = None,
        user_id: Optional[str] = None,
        truncate_variable: Optional[bool] = None,
        provider_config: Optional[ProviderConfig] = None,
        stream: bool = False,
    ) -> requests.Response:
        assert project_id is not None
        assert prompt is not None

        data = {
            "projectId": project_id,
            "prompt": prompt,
            "apiKey": api_key,
            "context": chat_context._to_dict() if chat_context is not None else None,
            "userId": user_id,
            "truncateVariable": truncate_variable,
            "providerConfig": provider_config._to_dict()
            if provider_config is not None
            else None,
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
        project_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        chat_context: Optional[ChatContext] = None,
        user_id: Optional[str] = None,
        truncate_variable: Optional[bool] = None,
        provider_config: Optional[ProviderConfig] = None,
    ) -> CompletionResponse:
        """Creates a completion for the given prompt.

        Parameters
        ----------
        project_id : str
            The ID of your Commonbase project.
        prompt : str
            The prompt for which a completion is generated.
        api_key : str, optional
            The API key used for authentication. Currently not necessary.
        chat_context : ChatContext, optional
            The list of chat messages in a conversation
        user_id : str, optional
            The User ID that will be logged for the invocation.
        truncate_variable : bool, optional
            A flag to toggle redaction variable truncation.

        Raises
        ------
        CommonbaseException
            If the request is malformed or there is an API error.
        """

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

        if response.status_code >= 400 or "error" in json:
            raise CommonbaseException(json)

        return CompletionResponse(response.json())

    @classmethod
    def stream(
        cls,
        project_id: str,
        prompt: str,
        api_key: Optional[str] = None,
        chat_context: Optional[ChatContext] = None,
        user_id: Optional[str] = None,
        truncate_variable: Optional[bool] = None,
        provider_config: Optional[ProviderConfig] = None,
    ) -> Generator[CompletionResponse, None, None]:
        """Creates a completion stream for the given prompt.

        Parameters
        ----------
        project_id : str
            The ID of your Commonbase project.
        prompt : str
            The prompt for which a completion is generated.
        api_key : str, optional
            The API key used for authentication. Currently not necessary.
        chat_context : ChatContext, optional
            The list of chat messages in a conversation
        user_id : str, optional
            The User ID that will be logged for the invocation.
        truncate_variable : bool, optional
            A flag to toggle redaction variable truncation.

        Raises
        ------
        CommonbaseException
            If the request is malformed or there is an API error.
        """
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

        if response.status_code >= 400:
            raise CommonbaseException(response.json())

        client = sseclient.SSEClient(response)
        for event in client.events():
            yield CompletionResponse(json.loads(event.data))
