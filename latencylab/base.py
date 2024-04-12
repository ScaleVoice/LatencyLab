import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from latencylab.output.csv import write_results_csv
from latencylab.output.stdout import print_to_stdout

from latencylab.providers.base import BaseProvider, ProviderResult

DEFAULT_SLEEP_INTERVAL_SECONDS = 5 * 60
DEFAULT_MAX_TIME_SECONDS = 24 * 60 * 60


def run_providers_in_threads(providers: list[BaseProvider], max_request_time_seconds) -> list[ProviderResult]:
    results = []

    with ThreadPoolExecutor() as executor:
        provider_futures = {executor.submit(provider.run): provider for provider in providers}

        for future, provider in provider_futures.items():
            failed_request_result = ProviderResult(success=False, provider_name=str(provider))

            try:
                result: ProviderResult = future.result(timeout=max_request_time_seconds)
                results.append(result)
            except concurrent.futures.TimeoutError:
                print(f"Provider {provider} exceeded time limit {max_request_time_seconds}s")
                results.append(failed_request_result)
            except Exception as exc:
                print(f"Provider {provider} generated an exception: {exc}")
                results.append(failed_request_result)

    return results


def run_test(
    providers: list[BaseProvider],
    sleep_interval_seconds: int,
    max_test_time_seconds: int,
    output_csv_file: Path,
):
    start_time = time.time()

    while True:
        run_start_time = time.time()
        results = run_providers_in_threads(providers, sleep_interval_seconds)

        write_results_csv(results, output_csv_file)
        print_to_stdout(results)

        run_total_time = time.time() - run_start_time

        remaining_sleep_time_seconds = sleep_interval_seconds - run_total_time

        if remaining_sleep_time_seconds > 0:
            time.sleep(remaining_sleep_time_seconds)

        seconds_since_start = time.time() - start_time
        if seconds_since_start >= max_test_time_seconds:
            return
