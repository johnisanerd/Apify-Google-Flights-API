[https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search](https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search?fpr=9n7kx3)

# 🚀 Google Flights Search API

> **The most efficient, reliable, and developer-friendly Google Flights search API.**

You can run this using pay [per event pricing here](https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search?fpr=9n7kx3).

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- An Apify account and API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Apify-Google-Flights-API
   ```

2. **Create a virtual environment with `uv` (recommended)**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Install dependencies with `uv`**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Configure your API key**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Apify API key
   # Get your API key from: https://apify.com?fpr=9n7kx3
   ```

5. **Run the basic example**
   ```bash
   python google-flights-api.py
   ```

6. **Run the booking-options example (`BOS -> PQI`)**
   ```bash
   python google-flights-get-booking-options.py
   ```

## Daily Low-Cost Booking Options Test

`google-flights-get-booking-options.py` demonstrates booking options using:
- `departure_id="BOS"`
- `arrival_id="PQI"`
- `fetch_booking_options=true`
- `max_pages=1`

Because this route is run only once per day, it is a low-cost way to verify
that booking-option extraction and booking links are still working end to end.

### Alternative: Direct API Key Usage
If you prefer not to use a `.env` file, you can set the environment variable directly:
```bash
export APIFY_API_TOKEN="your_api_key_here"
python google-flights-get-booking-options.py
```
[https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search](https://apify.com/johnvc/google-flights-data-scraper-flight-and-price-search?fpr=9n7kx3)

[**Made with ❤️**](https://apify.com/johnvc?fpr=9n7kx3)

*Transform your flight search automation with the most reliable and efficient Google Flights search scraper on the market.*
Last Updated: 2026.05.07
