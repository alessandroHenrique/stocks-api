import pytest
from stocks.serializers import (
    StockSerializer,
    StockValuesSerializer,
    StockPerformanceSerializer,
    CompetitorSerializer,
    MarketCapSerializer,
)
from stocks.models import Stock, StockValues, StockPerformance, Competitor, MarketCap
from datetime import date


@pytest.mark.django_db
class TestSerializers:
    """Tests for serializers"""

    def setup_method(self):
        """Initialize reusable objects for tests"""
        self.stock = Stock.objects.create(
            status="OK",
            purchased_amount=100,
            purchased_status="active",
            request_data=date.today().isoformat(),
            company_code="AAPL",
            company_name="Apple Inc.",
        )
        self.market_cap = MarketCap.objects.create(currency="USD", value=2500000000.0)

    def test_stock_serializer_validation_and_save(self):
        """Test StockSerializer for data validation and saving"""
        data = {
            "status": "OK",
            "purchased_amount": 50,
            "request_data": date.today().isoformat(),
            "company_code": "MSFT",
            "company_name": "Microsoft Corp.",
        }
        serializer = StockSerializer(data=data)
        assert serializer.is_valid()
        stock = serializer.save()
        assert stock.company_code == "MSFT"
        assert stock.company_name == "Microsoft Corp."

    def test_stock_values_serializer_validation_and_save(self):
        """Test StockValuesSerializer for data validation and saving"""
        data = {"open_value": 150.0, "high": 155.0, "low": 145.0, "close": 152.0}
        serializer = StockValuesSerializer(data=data)
        assert serializer.is_valid()
        stock_values = serializer.save(stock=self.stock)
        assert stock_values.stock == self.stock
        assert stock_values.open_value == 150.0
        assert stock_values.close == 152.0

    def test_stock_performance_serializer_validation_and_save(self):
        """Test StockPerformanceSerializer for data validation and saving"""
        data = {
            "five_days": 1.5,
            "one_month": 3.2,
            "three_months": 7.8,
            "year_to_date": 12.0,
            "one_year": 15.0,
        }
        serializer = StockPerformanceSerializer(data=data)
        assert serializer.is_valid()
        performance = serializer.save(stock=self.stock)
        assert performance.stock == self.stock
        assert performance.five_days == 1.5
        assert performance.one_year == 15.0

    def test_market_cap_serializer_validation_and_save(self):
        """Test MarketCapSerializer for data validation and saving"""
        data = {"currency": "USD", "value": 3000000000.0}
        serializer = MarketCapSerializer(data=data)
        assert serializer.is_valid()
        market_cap = serializer.save()
        assert market_cap.currency == "USD"
        assert market_cap.value == 3000000000.0

    def test_competitor_serializer_validation_and_save(self):
        """Test CompetitorSerializer for data validation and saving"""
        data = {"name": "Google Inc.", "market_cap_id": self.market_cap.id}
        serializer = CompetitorSerializer(data=data)
        assert serializer.is_valid()
        competitor = serializer.save(stock=self.stock)
        assert competitor.name == "Google Inc."
        assert competitor.market_cap == self.market_cap
        assert competitor.stock == self.stock
