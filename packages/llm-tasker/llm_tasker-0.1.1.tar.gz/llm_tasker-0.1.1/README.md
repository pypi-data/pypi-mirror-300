# LLM Task

**LLM Tasker** is a small Python library designed to simplify working with language models and prompts. It provides a structure for defining tasks, configuring LLM clients, and managing responses in a type-safe manner. 

## Features

- Supports various LLM clients (e.g., OpenAI) with easy configuration.
- Define structured prompt-based tasks as Python classes.
- Type-safe implementation using Pydantic models.
- Asynchronous support for efficient interaction with LLM services.
- Reusable task configuration and logic.


## Installation

```bash
pip install llm_task
```

## Example Usage
```python
from openai import AsyncOpenAI
from pydantic import BaseModel
from llm_tasker.task import LLMTask, TaskConfig

LLM_API_KEY = "your-openai-api-key"
LLM_MODEL_ID = "gpt-4o
client = AsyncOpenAI(api_key=LLM_API_KEY)

class AnalysisResult(BaseModel):
    subject: str
    verb: str
    object: str

class NestedOutputTask(LLMTask):
    """
    Analyze the following sentence and return a structured nested output with the main subject, verb, and object.
    
    Sentence: `{sentence}`

    Output format:
    ```json
    {{
        "subject": "subject of the sentence",
        "verb": "main verb",
        "object": "object of the sentence"
    }}
    ```
    """
    
    sentence: str
    result: AnalysisResult | None = None
    config = TaskConfig(client=client, model=LLM_MODEL_ID)

if __name__ == "__main__":
    import asyncio

    async def main():
        task = NestedOutputTask(
            sentence="The cat chased the mouse."
        )
        await task()
        print(task.result)

    asyncio.run(main())
```

## License

This project is licensed under the MIT License.