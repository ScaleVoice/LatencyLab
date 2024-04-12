from openai.lib.azure import AzureOpenAI

from latencylab.providers.base import DEFAULT_INPUT_TEXT_CHARS
from latencylab.providers.openai import BaseOpenAIProvider


class AzureGPTProvider(BaseOpenAIProvider):
    def __init__(
        self, azure_key: str, azure_endpoint: str, azure_deployment_name: str, model_name: str, input_text_chars: int = DEFAULT_INPUT_TEXT_CHARS
    ):
        self.client = AzureOpenAI(api_key=azure_key, api_version="2024-02-01", azure_endpoint=azure_endpoint)
        self.deployment_name = azure_deployment_name
        self.public_model_name = model_name
        self.input_text_chars = input_text_chars

    @property
    def model_name(self):
        return self.deployment_name

    def __str__(self) -> str:
        return f"Azure_{self.public_model_name}"
