import pytest
from stocks.models import Stock, StockValues, StockPerformance, Competitor, MarketCap
from datetime import date


@pytest.mark.django_db
class TestModels:
    """Tests for the models and their relationships"""

    def setup_method(self):
        """Initialize base objects for the tests"""
        self.stock = Stock.objects.create(
            status="OK",
            purchased_amount=100,
            purchased_status="active",
            request_data=date.today().isoformat(),
            company_code="AAPL",
            company_name="Apple Inc.",
        )
        self.market_cap = MarketCap.objects.create(currency="USD", value=2500000000.0)

    def test_stock_creation(self):
        """Test creation of a Stock"""
        assert Stock.objects.count() == 1
        assert self.stock.status == "OK"
        assert self.stock.purchased_amount == 100
        assert self.stock.company_code == "AAPL"
        assert self.stock.company_name == "Apple Inc."
        assert str(self.stock) == "Apple Inc./AAPL"

    def test_stock_values_relationship(self):
        """Test the relationship between Stock and StockValues"""
        stock_values = StockValues.objects.create(
            stock=self.stock, open_value=150.0, high=155.0, low=145.0, close=152.0
        )
        assert stock_values.stock == self.stock
        assert stock_values.open_value == 150.0
        assert stock_values.close == 152.0
        assert str(stock_values) == f"Values for {self.stock.company_code}"

    def test_stock_performance_relationship(self):
        """Test the relationship between Stock and StockPerformance"""
        performance = StockPerformance.objects.create(
            stock=self.stock,
            five_days=1.5,
            one_month=3.2,
            three_months=7.8,
            year_to_date=12.0,
            one_year=15.0,
        )
        assert performance.stock == self.stock
        assert performance.five_days == 1.5
        assert performance.one_year == 15.0
        assert str(performance) == f"Performance for {self.stock.company_code}"

    def test_market_cap_creation(self):
        """Test the creation for a MarketCap object"""
        assert MarketCap.objects.count() == 1
        assert self.market_cap.currency == "USD"
        assert self.market_cap.value == 2500000000.0
        assert str(self.market_cap) == "USD 2500000000.0"

    def test_competitor_relationship(self):
        """Test the relationship between Competitor and MarketCap"""
        competitor = Competitor.objects.create(
            name="Microsoft", stock=self.stock, market_cap=self.market_cap
        )
        assert competitor.stock == self.stock
        assert competitor.market_cap == self.market_cap
        assert competitor.name == "Microsoft"
        assert str(competitor) == "Microsoft"
