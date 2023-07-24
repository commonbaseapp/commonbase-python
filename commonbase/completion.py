import requests


class Completion:
    @classmethod
    def create(
        cls,
        projectId,
        apiKey=None,
        prompt=None,
        chatContext=None,
        userId=None,
        variables=None,
        truncateVariable=None,
        providerConfig=None,
    ):
        data = {
            "projectId": projectId,
            "apiKey": apiKey,
            "prompt": prompt,
            "variables": variables,
            "context": chatContext,
            "userId": userId,
            "truncateVariable": truncateVariable,
            "providerConfig": providerConfig,
        }
        data = {k: v for k, v in data.items() if v is not None}
        response = requests.post("https://api.commonbase.com/completions", json=data)
        return response.json()
