from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProviderResult:
    success: bool
    provider_name: str
    output_characters: int = 0
    first_token_time_seconds: float = 0.0
    first_sentence_time_seconds: float = 0.0
    total_request_time_seconds: float = 0.0
    chunks_time_seconds: list[float] = field(default_factory=list)


class BaseProvider(ABC):
    @abstractmethod
    def run(self) -> ProviderResult:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def input_text(self) -> str:
        input_file = Path(__file__).parent / "input_text.txt"
        return input_file.read_text()


def text_contains_sentence_end(text: str) -> bool:
    return "." in text
