from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Stock
from .models import StockPrices
from .models import Transaction
from .models import Holdings
from .models import Portfolio


@admin.register(Stock)
class StockAdmin(ImportExportModelAdmin):
    pass


@admin.register(StockPrices)
class StockPricesAdmin(ImportExportModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    pass


@admin.register(Holdings)
class HoldingsAdmin(ImportExportModelAdmin):
    pass


@admin.register(Portfolio)
class PortfolioAdmin(ImportExportModelAdmin):
    pass
