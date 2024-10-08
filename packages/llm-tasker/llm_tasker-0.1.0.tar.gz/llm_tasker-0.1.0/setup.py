# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['llm_task', 'llm_task.backends.redis']

package_data = \
{'': ['*']}

install_requires = \
['openai>=1.51.0,<2.0.0', 'pydantic>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'llm-tasker',
    'version': '0.1.0',
    'description': 'A lightweight Python library for creating tasks and workflows with Large Language Models (LLMs) using prompt templates.',
    'long_description': '# LLM Task\n\n**LLM Task** is a small Python library designed to simplify working with language models and prompts. It provides a structure for defining tasks, configuring LLM clients, and managing responses in a type-safe manner. \n\n## Features\n\n- Supports various LLM clients (e.g., OpenAI) with easy configuration.\n- Define structured prompt-based tasks as Python classes.\n- Type-safe implementation using Pydantic models.\n- Asynchronous support for efficient interaction with LLM services.\n- Reusable task configuration and logic.\n\n\n## Installation\n\n```bash\npip install llm_task\n```\n\n## Example Usage\n```python\nfrom openai import AsyncOpenAI\nfrom pydantic import BaseModel\nfrom llm_task.task import LLMTask, TaskConfig\n\nLLM_API_KEY = "your-openai-api-key"\nLLM_MODEL_ID = "gpt-4o\nclient = AsyncOpenAI(api_key=LLM_API_KEY)\n\nclass AnalysisResult(BaseModel):\n    subject: str\n    verb: str\n    object: str\n\nclass NestedOutputTask(LLMTask):\n    """\n    Analyze the following sentence and return a structured nested output with the main subject, verb, and object.\n    \n    Sentence: `{sentence}`\n\n    Output format:\n    ```json\n    {{\n        "subject": "subject of the sentence",\n        "verb": "main verb",\n        "object": "object of the sentence"\n    }}\n    ```\n    """\n    \n    sentence: str\n    result: AnalysisResult | None = None\n    config = TaskConfig(client=client, model=LLM_MODEL_ID)\n\nif __name__ == "__main__":\n    import asyncio\n\n    async def main():\n        task = NestedOutputTask(\n            sentence="The cat chased the mouse."\n        )\n        await task()\n        print(task.result)\n\n    asyncio.run(main())\n```\n\n## License\n\nThis project is licensed under the MIT License.',
    'author': 'Nikita Irgashev',
    'author_email': 'nik.irg@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nikirg/llm_task',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
