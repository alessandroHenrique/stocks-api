# polygon_data - AWS Lambda

This AWS Lambda function fetches stock data from the **Polygon.io** API for a given stock symbol and date. It is designed to handle multiple retries in case of errors like missing data or API rate limits.

## **Functionality**

The Lambda:
1. Accepts a JSON payload with a `symbol` (stock symbol) and a `start_date` (date for fetching stock data).
2. Queries the **Polygon.io** API for open, high, low, and close prices for the given date.
3. Implements retry logic to fetch data for up to 3 previous days if no data is available for the provided date.
4. Returns a structured JSON response with the stock data or an error message.


## **Input Parameters**

- `symbol` (string, required): The stock symbol (e.g., `AAPL`, `TSLA`).
- `start_date` (string, required): The date in `YYYY-MM-DD` format for fetching stock data.

**If one of the parameters are not received, the following will be the response:**
```json
{
  "statusCode": 500,
  "body": {
    "error": "Both 'symbol' and 'start_date' parameters are required."
  }
}
```

**Example Input:**
```json
{
  "symbol": "AAPL",
  "start_date": "2024-11-17"
}
```

**Example Output:**
```json
{
  "statusCode": 200,
  "body": {
    "status": "OK",
    "from": "2024-11-15",
    "symbol": "AAPL",
    "open": 226.4,
    "high": 226.92,
    "low": 224.27,
    "close": 225,
    "volume": 45374616,
    "afterHours": 225.26,
    "preMarket": 226.9
  }
}
```

**If no stock data is available for the requested date or after retries:**
```json
{
  "statusCode": 500,
  "body": {
    "error": "Stock data not found for AAPL in the last 3 days."
  }
}
```


## **Environment Variables**

The function requires the following environment variable for configuration:

- **`POLYGON_API_KEY`**: API key for accessing the Polygon.io API.

This variable must be set in the AWS Lambda environment configuration.


## **Dependencies**

The function relies on the following Python library:

1. **`requests`**: For sending HTTP requests to the MarketWatch website.
Ensure this dependency is installed when packaging the Lambda function.
