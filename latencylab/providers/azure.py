from openai.lib.azure import AzureOpenAI

from latencylab.providers.openai import BaseOpenAIProvider


class AzureGPTProvider(BaseOpenAIProvider):
    def __init__(self, azure_key, azure_endpoint, azure_deployment_name, model_name):
        self.client = AzureOpenAI(api_key=azure_key, api_version="2024-02-01", azure_endpoint=azure_endpoint)
        self.deployment_name = azure_deployment_name
        self.public_model_name = model_name

    @property
    def model_name(self):
        return self.deployment_name

    def __str__(self) -> str:
        return f"Azure_{self.public_model_name}"
