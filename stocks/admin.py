from django.contrib import admin
from .models import Stock, StockValues


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("company_name", "company_code", "status", "purchased_amount")
    search_fields = ("company_name", "company_code")
