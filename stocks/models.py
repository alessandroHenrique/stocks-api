from django.db import models


class Stock(models.Model):
    status = models.CharField(max_length=100, blank=True)
    purchased_amount = models.IntegerField(default=0)
    purchased_status = models.CharField(max_length=50, blank=True)
    request_data = models.DateField()
    company_code = models.CharField(max_length=20, unique=True)
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.company_name}/{self.company_code}"


class StockValues(models.Model):
    stock = models.OneToOneField(
        Stock, on_delete=models.CASCADE, related_name="stock_values"
    )
    open_value = models.FloatField(blank=True, default=0.0)
    high = models.FloatField(blank=True, default=0.0)
    low = models.FloatField(blank=True, default=0.0)
    close = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return f"Values for {self.stock.company_code}"


class StockPerformance(models.Model):
    stock = models.OneToOneField(
        Stock, on_delete=models.CASCADE, related_name="performance_data"
    )
    five_days = models.FloatField(blank=True, default=0.0)
    one_month = models.FloatField(blank=True, default=0.0)
    three_months = models.FloatField(blank=True, default=0.0)
    year_to_date = models.FloatField(blank=True, default=0.0)
    one_year = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return f"Performance for {self.stock.company_code}"


class MarketCap(models.Model):
    currency = models.CharField(max_length=20, blank=True)
    value = models.FloatField(blank=True, default=0.0)

    def __str__(self):
        return f"{self.currency} {self.value}"


class Competitor(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="competitors"
    )
    name = models.CharField(max_length=255)
    market_cap = models.OneToOneField(
        MarketCap, on_delete=models.CASCADE, related_name="competitor"
    )

    def __str__(self):
        return self.name
