import csv
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any

from latencylab.providers.base import ProviderResult


def get_csv_values(results: list[ProviderResult]) -> dict[str, Any]:
    csv_values = {TIME_STAMP_CSV_COLUMN_NAME: datetime.now()}

    for result in results:
        provider_name = result.provider_name
        value_names = [v for v in asdict(result).keys() if v != "provider_name"]

        for value_name in value_names:
            name = f"{provider_name} {value_name}"
            value = getattr(result, value_name)

            csv_values[name] = value

    return csv_values


def write_results_csv(results: list[ProviderResult], output_file_path: Path):
    csv_values = get_csv_values(results)

    file_exists = output_file_path.exists()

    with open(output_file_path, "a" if file_exists else "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_values.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(csv_values)


TIME_STAMP_CSV_COLUMN_NAME = "timestamp"
