from django.db.models import F

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
import numpy as np

from .custom_auth import BearerTokenAuth
from .serializers import *
from .models import *
from .pagination import *
from .utils import generate_bell_curve_data, create_custom_tooltip


# Create your views here.

class SymbolsAPIView(APIView):
    authentication_classes =  [BearerTokenAuth]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = StockSymbolSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer.save()

        return Response(data={
            'Message': 'Symbol Created Successfully.'
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        symbol_code = request.query_params.get('symbol_code')
        market_code = request.query_params.get('market_code')
        page_size = request.query_params.get('page_size', 10)
        symbol_name = request.query_params.get('name')

        if (symbol_code and (not market_code)) or ((not symbol_code) and market_code):
            return Response({
                'message': 'Supply Complete Parameters for the Symbol Information.'
                }, status=status.HTTP_412_PRECONDITION_FAILED)
        
        elif symbol_code and market_code:
            symbol = SymbolInformation.objects.filter(symbol_code=symbol_code, market_code=market_code).first()
            if symbol:
                serializer = StockSymbolSerializer(symbol)

                return Response(data={
                    'data' : serializer.data
                    }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Symbol not found'
                    }, status=status.HTTP_404_NOT_FOUND)
        else:
            symbols = SymbolInformation.objects.all()
            if symbol_name:
                symbols = SymbolInformation.objects.filter(symbol_name__icontains=symbol_name)
            
            # Perform Pagination on the Data and Return it.

            pagination = PageNumberPagination()
            pagination.page_size = page_size
            page = pagination.paginate_queryset(symbols, request)
            serializer = StockSymbolSerializer(page, many=True)
    
            return pagination.get_paginated_response(
                serializer.data
            )
            # return Response(data, status=status.HTTP_200_OK)
        
    def patch(self, request):
        symbol_code = request.query_params.get('symbol_code')
        market_code = request.query_params.get('market_code')

        if (symbol_code and (not market_code)) or ((not symbol_code) and market_code):
            return Response({
                'message': 'Supply Complete Parameters for the Symbol Information.'
                }, status=status.HTTP_404_NOT_FOUND)

        elif not (symbol_code and market_code):
            return Response({
                'message': 'Both symbol_code and market_code must be provided for update.'
            }, status=status.HTTP_400_BAD_REQUEST)

        symbol = SymbolInformation.objects.filter(symbol_code=symbol_code, market_code=market_code).first()
        if not symbol:
            return Response({
                'message': 'Symbol not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = StockSymbolSerializer(symbol, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Symbol information updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        symbol_code = request.query_params.get('symbol_code')
        market_code = request.query_params.get('market_code')


        if not (symbol_code and market_code):
            return Response({
                'message': 'Both symbol_code and market_code must be provided for deletion.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif (symbol_code and (not market_code)) or ((not symbol_code) and market_code):
            return Response({
                'message': 'Supply Complete Parameters for the Symbol Information.'
                }, status=status.HTTP_404_NOT_FOUND)

        symbol = SymbolInformation.objects.filter(symbol_code=symbol_code, market_code=market_code).first()
        if not symbol:
            return Response({
                'message': 'Symbol not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        symbol.delete()

        return Response({
            'message': 'Symbol deleted successfully.'
        }, status=status.HTTP_204_NO_CONTENT)


def stocks_queryset():
    queryset = StockReportEntry.objects.select_related('stock_id').values(
            'stock_id__symbol_code',
            'stock_id__symbol_name',                # select_related -> Direct Join and values -> SQL values
            'stock_id__market_code',
            'order_reject_upper',
            'order_reject_lower',
            'last_day_close',
            'date_of_entyry'
        ).order_by('date_of_entyry').annotate(                         # Aliasing
            symbol_code=F('stock_id_id__symbol_code'),
            symbol_name=F('stock_id_id__symbol_name'),
            market_code=F('stock_id_id__market_code'),
            date_of_entry=F('date_of_entyry'),
            high=F('order_reject_upper'),
            low=F('order_reject_lower'),
            lcdp=F('last_day_close')
        )
    return queryset

class SymbolStatsAPI(ListAPIView):
    authentication_classes =  [BearerTokenAuth]
    permission_classes = [IsAuthenticated]
    pagination_class = SymbolAPIPagination
    serializer_class = SymbolStatSerializer

    def get_queryset(self):
        queryset = stocks_queryset()

        date = self.request.query_params.get('date', None)
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        symbol_code = self.request.query_params.get('symbol',None)
        market_code = self.request.query_params.get('market', None)
        symbol_name = self.request.query_params.get('name', None)

        if date:
            queryset = queryset.filter(date_of_entyry=date)
        if from_date and to_date:
            queryset = queryset.filter(date_of_entyry__range=(from_date, to_date))
        if symbol_name:
            queryset = queryset.filter(symbol_name__icontains=symbol_name)
        if symbol_code:
            queryset = queryset.filter(symbol_code=symbol_code)
        if market_code:
            queryset = queryset.filter(market_code=market_code)
        
        return queryset
    

class SymbolDeviationAPI(ListAPIView):
    authentication_classes = [BearerTokenAuth]
    permission_classes = [IsAuthenticated]
    pagination_class = SymbolAPIPagination
    serializer_class = SymbolStatSerializer

    def get_queryset(self):
        queryset = stocks_queryset()

        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)
        symbol_name = self.request.query_params.get('name', None)

        if from_date is None or to_date is None:
            raise ParseError(detail="Both 'from' and 'to' must be provided if one of them is specified.")
        if symbol_name is None:
            raise NotFound(detail="Symbol Name must be provided as a parameter 'name'.")
        
        queryset = queryset.filter(date_of_entyry__range=(from_date, to_date))

        if ',' in symbol_name:
            symbol_names = symbol_name.split(',')
            return [self.apply_deviations(queryset.filter(symbol_name__icontains=name), name) for name in symbol_names]
        else:
            queryset = queryset.filter(symbol_name__icontains=symbol_name)

        return queryset

    def apply_deviations(self, qset, name=None):
        high_vals = qset.values_list('order_reject_upper', flat=True)
        low_vals = qset.values_list('order_reject_lower', flat=True)
        lcdp_vals = qset.values_list('last_day_close', flat=True)

        high_std = np.std(high_vals)
        low_std = np.std(low_vals) 
        lcdp_std = np.std(lcdp_vals)

        # Generate bell curve data
        high_data = generate_bell_curve_data(high_std, high_std/2 )
        low_data = generate_bell_curve_data(low_std, low_std/2)
        lcdp_data = generate_bell_curve_data(lcdp_std, lcdp_std/2)

        rows = [
            [
                i,
                high_data[i][1], create_custom_tooltip(name, 'high', high_data[i][1]),
                low_data[i][1], create_custom_tooltip(name, 'low', low_data[i][1]),
                lcdp_data[i][1], create_custom_tooltip(name, 'lcdp', lcdp_data[i][1]),
            ]
            for i in range(min(len(high_data), len(low_data), len(lcdp_data)))
        ]

        return rows

    def list(self, request, *args, **kwargs):
        queryset_or_list = self.get_queryset()
        symbol_name = self.request.query_params.get('name', None)
        HEADER_ROW = [
            'Observation', 'High', {'type': 'string', 'role': 'tooltip', 'p': {'html': 'true'}},
            'Low', {'type': 'string', 'role': 'tooltip', 'p': {'html': 'true'}},
            'LCDP', {'type': 'string', 'role': 'tooltip', 'p': {'html': 'true'}}
        ]

        response_data = [HEADER_ROW]

        if isinstance(queryset_or_list, list):
            
            # Trash logic. I know. But I couldn't think better :(
            symbol_data = queryset_or_list
            rows = []
            for element in symbol_data:
                rows.extend(element)

            response_data.extend(rows)


        else:
            # When single queryset was returned
            page = self.paginate_queryset(queryset_or_list)

            if page is not None:
                response_data.extend((self.apply_deviations(queryset_or_list, name=symbol_name)))

            else:
                response_data = {}
        

        return Response(response_data)

