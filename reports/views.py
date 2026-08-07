from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from reports.serializers import CurrentStockSerializer, DailySalesSerializer, StockValuationSerializer
from .services import ReportService

from django.utils.dateparse import parse_date


class CurrentStockAPIView(GenericAPIView):
    serializer_class = CurrentStockSerializer

    def get(self, request):
        queryset = ReportService.get_current_stock_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StockValuationAPIView(GenericAPIView):
    serializer_class = StockValuationSerializer

    def get(self, request):
        queryset = ReportService.get_stock_valuation_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DailySalesAPIView(GenericAPIView):
    serializer_class = DailySalesSerializer

    def get(self, request):
        date_str = request.query_params.get('date')
        date = parse_date(date_str) 
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        report_data = ReportService.get_daily_sales_report(request.user.tenant, date)
        report_data['date'] = date  
        serializer = self.get_serializer(report_data)
        return Response(serializer.data)