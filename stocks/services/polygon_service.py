# import logging
# from datetime import datetime, timedelta
# import requests
# from django.conf import settings


# logger = logging.getLogger("stocks")

# POLYGON_API_URL = "https://api.polygon.io/v1/open-close/{symbol}/{date}"
# API_KEY = settings.POLYGON_API_KEY


# def get_stock_data(symbol, start_date):
#     """
#     Make a request to the Polygon.io API to fetch stock data
#     """
#     max_retries = 3
#     retry_count = 0
#     current_date = start_date

#     headers = {"Authorization": f"Bearer {API_KEY}"}

#     logger.info(f"Fetching stock data for {symbol} starting from {start_date}")

#     while retry_count <= max_retries:
#         url = POLYGON_API_URL.format(symbol=symbol, date=current_date)
#         logger.debug(f"Requesting Polygon API: {url}")
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:
#             logger.info(
#                 f"Stock data retrieved successfully for {symbol} on {current_date}"
#             )
#             return response.json()
#         elif response.status_code == 404:
#             logger.warning(f"No data found for {symbol} on {current_date}. Retrying...")
#             retry_count += 1
#             current_date = datetime.strptime(current_date, "%Y-%m-%d") - timedelta(
#                 days=1
#             )
#             current_date = current_date.isoformat().split("T")[0]
#         else:
#             logger.error(f"Polygon API error ({response.status_code}): {response.text}")
#             response.raise_for_status()

#     raise ValueError(
#         f"Stock data not found for {symbol} in the last {max_retries} days."
#     )
