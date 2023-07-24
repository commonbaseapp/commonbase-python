# Commonbase Python SDK

Commonbase allows developers to integrate with any popular LLM API provider without needing to change any code. The SDK helps with collecting data and feedback from the users and helps you fine-tune models for your specific use case.

## Installation

```
pip install commonbase
```

## Usage

A project ID is required for all Commonbase requests. You can find your project ID in the [Commonbase Dashboard](https://commonbase.com/test-50727/project/test/overview).

To create a completion, provide your project ID and prompt to the `Completion.create` class method.

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
