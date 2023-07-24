# Commonbase Python SDK

Commonbase allows developers to integrate with any popular LLM API provider without needing to change any code. The SDK helps with collecting data and feedback from the users and helps you fine-tune models for your specific use case.

## Installation

```
pip install commonbase
```

## Usage

```py
import commonbase

project_id="XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX"

result = commonbase.Completion.create(project_id=project_id, prompt="Hello!")

print(result.choices[0].text)
```
