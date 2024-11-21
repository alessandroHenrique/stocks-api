import boto3
import json
import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, timedelta
from django.core.cache import cache
from django.db.models import Prefetch
from django.utils import timezone
from .models import Competitor, Stock
from .serializers import (
    StockSerializer,
    StockValuesSerializer,
    StockPerformanceSerializer,
    MarketCapSerializer,
    CompetitorSerializer,
    StockResponseSerializer,
    StockRequestSerializer,
)
from .utils import invoke_lambda, get_last_valid_day


logger = logging.getLogger("stocks")


class StockAPIView(APIView):
    def fetch_data_from_lambda(self, service_name, payload):
        """
        Fetches data from a specific Lambda service and validates the response.
        """
        response = invoke_lambda(service_name, payload)
        if response.get("statusCode") != 200:
            error_msg = response.get("body", {}).get("error", "Unknown error")
            raise ValueError(f"{service_name} error: {error_msg}")
        return response.get("body")

    def create_or_update_stock_data(self, stock_symbol, company_name, polygon_data):
        stock = self.get_stock(stock_symbol)

        stock_data = {
            "status": polygon_data.get("status"),
            "request_data": polygon_data.get("from"),
            "company_code": stock_symbol,
            "company_name": company_name,
        }

        stock_serializer = StockSerializer(instance=stock, data=stock_data)
        stock_serializer.is_valid(raise_exception=True)
        return stock_serializer.save()

    def create_or_update_stock_values(self, stock, polygon_data):
        """
        Updates stock values using the polygon data.
        """
        stock_values_data = {
            "open_value": polygon_data.get("open"),
            "high": polygon_data.get("high"),
            "low": polygon_data.get("low"),
            "close": polygon_data.get("close"),
        }

        stock_values_serializer = StockValuesSerializer(
            instance=getattr(stock, "stock_values", None), data=stock_values_data
        )
        stock_values_serializer.is_valid(raise_exception=True)
        stock_values_serializer.save(stock=stock)

    def create_or_update_performance_data(self, stock, performance_data):
        """
        Updates stock performance data using the provided data.
        """
        stock_performance_data = {
            "five_days": performance_data.get("5_day", 0.0),
            "one_month": performance_data.get("1_month", 0.0),
            "three_months": performance_data.get("3_month", 0.0),
            "year_to_date": performance_data.get("ytd", 0.0),
            "one_year": performance_data.get("1_year", 0.0),
        }

        stock_performance_serializer = StockPerformanceSerializer(
            instance=getattr(stock, "performance_data", None),
            data=stock_performance_data,
        )
        stock_performance_serializer.is_valid(raise_exception=True)
        stock_performance_serializer.save(stock=stock)

    def create_or_update_competitors(self, stock, competitors):
        """
        Updates the stock's competitors data.
        """
        existing_competitors = (
            {c.name: c for c in stock.competitors.all()}
            if stock.competitors.exists()
            else {}
        )

        for competitor in competitors:
            market_cap_data = competitor.get("market_cap")
            market_cap_serializer = MarketCapSerializer(
                data={}, context={"raw_market_cap": market_cap_data}
            )
            market_cap_serializer.is_valid(raise_exception=True)
            market_cap = market_cap_serializer.save()

            competitor_name = competitor.get("name")
            competitor_instance = existing_competitors.get(competitor_name, None)
            competitor_data = {
                "name": competitor_name,
                "market_cap_id": market_cap.id,
            }

            competitor_serializer = CompetitorSerializer(
                instance=competitor_instance, data=competitor_data
            )
            competitor_serializer.is_valid(raise_exception=True)
            competitor_serializer.save(stock=stock)

    @swagger_auto_schema(
        operation_description="Retrieve stock data for a given symbol",
        responses={200: StockResponseSerializer()},
    )
    def get(self, request, stock_symbol):
        stock_symbol = stock_symbol.upper()
        cache_key = f"stock_{stock_symbol}"
        cached_data = cache.get(cache_key)
        last_valid_day = get_last_valid_day()

        if cached_data and last_valid_day == cached_data.get("request_data"):
            logger.info(f"Cache hit for {stock_symbol} on {last_valid_day}")
            return Response(cached_data, status=200)

        try:
            logger.info(f"Fetching data for {stock_symbol}")
            polygon_data = self.fetch_data_from_lambda(
                "polygon_data", {"symbol": stock_symbol, "start_date": last_valid_day}
            )
            logger.debug(f"Polygon data fetched: {polygon_data}")

            logger.info(f"Fetching data from Market watch")
            company_name, performance_data, competitors = self.fetch_data_from_lambda(
                "marketwatch_data", {"symbol": stock_symbol}
            )
            logger.debug(
                f"Marketwatch data fetched for {stock_symbol}: {company_name}, {performance_data}, {competitors}"
            )

            stock = self.create_or_update_stock_data(
                stock_symbol, company_name, polygon_data
            )
            self.create_or_update_stock_values(stock, polygon_data)
            self.create_or_update_performance_data(stock, performance_data)
            self.create_or_update_competitors(stock, competitors)

            stock.refresh_from_db()
            stock_serializer = StockSerializer(stock)
            data = stock_serializer.data
            cache.set(cache_key, data, timeout=86400 * 7)

            return Response(data, status=200)

        except ValueError as e:
            logger.error(f"Error while fetching stock data: {e}")
            return Response({"error": str(e)}, status=502)

        except Exception as e:
            logger.error(f"Error while fetching stock data: {e}")
            return Response({"error": str(e)}, status=500)

    @swagger_auto_schema(
        operation_description="Update stock purchase information",
        request_body=StockRequestSerializer,
        responses={201: "Stock purchase updated successfully"},
    )
    def post(self, request, stock_symbol):
        try:
            stock_symbol = stock_symbol.upper()
            amount = request.data.get("amount")
            if not isinstance(amount, (int, float)) or amount < 0:
                return Response(
                    {"error": "The 'amount' field must be a positive number."},
                    status=400,
                )
            stock = self.get_stock(stock_symbol)

            if not stock:
                stock_data = {
                    "company_code": stock_symbol,
                    "purchased_amount": amount,
                    "purchased_status": "active",
                }

                stock_serializer = StockSerializer(data=stock_data)
                stock_serializer.is_valid(raise_exception=True)
                stock = stock_serializer.save()
            else:
                stock.purchased_amount += int(amount)
                stock.save()

                cache_key = f"stock_{stock_symbol}"
                if cache.get(cache_key):
                    data = cache.get(cache_key)
                    data["purchased_amount"] = stock.purchased_amount
                    data["purchased_status"] = "active"
                else:
                    data = stock
                cache.set(cache_key, data, timeout=86400 * 7)

            return Response(
                {
                    "message": f"{amount} units of stock {stock_symbol} were added to your stock record."
                },
                status=201,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_stock(self, company_code):
        return (
            Stock.objects.select_related("stock_values", "performance_data")
            .prefetch_related(
                Prefetch(
                    "competitors",
                    queryset=Competitor.objects.select_related("market_cap"),
                )
            )
            .filter(company_code=company_code)
            .first()
        )
