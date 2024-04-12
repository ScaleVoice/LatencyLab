from pathlib import Path

import typer
from typing_extensions import Annotated

from latencylab.base import DEFAULT_SLEEP_INTERVAL_SECONDS, run_test
from latencylab.providers.azure import AzureGPTProvider
from latencylab.providers.openai import GPT35Provider, GPT4TurboProvider, GPT350125Provider, GPT4Turbo0125Provider

app = typer.Typer()


@app.command()
def all_providers(
    openai_key: str,
    azure_key: str,
    azure_endpoint: str,
    azure_deployment_gpt35: str,
    azure_deployment_gpt4_turbo: str,
    output_csv_file: Path,
    prompt_size_increment_chars: int,
    sleep_interval_seconds: Annotated[int, typer.Option()] = DEFAULT_SLEEP_INTERVAL_SECONDS,
):
    max_prompt_size = len((Path(__file__).parent / "providers" / "input_text.txt").read_text())
    for prompt_size in range(prompt_size_increment_chars, max_prompt_size, prompt_size_increment_chars):
        run_test(
            [
                GPT35Provider(openai_key=openai_key, input_text_chars=prompt_size),
                GPT350125Provider(openai_key=openai_key, input_text_chars=prompt_size),
                GPT4TurboProvider(openai_key=openai_key, input_text_chars=prompt_size),
                GPT4Turbo0125Provider(openai_key=openai_key, input_text_chars=prompt_size),
                AzureGPTProvider(azure_key, azure_endpoint, azure_deployment_gpt4_turbo, "gpt-4-1106-preview", input_text_chars=prompt_size),
                AzureGPTProvider(azure_key, azure_endpoint, azure_deployment_gpt35, "gpt-3.5-turbo-0613", input_text_chars=prompt_size),
            ],
            sleep_interval_seconds,
            sleep_interval_seconds,
            output_csv_file,
        )
