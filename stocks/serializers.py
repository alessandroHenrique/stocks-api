import re
from babel.core import Locale
from rest_framework import serializers
from .models import Stock, StockValues, StockPerformance, Competitor, MarketCap


class MarketCapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketCap
        fields = ["currency", "value"]

    def validate(self, data):
        """
        Validates the field market cap to get the currency and value
        """
        if data.get("currency") and data.get("value"):
            return data

        raw_market_cap = self.context.get("raw_market_cap", None)
        if not raw_market_cap:
            raise serializers.ValidationError("Market cap data is required.")
        symbol, value_str = self.get_values_from_string(raw_market_cap)

        data["currency"] = self.parse_currency_from_symbol(symbol)
        data["value"] = self.parse_value_from_string(value_str)
        return data

    def get_values_from_string(self, raw_market_cap):
        match = re.match(r"([^\d.]+)([\d.].*)", raw_market_cap)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def parse_currency_from_symbol(self, symbol):
        """
        Maps symbols to ISO codes using Babel and find the right one.
        """
        locale = Locale.parse("en_US")
        symbols = {symbol: code for code, symbol in locale.currency_symbols.items()}

        symbol = symbols.get(symbol)
        if not symbol:
            raise serializers.ValidationError(f"Symbol {symbol} not recognized.")
        return symbol

    def parse_value_from_string(self, value_str):
        """
        Generate a float number from a string
        """
        suffix_mapping = {"T": 1e12, "B": 1e9, "M": 1e6}

        if value_str[-1] in suffix_mapping:
            multiplier = suffix_mapping[value_str[-1]]
            base_value = float(value_str[:-1])
            return base_value * multiplier
        else:
            return float(value_str)


class CompetitorSerializer(serializers.ModelSerializer):
    market_cap_id = serializers.PrimaryKeyRelatedField(
        queryset=MarketCap.objects.all(), source="market_cap", write_only=True
    )
    market_cap = MarketCapSerializer(read_only=True)

    class Meta:
        model = Competitor
        fields = ["name", "market_cap", "market_cap_id"]

    def create(self, validated_data):
        return Competitor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        market_cap = validated_data.pop("market_cap", None)
        if market_cap:
            instance.market_cap = market_cap

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StockValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockValues
        fields = ["open_value", "high", "low", "close"]


class StockPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPerformance
        fields = ["five_days", "one_month", "three_months", "year_to_date", "one_year"]


class StockSerializer(serializers.ModelSerializer):
    stock_values = StockValuesSerializer(required=False, allow_null=True)
    performance_data = StockPerformanceSerializer(required=False, allow_null=True)
    competitors = CompetitorSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Stock
        fields = [
            "status",
            "purchased_amount",
            "purchased_status",
            "request_data",
            "company_code",
            "company_name",
            "stock_values",
            "performance_data",
            "competitors",
        ]
