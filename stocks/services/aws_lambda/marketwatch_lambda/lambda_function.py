import os
import requests
from bs4 import BeautifulSoup


BRIGHTDATA_USER = os.getenv("BRIGHTDATA_USER")
BRIGHTDATA_PASSWORD = os.getenv("BRIGHTDATA_PASSWORD")

PROXIES = {
    "http": f"http://{BRIGHTDATA_USER}:{BRIGHTDATA_PASSWORD}.superproxy.io:22225",
    "https": f"https://{BRIGHTDATA_USER}:{BRIGHTDATA_PASSWORD}.superproxy.io:22225",
}

MARKETWATCH_BASE_URL = "https://www.marketwatch.com/investing/stock/{symbol}"


def lambda_handler(event, context):
    try:
        symbol = event.get("symbol")
        if not symbol:
            raise ValueError("'symbol' parameter is required.")

        data = get_marketwatch_data(symbol)

        return {
            "statusCode": 200,
            "body": data,
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"error": str(e)},
        }


def get_marketwatch_data(symbol):
    """
    Scrapes performance and competitors data from the Marketwatch page.
    """
    url = MARKETWATCH_BASE_URL.format(symbol=symbol.lower())
    response = requests.get(url, proxies=PROXIES, verify=False)

    if response.status_code != 200:
        raise ValueError(f"Could not fetch data from MarketWatch for {symbol}")

    soup = BeautifulSoup(response.text, "html.parser")
    company_name = soup.find("h1", {"class": "company__name"})
    if company_name:
        company_name = company_name.get_text(strip=True)

    performance_data = {}
    performance_table = soup.find(
        "div", {"class": "element element--table performance"}
    )
    if performance_table:
        rows = performance_table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text(strip=True).lower().replace(" ", "_")
                value = cells[1].get_text(strip=True).replace("%", "")
                performance_data[key] = float(value) if value else 0.0

    competitors = []
    competitors_section = soup.find("div", {"class": "Competitors"})

    if competitors_section:
        rows = competitors_section.find_all("tr")[1:]
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                competitor_name = cells[0].get_text(strip=True)
                market_cap = cells[-1].get_text(strip=True)
                competitors.append({"name": competitor_name, "market_cap": market_cap})

    return company_name, performance_data, competitors
