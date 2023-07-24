import requests


class Completion:
    @classmethod
    def create(
        cls,
        project_id,
        api_key=None,
        prompt=None,
        chat_context=None,
        user_id=None,
        variables=None,
        truncate_variable=None,
        provider_config=None,
    ):
        data = {
            "projectId": project_id,
            "apiKey": api_key,
            "prompt": prompt,
            "variables": variables,
            "context": chat_context,
            "userId": user_id,
            "truncateVariable": truncate_variable,
            "providerConfig": provider_config,
        }
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.post("https://api.commonbase.com/completions", json=data)
        return response.json()
