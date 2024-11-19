# marketwatch_data - AWS Lambda

This AWS Lambda function performs web scraping on **MarketWatch** to retrieve performance data and competitor information for a given stock symbol. It leverages a proxy service for accessing the MarketWatch website.


## **Functionality**

The Lambda function:
1. Accepts a JSON payload containing:
   - `symbol`: The stock symbol (e.g., `AAPL`, `TSLA`).
2. Fetches the MarketWatch page for the given symbol.
3. Extracts:
   - Company name.
   - Performance data (e.g., five-day change, one-month change).
   - Competitors and their market capitalizations.
4. Returns a structured JSON response with the extracted data.

## **Input Parameters**

The function expects the following JSON input:
- `symbol` (string, required): The stock ticker symbol.

**If the symbol parameter is not received, the following will be the response:**
```json
{
  "statusCode": 500,
  "body": {
    "error": "'symbol' parameter is required."
  }
}
```

### **Example Input**
```json
{
  "symbol": "AAPL"
}
```

**Example Output:**
```json
{
  "statusCode": 200,
  "body": [
    "Apple Inc.",
    {
      "5_day": 2.29,
      "1_month": -2.75,
      "3_month": 1.26,
      "ytd": 19.13,
      "1_year": 20.32
    },
    [
      {
        "name": "Microsoft Corp.",
        "market_cap": "$3.09T"
      },
      {
        "name": "Alphabet Inc. Cl C",
        "market_cap": "$2.15T"
      },
      {
        "name": "Alphabet Inc. Cl A",
        "market_cap": "$2.15T"
      },
      {
        "name": "Amazon.com Inc.",
        "market_cap": "$2.12T"
      },
      {
        "name": "Meta Platforms Inc.",
        "market_cap": "$1.4T"
      },
      {
        "name": "Samsung Electronics Co. Ltd.",
        "market_cap": "₩378.64T"
      },
      {
        "name": "Samsung Electronics Co. Ltd. Pfd. Series 1",
        "market_cap": "₩378.64T"
      },
      {
        "name": "Sony Group Corp.",
        "market_cap": "¥18.1T"
      },
      {
        "name": "Dell Technologies Inc. Cl C",
        "market_cap": "$99.08B"
      },
      {
        "name": "HP Inc.",
        "market_cap": "$36.07B"
      }
    ]
  ]
}
```

**If the function fails to fetch data from MarketWatch:**
```json
{
  "statusCode": 500,
  "body": {
    "error": "Could not fetch data from MarketWatch for AAPL"
  }
}
```

## **Environment Variables**

The function requires the following environment variables for configuration:

- **`BRIGHTDATA_USER`**: BrightData username for proxy access.
- **`BRIGHTDATA_PASSWORD`**: BrightData password for proxy access.

These variables must be set in the AWS Lambda environment configuration.


## **Dependencies**

The function relies on the following Python libraries:

1. **`requests`**: For sending HTTP requests to the MarketWatch website.
2. **`beautifulsoup4`**: For parsing the HTML response and extracting the required data.

Ensure these dependencies are installed when packaging the Lambda function.


## **Proxy Configuration**

The function uses the **BrightData** proxy service to access MarketWatch.

- The proxy format:
  ```plaintext
  http://<BRIGHTDATA_USER>:<BRIGHTDATA_PASSWORD>.superproxy.io:22225
