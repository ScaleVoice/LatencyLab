from datetime import datetime
from dataclasses import asdict

from rich.console import Console
from rich.table import Table

from latencylab.providers.base import ProviderResult

IGNORED_COLUMNS = ["chunks_time_seconds"]


def print_to_stdout(results: list[ProviderResult]):
    console = Console()

    table = Table(title=f"Results from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for column in asdict(results[0]).keys():
        if column not in IGNORED_COLUMNS:
            table.add_column(column)

    for result in results:
        table.add_row(*[str(v) for k, v in asdict(result).items() if k not in IGNORED_COLUMNS])

    console.print(table)
