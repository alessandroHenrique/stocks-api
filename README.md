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
  "purchased_amount": 0,
  "purchased_status": "",
  "request_data": "2024-11-20",
  "company_code": "AAPL",
  "company_name": "Apple Inc.",
  "stock_values": {
    "open_value": 228.06,
    "high": 229.93,
    "low": 225.89,
    "close": 229
  },
  "performance_data": {
    "five_days": 0.7,
    "one_month": -0.33,
    "three_months": 2.36,
    "year_to_date": 19.37,
    "one_year": 20.13
  },
  "competitors": [
    {
      "name": "Microsoft Corp.",
      "market_cap": {
        "currency": "USD",
        "value": 3090000000000
      }
    },
    {
      "name": "Alphabet Inc. Cl C",
      "market_cap": {
        "currency": "USD",
        "value": 2160000000000.0002
      }
    },
    {
      "name": "Alphabet Inc. Cl A",
      "market_cap": {
        "currency": "USD",
        "value": 2160000000000.0002
      }
    },
    {
      "name": "Amazon.com Inc.",
      "market_cap": {
        "currency": "USD",
        "value": 2130000000000
      }
    },
    {
      "name": "Meta Platforms Inc.",
      "market_cap": {
        "currency": "USD",
        "value": 1430000000000
      }
    },
    {
      "name": "Samsung Electronics Co. Ltd.",
      "market_cap": {
        "currency": "KRW",
        "value": 376850000000000
      }
    },
    {
      "name": "Samsung Electronics Co. Ltd. Pfd. Series 1",
      "market_cap": {
        "currency": "KRW",
        "value": 376850000000000
      }
    },
    {
      "name": "Sony Group Corp.",
      "market_cap": {
        "currency": "JPY",
        "value": 18310000000000
      }
    },
    {
      "name": "Dell Technologies Inc. Cl C",
      "market_cap": {
        "currency": "USD",
        "value": 97590000000
      }
    },
    {
      "name": "HP Inc.",
      "market_cap": {
        "currency": "USD",
        "value": 35350000000
      }
    }
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

## Contato
For questions or feedback, feel free to reach out:

`email`: **alessandrohenriqueho@gmail.com**
