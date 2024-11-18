import pytest
from rest_framework.test import APIClient
from unittest.mock import patch
from stocks.models import Stock, MarketCap, Competitor
from datetime import date


@pytest.mark.django_db
class TestStockAPIView:
    """Tests for StockAPIView"""

    def setup_method(self):
        """Initialize reusable objects and mocks for tests"""
        self.client = APIClient()

        # Create reusable database objects
        self.stock = Stock.objects.create(
            status="OK",
            purchased_amount=100,
            purchased_status="active",
            request_data=date.today().isoformat(),
            company_code="AAPL",
            company_name="Apple Inc.",
        )
        self.market_cap = MarketCap.objects.create(currency="USD", value=2500000000.0)
        Competitor.objects.create(
            name="Microsoft", stock=self.stock, market_cap=self.market_cap
        )

        # Mock external services
        self.mock_polygon_patcher = patch(
            "stocks.services.polygon_service.get_stock_data"
        )
        self.mock_marketwatch_patcher = patch(
            "stocks.services.marketwatch_service.get_marketwatch_data"
        )
        self.mock_polygon = self.mock_polygon_patcher.start()
        self.mock_marketwatch = self.mock_marketwatch_patcher.start()

    def teardown_method(self):
        """Stop the mocks after each test"""
        self.mock_polygon_patcher.stop()
        self.mock_marketwatch_patcher.stop()

    def test_get_stock_success(self):
        """Test GET request for an existing stock"""
        self.mock_polygon.return_value = {
            "status": "OK",
            "open": 150.0,
            "high": 155.0,
            "low": 145.0,
            "close": 152.0,
            "from": date.today().isoformat(),
        }
        self.mock_marketwatch.return_value = (
            "Apple Inc.",
            {"five_days": 1.5, "one_month": 3.2},
            [{"name": "Google Inc.", "market_cap": "$1.8T"}],
        )

        response = self.client.get(f"/api/stock/{self.stock.company_code}/")
        assert response.status_code == 200
        data = response.json()
        assert data["company_code"] == "AAPL"
        assert data["company_name"] == "Apple Inc."
        assert data["stock_values"]["open_value"] == 150.0

    def test_get_stock_not_found(self):
        """Test GET request for a stock that does not exist in the database"""
        self.mock_polygon.return_value = {
            "status": "OK",
            "open": 150.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0,
            "from": date.today().isoformat(),
        }
        self.mock_marketwatch.return_value = (
            "Tesla Inc.",
            {"five_days": -2.0, "one_month": 5.0},
            [{"name": "Ford Motor Co.", "market_cap": "$0.8T"}],
        )

        response = self.client.get("/api/stock/TSLA/")
        assert response.status_code == 200
        data = response.json()
        assert data["company_code"] == "TSLA"
        assert data["stock_values"]["open_value"] == 150.0

    def test_post_stock_add_units(self):
        """Test POST request to add purchased units to an existing stock"""
        response = self.client.post(
            f"/api/stock/{self.stock.company_code}/", {"amount": 50}, format="json"
        )
        assert response.status_code == 201
        data = response.json()
        assert (
            data["message"]
            == f"50 units of stock {self.stock.company_code} were added to your stock record."
        )

        # Verify the updated purchased amount
        self.stock.refresh_from_db()
        assert self.stock.purchased_amount == 150

    def test_post_stock_create_new(self):
        """Test POST request to create a new stock and add purchased units"""
        self.mock_polygon.return_value = {
            "status": "OK",
            "open": 100.0,
            "high": 110.0,
            "low": 90.0,
            "close": 105.0,
            "from": date.today().isoformat(),
        }
        self.mock_marketwatch.return_value = (
            "Tesla Inc.",
            {"five_days": -2.0, "one_month": 5.0},
            [{"name": "Ford Motor Co.", "market_cap": "$0.8T"}],
        )

        response = self.client.post("/api/stock/TSLA/", {"amount": 20}, format="json")
        assert response.status_code == 201
        data = response.json()
        assert (
            data["message"] == "20 units of stock TSLA were added to your stock record."
        )

        # Verify the new stock was created
        new_stock = Stock.objects.get(company_code="TSLA")
        assert new_stock.purchased_amount == 20
