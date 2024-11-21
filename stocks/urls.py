from django.urls import path
from .views import StockAPIView


urlpatterns = [
    path("stock/<str:stock_symbol>/", StockAPIView.as_view(), name="stock-detail"),
]
