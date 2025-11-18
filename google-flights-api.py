"""
Google Flights API: A Quick Start Example
See more at: https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search

This script demonstrates how to use the Google Flights API Actor
to search Google Flights and retrieve structured flight data.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the ApifyClient with your API token
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Prepare the Actor input
run_input = {
    "departure_id": "LAX",
    "arrival_id": "JFK",
    "outbound_date": "2025-12-15",
    "adults": 1,
    "currency": "USD",
    "hl": "en",
    "gl": "us",
    "max_pages": 1,
}

for each in range(0, 10):
    # Run the Actor and wait for it to finish
    run = client.actor("johnvc/google-flights-data-scraper-flight-and-price-search").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    print("💾 Check your data here: https://console.apify.com/storage/datasets/" + run["defaultDatasetId"])
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)