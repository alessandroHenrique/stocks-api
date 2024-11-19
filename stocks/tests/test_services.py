import pytest
from unittest.mock import patch, MagicMock
from stocks.services.aws_lambda.polygon_lambda.lambda_function import get_stock_data
from stocks.services.aws_lambda.marketwatch_lambda.lambda_function import (
    get_marketwatch_data,
)
from datetime import date


@pytest.mark.django_db
class TestServices:
    """Tests for external services"""

    @patch("stocks.services.aws_lambda.polygon_lambda.lambda_function.requests.get")
    def test_get_stock_data_success(self, mock_requests):
        """Test get_stock_data returns correct data on success"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "OK",
            "open": 150.0,
            "high": 155.0,
            "low": 145.0,
            "close": 152.0,
            "from": date.today().isoformat(),
        }
        mock_requests.return_value = mock_response

        stock_data = get_stock_data("AAPL", date.today().isoformat())
        assert stock_data["status"] == "OK"
        assert stock_data["open"] == 150.0
        assert stock_data["high"] == 155.0

    @patch("stocks.services.aws_lambda.polygon_lambda.lambda_function.requests.get")
    def test_get_stock_data_404_retry(self, mock_requests):
        """Test get_stock_data retries on 404 error"""
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404

        mock_response_success = MagicMock()
        mock_response_success.status_code = 200
        mock_response_success.json.return_value = {
            "status": "OK",
            "open": 140.0,
            "high": 145.0,
            "low": 135.0,
            "close": 142.0,
            "from": (date.today().replace(day=date.today().day - 1)).isoformat(),
        }

        # Simulate 404 for the first request, success for the second
        mock_requests.side_effect = [mock_response_404, mock_response_success]

        stock_data = get_stock_data("AAPL", date.today().isoformat())
        assert stock_data["status"] == "OK"
        assert stock_data["open"] == 140.0
        assert (
            stock_data["from"]
            == (date.today().replace(day=date.today().day - 1)).isoformat()
        )

    @patch("stocks.services.aws_lambda.polygon_lambda.lambda_function.requests.get")
    def test_get_stock_data_fail_after_retries(self, mock_requests):
        """Test get_stock_data raises an error after max retries"""
        mock_response_404 = MagicMock()
        mock_response_404.status_code = 404
        mock_requests.side_effect = [mock_response_404] * 4

        with pytest.raises(
            ValueError, match="Stock data not found for AAPL in the last 3 days."
        ):
            get_stock_data("AAPL", date.today().isoformat())

    @patch("stocks.services.aws_lambda.marketwatch_lambda.lambda_function.requests.get")
    def test_get_marketwatch_data_success(self, mock_requests):
        """Test get_marketwatch_data parses HTML and returns correct data"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Mocked MarketWatch</title></head>
            <body>
                <h1 class="company__name">Tesla Inc.</h1>
                <div class="element element--table performance">
                    <tr>
                        <td>5 Day</td>
                        <td>-2.68%</td>
                    </tr>
                    <tr>
                        <td>1 Month</td>
                        <td>7.21%</td>
                    </tr>
                </div>
                <div class="Competitors">
                    <tr>
                        <th>Name</th>
                        <th>Chg %</th>
                        <th>Market Cap</th>
                    </tr>
                    <tr>
                        <td>Ford Motor Co.</td>
                        <td>$0.8T</td>
                    </tr>
                </div>
            </body>
        </html>
        """
        mock_requests.return_value = mock_response

        name, performance, competitors = get_marketwatch_data("TSLA")
        assert name == "Tesla Inc."
        assert performance["5_day"] == -2.68
        assert performance["1_month"] == 7.21
        assert len(competitors) == 1
        assert competitors[0]["name"] == "Ford Motor Co."
        assert competitors[0]["market_cap"] == "$0.8T"

    @patch("stocks.services.aws_lambda.marketwatch_lambda.lambda_function.requests.get")
    def test_get_marketwatch_data_404(self, mock_requests):
        """Test get_marketwatch_data handles 404 error"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests.return_value = mock_response

        with pytest.raises(
            ValueError, match="Could not fetch data from MarketWatch for TSLA"
        ):
            get_marketwatch_data("TSLA")
