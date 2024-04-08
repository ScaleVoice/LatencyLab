from abc import ABC, abstractmethod
from time import time

from openai import OpenAI

from latencylab.providers.base import BaseProvider, ProviderResult, text_contains_sentence_end


class BaseOpenAIProvider(BaseProvider, ABC):
    system_message = "Summarize following text"
    temperature = 0.0

    @property
    @abstractmethod
    def model_name(self):
        pass

    def run(self) -> ProviderResult:
        request_start_time = time()

        first_token_time_seconds = None
        first_sentence_time_seconds = None
        last_chunk_time = None

        complete_response = []
        chunks_times_seconds = []

        stream = self.client.chat.completions.create(
            model=self.model_name,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": self.input_text},
            ],
            stream=True,
        )

        for chunk in stream:
            try:
                chunk_content = chunk.choices[0].delta.content or ""
            except IndexError:
                chunk_content = ""

            complete_response.append(chunk_content)

            if last_chunk_time is not None:
                chunk_time_seconds = time() - last_chunk_time
                chunks_times_seconds.append(chunk_time_seconds)

            if chunk_content and first_token_time_seconds is None:
                first_token_time_seconds = time() - request_start_time

            if text_contains_sentence_end(chunk_content) and first_sentence_time_seconds is None:
                first_sentence_time_seconds = time() - request_start_time

            last_chunk_time = time()

        output_content = "".join(complete_response)

        request_total_time = time() - request_start_time

        return ProviderResult(
            success=True,
            provider_name=str(self),
            output_characters=len(output_content),
            first_token_time_seconds=first_token_time_seconds,
            first_sentence_time_seconds=first_sentence_time_seconds,
            total_request_time_seconds=request_total_time,
            chunks_time_seconds=chunks_times_seconds,
        )


class GPT35Provider(BaseOpenAIProvider):
    model_name = "gpt-3.5-turbo-0613"

    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def __str__(self) -> str:
        return f"OpenAI_{self.model_name}"


class GPT350125Provider(BaseOpenAIProvider):
    model_name = "gpt-3.5-turbo-0125"

    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def __str__(self) -> str:
        return f"OpenAI_{self.model_name}"


class GPT4TurboProvider(BaseOpenAIProvider):
    model_name = "gpt-4-1106-preview"

    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def __str__(self) -> str:
        return f"OpenAI_{self.model_name}"


class GPT4Turbo0125Provider(BaseOpenAIProvider):
    model_name = "gpt-4-0125-preview"

    def __init__(self, openai_key):
        self.client = OpenAI(api_key=openai_key)

    def __str__(self) -> str:
        return f"OpenAI_{self.model_name}"
