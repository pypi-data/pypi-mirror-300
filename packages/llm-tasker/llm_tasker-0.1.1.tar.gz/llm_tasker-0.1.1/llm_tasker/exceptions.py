# ValueError(
#     "You need to provide a task prompt template, which, technically, is a class docstring."
# )

# ValueError("You need to provide an LLM client via `LLMTask.set_client` class method.")

# ValueError(
#     "You need to provide an LLM model via `LLMTask.configure` class method or `LLMTask.__call__` instance method."
# )

class MissingTaskPromptTemplateError(ValueError):
    """Exception raised when a task prompt template (class docstring) is missing."""
    def __init__(self):
        super().__init__("You need to provide a task prompt template, which, technically, is a class docstring.")
