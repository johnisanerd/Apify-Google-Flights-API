"""
Google Flights API: A Quick Start Example
See more at: https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search?fpr=9n7kx3
Input schema: https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search/input-schema?fpr=9n7kx3

This script shows how to call the Google Flights API on Apify from Python and read
its structured JSON output. It exercises several input parameters so you can see
what is configurable, while keeping the run small so your first call stays cheap.

For the booking-links example (direct airline/OTA URLs), see
google-flights-get-booking-options.py.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (one page, booking-option resolution off) to keep this
# first run inexpensive. Raise these once you have your own API key and budget.
run_input = {
    "departure_id": "LAX",
    "arrival_id": "JFK",
    "outbound_date": "2026-06-17",   # YYYY-MM-DD (one-way: omit return_date)
    "adults": 1,
    "currency": "USD",
    "hl": "en",                      # language code
    "gl": "us",                      # country code
    "max_pages": 1,                  # kept at 1 to keep the run cheap
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset (one item per page)
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} page(s) of results.\n")

# Show the top recommended flights from each page.
for item in items:
    meta = item.get("search_metadata", {})
    print(f"Total flights found: {meta.get('total_flights_found')}")
    for flight in (item.get("best_flights") or [])[:5]:
        legs = flight.get("flights") or []
        if not legs:
            continue
        origin = legs[0].get("departure_airport", {}).get("id")
        dest = legs[-1].get("arrival_airport", {}).get("id")
        airline = legs[0].get("airline")
        stops = len(legs) - 1
        print(
            f"  ${flight.get('price')}  {airline}  {origin} -> {dest}  "
            f"stops={stops}  {flight.get('total_duration')} min"
        )
    print()
