from django.db import models
from datetime import datetime
# Create your models here.

class SymbolInformation(models.Model):
    """A class to represent the symbol meta data."""

    symbol_id = models.AutoField(primary_key=True)
    market_code = models.CharField(max_length=5)
    symbol_name = models.CharField(max_length=50)
    symbol_code = models.CharField(max_length=20, default='EMPTY')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

class StockReportEntry(models.Model):
    """A class to associate the SymbolInformation with actual day-to-day values."""
    
    stock_id = models.ForeignKey(SymbolInformation, on_delete=models.CASCADE)
    date_of_entyry = models.TextField(default=' ')
    settlement_type = models.CharField(max_length=50)
    order_reject_upper = models.FloatField(verbose_name='high', default=0.0)
    order_reject_lower = models.FloatField(verbose_name='low', default=0.0)
    last_day_close = models.FloatField(verbose_name='lcdp', default=0.0)
    created_at = models.DateField(default=datetime.now)
