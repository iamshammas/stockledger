from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from reports.serializers import CurrentStockReportSerializer, DailySalesReportSerializer, MonthlySalesReportSerializer, StockValuationReportSerializer
from .services import ReportService

from django.utils.dateparse import parse_date


class CurrentStockAPIView(GenericAPIView):
    serializer_class = CurrentStockReportSerializer

    def get(self, request):
        queryset = ReportService.get_current_stock_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StockValuationAPIView(GenericAPIView):
    serializer_class = StockValuationReportSerializer

    def get(self, request):
        queryset = ReportService.get_stock_valuation_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DailySalesAPIView(GenericAPIView):
    serializer_class = DailySalesReportSerializer

    def get(self, request):
        date_str = request.query_params.get('date')
        date = parse_date(date_str) 
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        report_data = ReportService.get_daily_sales_report(request.user.tenant, date)
        report_data['date'] = date  
        serializer = self.get_serializer(report_data)
        return Response(serializer.data)

class MonthlySalesAPIView(GenericAPIView):
    serializer_class = MonthlySalesReportSerializer

    def get(self, request):
        year = request.query_params.get('year')
        if not year or not year.isdigit() or len(year) != 4:
            return Response({"error": "Invalid year format. Use YYYY"}, status=400)
        
        report_data = ReportService.get_monthly_sales_report(request.user.tenant, int(year))
        serializer = self.get_serializer(report_data, many=True)
        return Response(serializer.data)