# Commonbase Python SDK

Commonbase allows developers to integrate with any popular LLM API provider
without needing to change any code. The SDK helps with collecting data and
feedback from the users and helps you fine-tune models for your specific use case.

## Installation

```
pip install commonbase
```

## Usage

A project ID is required for all Commonbase requests. You can find your project ID
in the [Commonbase Dashboard](https://commonbase.com/test-50727/project/test/overview).

## Text Completion

To create a basic text completion, use the `Completion.create` class method with a `prompt` argument.

```py
import commonbase

project_id="XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX"

result = commonbase.Completion.create(project_id=project_id, prompt="Hello!")

print(result.choices[0].text)
```

Use `Completion.stream` to stream a completion response.

```py
import commonbase

project_id="XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX"

result = commonbase.Completion.stream(
    project_id=project_id,
    prompt="Write me a short essay about artificial intelligence."
)

for completion in result:
    print(completion.choices[0].text, end="")
```

### Chat

To create a chat completion, use the `context` method to provide a list of chat messages.
You must also set the OpenAI configuration to `chat`. In this mode, the `prompt` argument
functions as a system message.

```py
import commonbase

project_id="XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX"

result = commonbase.Completion.create(
    project_id=project_id,
    prompt="You are an assistant who helps users with tech problems.",
    chat_context=commonbase.ChatContext([
        commonbase.ChatMessage(role="user", content="My internet isn't working."),
        commonbase.ChatMessage(role="assistant", content="Have you tried restarting your router?"),
        commonbase.ChatMessage(role="user", content="Yes I've tried that."),
    ]),
    provider_config=commonbase.ProviderConfig(
        provider="cb-openai-eu", params=commonbase.OpenAIParams(type="chat")
    ),
)

print(result.choices[0].text)
```
