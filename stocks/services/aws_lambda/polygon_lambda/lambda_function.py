import os
from datetime import datetime, timedelta
import requests


POLYGON_API_URL = "https://api.polygon.io/v1/open-close/{symbol}/{date}"
API_KEY = os.getenv("POLYGON_API_KEY")


def lambda_handler(event, context):
    try:
        symbol = event.get("symbol")
        start_date = event.get("start_date")
        if not symbol or not start_date:
            raise ValueError("Both 'symbol' and 'start_date' parameters are required.")

        data = get_stock_data(symbol, start_date)

        return {
            "statusCode": 200,
            "body": data,
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)},
        }


def get_stock_data(symbol, start_date):
    """
    Make a request to the Polygon.io API to fetch stock data
    """
    max_retries = 3
    retry_count = 0
    current_date = start_date

    headers = {"Authorization": f"Bearer {API_KEY}"}

    while retry_count <= max_retries:
        url = POLYGON_API_URL.format(symbol=symbol, date=current_date)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            retry_count += 1
            current_date = datetime.strptime(current_date, "%Y-%m-%d") - timedelta(
                days=1
            )
            current_date = current_date.isoformat().split("T")[0]
        else:
            response.raise_for_status()

    raise ValueError(
        f"Stock data not found for {symbol} in the last {max_retries} days."
    )
