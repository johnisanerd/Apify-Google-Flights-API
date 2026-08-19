# ✈️ Google Flights API: Flight and Price Search in Clean JSON

> The most efficient, reliable, and developer-friendly way to use the Google Flights API.

**Actor page:** [apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search](https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search/input-schema](https://apify.com/johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search/input-schema?fpr=9n7kx3)

The Google Flights API searches flights and returns clean, structured JSON. Each page of results comes back with the top recommended flights and alternatives, full flight legs and timings, prices, price insights (level and historical range), airport details, and search metadata. It supports one-way, round-trip, and multi-city itineraries, single or multiple airports, filters for price, stops, airlines, and passenger counts, and can optionally resolve direct airline and OTA booking links. Localized across 29+ languages and 39+ countries.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Google-Flights-API.git
   cd Apify-Google-Flights-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python google-flights-api.py
   ```

This repo also includes **`google-flights-get-booking-options.py`**, a low-cost one-way example (BOS to PQI) that enables `fetch_booking_options` to resolve direct airline and OTA booking links:
```bash
uv run python google-flights-get-booking-options.py
```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python google-flights-api.py
```

## Why Use This Google Flights API?

**Complete itineraries.** Search one-way, round-trip, and multi-city trips, with single or multiple departure and arrival airports, and get the top recommended flights plus alternatives with full leg-by-leg detail.

**Direct booking links.** Enable `fetch_booking_options` and each flight resolves to a live booking URL on the airline or OTA site, with fare families and baggage fees, ready to embed in your app.

**Powerful filters.** Constrain by max price, max stops, preferred airlines, passenger counts, and exclude basic economy.

**Price intelligence.** Every search returns price insights: the current level (low, typical, high) and a historical price range for the route.

**Predictable, pay-per-use pricing.** Billing is per page processed, plus per resolved booking link only when you ask for them. No subscription. You control cost with the page limit.

**Easy to automate.** Call it from Python in a few lines, or load it as an MCP tool so assistants like Claude and Cursor can search flights for you on demand.

## Features

### Core Capabilities
- **One-way, round-trip, and multi-city** itineraries
- **Single or multiple airports** per leg (e.g. `CDG,ORY`)
- **Filters** for price, stops, airlines, passengers, and basic economy
- **Optional direct booking links** (airline/OTA URLs, fare families, baggage fees)
- **Localization** across 29+ languages and 39+ countries

### Data Quality
- **Best and alternative flights** with full leg timings, airline, and duration
- **Price insights** with level and historical range
- **Airport details** for departure and arrival
- **Per-page metadata** and search parameters echoed back
- **Consistent JSON** shape across every query

## Usage Examples

### Basic one-way search
```json
{
  "departure_id": "LAX",
  "arrival_id": "JFK",
  "outbound_date": "2026-06-17",
  "adults": 1,
  "currency": "USD",
  "max_pages": 1
}
```

### Round trip with filters
```json
{
  "departure_id": "JFK",
  "arrival_id": "LHR",
  "outbound_date": "2026-11-25",
  "return_date": "2026-12-02",
  "adults": 2,
  "max_price": 1500,
  "max_stops": 1,
  "max_pages": 2
}
```

### Multi-city trip
```json
{
  "multi_city_json": "[{\"departure_id\":\"CDG\",\"arrival_id\":\"NRT\",\"date\":\"2026-11-17\"},{\"departure_id\":\"NRT\",\"arrival_id\":\"LAX\",\"date\":\"2026-11-24\"}]",
  "adults": 1,
  "currency": "USD",
  "max_pages": 1
}
```

### Direct booking links
```json
{
  "departure_id": "LAX",
  "arrival_id": "JFK",
  "outbound_date": "2026-06-17",
  "adults": 1,
  "fetch_booking_options": true,
  "max_pages": 1
}
```
Note: `fetch_booking_options` works for one-way searches, is billed per resolved link, and needs Actor memory of 512 MB or more (it uses a headless browser).

## Input Parameters

Either `departure_id` + `arrival_id` + `outbound_date`, or `multi_city_json`, is required.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `departure_id` | `string` | Yes* | - | Departure airport code(s), comma-separated for multiple (e.g. `LAX`, `CDG,ORY`). |
| `arrival_id` | `string` | Yes* | - | Arrival airport code(s), comma-separated for multiple. |
| `outbound_date` | `string` | Yes* | - | Departure date, `YYYY-MM-DD`. |
| `return_date` | `string` | No | (none) | Return date for round trips, `YYYY-MM-DD`. |
| `multi_city_json` | `string` | Yes* | - | JSON string of legs for multi-city trips. Replaces the three fields above. |
| `adults` | `integer` | No | `1` | Adult passengers (minimum 1). |
| `children` | `integer` | No | `0` | Child passengers. |
| `infants` | `integer` | No | `0` | Infant passengers. |
| `currency` | `string` | No | `USD` | Currency code, e.g. `USD`, `EUR`, `GBP`. |
| `hl` | `string` | No | `en` | Language code (29+ supported). |
| `gl` | `string` | No | `us` | Country code (39+ supported). |
| `max_price` | `integer` | No | (none) | Maximum price filter in the chosen currency. |
| `max_stops` | `integer` | No | (none) | Maximum stops (`0` = direct only). |
| `airlines` | `string` | No | (none) | Comma-separated preferred airline codes, e.g. `UA,AA,DL`. |
| `exclude_basic` | `boolean` | No | `false` | Exclude basic-economy fares. |
| `fetch_booking_options` | `boolean` | No | `false` | Resolve direct booking links (one-way only; billed per link; needs 512 MB+). |
| `max_pages` | `integer` | No | `1` | Maximum pages to fetch (`0` = no limit). |
| `output_file` | `string` | No | (none) | Optional filename to save results. |

## Output Format

A real result for `LAX` to `JFK` (one item per page; `best_flights` legs and the `price_insights` history are trimmed here for readability).

```json
{
  "search_parameters": {
    "trip_type_description": "One-way",
    "departure_id": "LAX",
    "arrival_id": "JFK",
    "outbound_date": "2026-06-17",
    "adults": 1,
    "currency": "USD",
    "language": "en",
    "country": "us"
  },
  "search_metadata": {
    "total_flights_found": 29,
    "best_flights_count": 3,
    "other_flights_count": 26,
    "pages_processed": 1,
    "pagination_limit_reached": true,
    "booking_options_count": 0
  },
  "page_number": 1,
  "best_flights": [
    {
      "price": 207,
      "type": "One way",
      "total_duration": 590,
      "flights": [
        {
          "departure_airport": { "name": "Los Angeles International Airport", "id": "LAX", "time": "2026-06-17 09:24" },
          "arrival_airport": { "name": "Charlotte Douglas International Airport", "id": "CLT", "time": "2026-06-17 17:28" },
          "airline": "American",
          "flight_number": "AA 2570",
          "travel_class": "Economy",
          "duration": 304
        },
        {
          "departure_airport": { "name": "Charlotte Douglas International Airport", "id": "CLT", "time": "2026-06-17 20:11" },
          "arrival_airport": { "name": "John F. Kennedy International Airport", "id": "JFK", "time": "2026-06-17 22:14" },
          "airline": "American",
          "flight_number": "AA 1727",
          "travel_class": "Economy",
          "duration": 123
        }
      ]
    }
  ],
  "other_flights": [],
  "price_insights": {
    "lowest_price": 207,
    "price_level": "typical",
    "typical_price_range": [145, 255]
  },
  "airports": [
    {
      "departure": [
        { "airport": { "id": "LAX", "name": "Los Angeles International Airport" }, "city": "Los Angeles", "country": "United States" }
      ],
      "arrival": [
        { "airport": { "id": "JFK", "name": "John F. Kennedy International Airport" }, "city": "New York", "country": "United States" }
      ]
    }
  ],
  "booking_options": []
}
```

When `fetch_booking_options` is `true`, each `booking_options` entry includes a resolved `booking_url` to the airline or OTA, plus fare family and baggage details.

---

## Use as an MCP tool

You can load the Google Flights API as an MCP tool so assistants call it for you. The MCP server URL preloads just this one Actor:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search
```

Authenticate with OAuth in the browser when offered, or with your Apify API token (the same `APIFY_API_TOKEN` used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Google Flights API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Google Flights API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Google Flights API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search`, using OAuth when prompted.
5. Ask Claude to run the Google Flights API.

Open Claude on the web: https://claude.ai/referral/uIlpa7nPLg

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Google Flights API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/Google-Flights-Data-Scraper-Flight-and-Price-Search`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Google Flights API to power travel apps, fare tracking, and analytics with reliable, structured results.*

Last Updated: 2026.08.19
