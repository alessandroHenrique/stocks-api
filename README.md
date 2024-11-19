# Stocks API

An API for retrieving and managing stock data using integrations with **Polygon.io** and **MarketWatch**.
The system fetches stock performance metrics, competitors' data, and pricing details while ensuring seamless caching and scalability using Redis and AWS Lambda.

## Requirements

Ensure you have the following installed before running the project:

- Docker
- Docker Compose

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:alessandroHenrique/stocks-api.git
   ```

2. Navigate to the project directory:

    ```bash
    cd stocks-api
    ```

3. Setup Environment Configuration:
  - Locate the .env.template file in the project directory.
  - Create a copy of the file and rename it to `.env`
    ```bash
    cp .env.template .env
    ```
  - Open the `.env` file and fill in the required values. Below is a description of each variable:
    ### Database configuration:
    - `DB_HOST`: Host for the PostgreSQL database.
    - `DB_PORT`: Port for the PostgreSQL database (default: 5432).
    - `POSTGRES_DB`: Name of the PostgreSQL database.
    - `POSTGRES_USER`: Username for the PostgreSQL database.
    - `POSTGRES_PASSWORD`: Password for the PostgreSQL database.

    ### AWS configuration:
    - `AWS_ACCESS_KEY_ID`: AWS access key for Lambda integration.
    - `AWS_SECRET_ACCESS_KEY`: AWS secret key for Lambda integration.
    - `AWS_DEFAULT_REGION`: AWS region for the Lambda functions.

    ### Django configuration:
    - `SECRET_KEY`: Secret key for Django application security.
    - `DEBUG`: Debug mode for the Django application (True for development, False for production).

    ### Redis configuration:
    - `REDIS_URL`: URL for the Redis server.

  - Save the file. The application will use these variables during runtime.

4. Build and start the project using Docker Compose:

    ```bash
    docker-compose up
    ```
    or simply
    ```bash
    make start
    ```

At this point, the API will be available for interaction.

## Usage

The API is documented using Swagger and is accessible at:

- Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
- ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

You can use the interface to test the API endpoints directly in your browser.

The API has two main features:
1. Fetch stock data.
2. Update stock purchase information.

### Fetch Stock Data:
Retrieve performance data, pricing, and competitors for a specific stock.

 - Endpoint: http://localhost:8000/api/stock/{symbol}
 - Método: GET
 - Example Request Using curl:
    ```curl
    curl -X 'GET' \
      'http://localhost:8000/api/stock/AAPL/' \
      -H 'accept: application/json'
    ```
**Example Response**:
```json
{
    "status": "OK",
    "company_code": "AAPL",
    "company_name": "Apple Inc.",
    "stock_values": {
        "open_value": 150.0,
        "high": 155.0,
        "low": 145.0,
        "close": 152.0
    },
    "performance_data": {
        "five_days": 1.5,
        "one_month": 3.2,
        "three_months": 5.0,
        "year_to_date": 56.4,
        "one_year": 65.3
    },
    "competitors": [
        {"name": "Microsoft Corp.", "market_cap": "$2.4T"},
        {"name": "Google LLC", "market_cap": "$1.8T"}
    ]
}
```

### Update Stock Purchase amount information:
Add purchased units to a specific stock or create a new record if the stock doesn't exist.

 - Endpoint: http://localhost:8000/api/stock/{symbol}
 - Método: POST
 - Request Payload:
    ```json
    {
        "amount": 10
    }
    ```
 - Example Request Using curl:
    ```curl
    curl -X 'POST' \
      'http://localhost:8000/api/stock/AAPL/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{"amount": 10}'
    ```

**Example Response**:
```json
{
    "message": "10 units of stock AAPL were added to your stock record."
}
```

## Features

### Caching with redis
The API uses Redis to cache stock data for quick retrieval. If a request is made for data already cached on the same day, it returns the cached data instead of fetching new data.

### Integrations
 - Polygon.io: Fetch stock pricing details.
 - MarketWatch: Retrieve performance metrics and competitors' data.

### AWS Lambda
Key functionalities for interacting with external services (Polygon and MarketWatch) are offloaded to AWS Lambda, ensuring scalability and reducing latency.

## Tests
To run the test suite, use the following commands:

```bash
docker-compose run --rm web pytest --cov --cov-report term-missing --disable-warnings
```

or:

```bash
make test
```
This command executes unit tests and generates a coverage report.

## Environment Variables
The application requires the following environment variables to run:

### API Keys
 - `POLYGON_API_KEY`: API key for Polygon.io.

### Redis Configuration
 - `REDIS_HOST`: Host for Redis (default: redis).
 - `REDIS_PORT`: Port for Redis (default: 6379).

### AWS Configuration
 - `AWS_ACCESS_KEY_ID`: AWS access key for Lambda integration.
 - `AWS_SECRET_ACCESS_KEY`: AWS secret key for Lambda integration.
 - `AWS_DEFAULT_REGION`: AWS region for the Lambda functions.

### Proxy Configuration
 - `BRIGHTDATA_USER`: Username for BrightData proxy.
 - `BRIGHTDATA_PASSWORD`: Password for BrightData proxy.

## Contato
For questions or feedback, feel free to reach out:

`email`: **alessandrohenriqueho@gmail.com**
