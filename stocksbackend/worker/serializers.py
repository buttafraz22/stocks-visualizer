from rest_framework import serializers
from .models import *

class StockSymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SymbolInformation
        fields = ['symbol_id', 'market_code', 'symbol_name', 'symbol_code']
    
    def create(self, validated_data):
        symbol = SymbolInformation(
            symbol_name = validated_data['symbol_name'],
            market_code = validated_data['market_code'],
            symbol_code = validated_data['symbol_code']
        )
        symbol.save()
        return symbol
    
    def validate(self, attrs):
        if 'symbol_name' not in attrs or 'market_code' not in attrs or 'symbol_code' not in attrs:
            raise serializers.ValidationError("symbol_name, market_code, and symbol_code are required fields.")
        
        return attrs

class SymbolStatSerializer(serializers.Serializer):
    symbol_code = serializers.CharField(source='stock_id__symbol_code')
    market_code = serializers.CharField(source='stock_id__market_code')
    symbol_name = serializers.CharField(source='stock_id__symbol_name')
    date_of_entry = serializers.CharField(source='date_of_entyry')
    high = serializers.FloatField(source='order_reject_upper')
    low = serializers.FloatField(source='order_reject_lower')
    lcdp = serializers.FloatField(source='last_day_close')

    class Meta:
        model = StockReportEntry
        fields = ['symbol_code', 'symbol_name', 'market_code',
                  'high','low','lcdp','date_of_entry']
                    
                