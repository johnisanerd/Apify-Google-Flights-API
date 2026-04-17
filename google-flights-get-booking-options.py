"""Run a simple, low-cost BOS->PQI booking options test.

Docs:
- https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search
- https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search/input-schema

This script runs a one-way search with ``fetch_booking_options=true``,
pretty-prints results, and saves them to a local JSON file.
"""

from __future__ import annotations

import json
import os
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict

from apify_client import ApifyClient
from dotenv import load_dotenv

ACTOR_ID = "johnvc/google-flights-data-scraper-flight-and-price-search"


class ActorRun(TypedDict):
    """Subset of Actor run fields used by this example."""

    defaultDatasetId: str


class RunInput(TypedDict):
    """Input schema fields used in this booking options demo."""

    departure_id: str
    arrival_id: str
    outbound_date: str
    adults: int
    currency: str
    hl: str
    gl: str
    max_pages: int
    fetch_booking_options: bool


def build_run_input(outbound_date: str) -> RunInput:
    """Create a one-way BOS->PQI query for booking-options validation.

    Args:
        outbound_date: Flight departure date formatted as YYYY-MM-DD.

    Returns:
        A strongly typed Actor input payload.
    """
    return RunInput(
        departure_id="BOS",
        arrival_id="PQI",
        outbound_date=outbound_date,
        adults=1,
        currency="USD",
        hl="en",
        gl="us",
        max_pages=1,
        fetch_booking_options=True,
    )


def get_client() -> ApifyClient:
    """Build an Apify client from the ``APIFY_API_TOKEN`` environment variable.

    Raises:
        RuntimeError: If the API token is missing.
    """
    load_dotenv()
    token = os.getenv("APIFY_API_TOKEN")
    if not token:
        raise RuntimeError("Missing APIFY_API_TOKEN. Add it to .env or export it.")
    return ApifyClient(token)


def fetch_items(client: ApifyClient, dataset_id: str) -> list[dict]:
    """Fetch all items from a dataset.

    Args:
        client: Initialized Apify API client.
        dataset_id: Dataset ID from the completed Actor run.

    Returns:
        Dataset items as a list of dictionaries.
    """
    return list(client.dataset(dataset_id).iterate_items())


def count_booking_options(items: list[dict]) -> int:
    """Count total booking options across all dataset items.

    Args:
        items: Dataset items returned by the Actor run.

    Returns:
        Total number of booking options.
    """
    total = 0
    for item in items:
        booking_options = item.get("booking_options", [])
        if isinstance(booking_options, list):
            total += len(booking_options)
    return total


def extract_booking_urls(items: list[dict]) -> list[str]:
    """Extract and deduplicate booking URLs from dataset items.

    Args:
        items: Dataset items returned by the Actor run.

    Returns:
        A sorted list of unique booking URLs.
    """
    urls: set[str] = set()

    for item in items:
        booking_options = item.get("booking_options", [])
        if not isinstance(booking_options, list):
            continue

        for booking_entry in booking_options:
            if not isinstance(booking_entry, dict):
                continue

            nested_options = booking_entry.get("booking_options", [])
            if not isinstance(nested_options, list):
                continue

            for option_group in nested_options:
                if not isinstance(option_group, dict):
                    continue

                together = option_group.get("together", {})
                if not isinstance(together, dict):
                    continue

                booking_url = together.get("booking_url")
                if isinstance(booking_url, str) and booking_url:
                    urls.add(booking_url)

    return sorted(urls)


def save_items_locally(items: list[dict], outbound_date: str) -> Path:
    """Save results to a local, pretty-printed JSON file.

    Args:
        items: Dataset items returned by the Actor run.
        outbound_date: Outbound date used for the search.

    Returns:
        Path to the saved JSON file.
    """
    output_path = Path(f"booking-options-bos-pqi-{outbound_date}.json")
    output_path.write_text(json.dumps(items, indent=2), encoding="utf-8")
    return output_path

def main() -> None:
    """Execute a one-way search and fetch booking options.

    The date is set to 30 days from today so the script can be run any day
    without manually editing the date value.
    """
    outbound_date = (date.today() + timedelta(days=30)).isoformat()
    run_input = build_run_input(outbound_date=outbound_date)
    client = get_client()
    run: ActorRun = client.actor(ACTOR_ID).call(run_input=run_input)

    dataset_id = run["defaultDatasetId"]
    print(f"Dataset URL: https://console.apify.com/storage/datasets/{dataset_id}")

    items = fetch_items(client=client, dataset_id=dataset_id)
    booking_options_count = count_booking_options(items)

    print(f"Pages returned: {len(items)}")
    print(f"Booking options returned: {booking_options_count}")
    print("Running this once per day keeps this test low cost.")

    output_path = save_items_locally(items=items, outbound_date=outbound_date)
    print(f"Saved local file: {output_path.resolve()}")

    booking_urls = extract_booking_urls(items)
    print("\nBooking URLs:")
    if booking_urls:
        for index, url in enumerate(booking_urls, start=1):
            print(f"{index}. {url}")
    else:
        print("No booking URLs found.")


if __name__ == "__main__":
    main()