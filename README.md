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
in the [Commonbase Dashboard](https://commonbase.com/).

To create text and chat completions, use `commonbase.Completion.create`:

```py
import commonbase

project_id=

result = commonbase.Completion.create(
    project_id="<your_project_id>",
    prompt="Hello!"
)

print(result.choices[0].text)
```

To stream a completion as it is generated, use `commonbase.Completion.stream`.

For more examples, see [/examples](https://github.com/commonbaseapp/commonbase-python/tree/main/examples).
